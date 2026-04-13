from django.db.models import Q
from .dependancies import *

def getBeneficeSales(data):
	benefice = 0
	for s in data:
		# Utiliser le prix d'achat enregistré lors de la vente, sinon repli sur le prix actuel du produit
		buy_price = s.buy_price if hasattr(s, 'buy_price') and s.buy_price > 0 else s.product.buy_price
		pat = buy_price * s.quantity
		benefice += (s.amount - pat)

	return benefice

def getBeneficeSupplies(data):
	benefice = 0
	for s in data:
		pat = s.product.sale_price*s.quantity
		benefice += (s.total_buy_price-pat)

	return benefice

class ShopViewSet(viewsets.ModelViewSet):
	authentication_classes = SessionAuthentication, JWTAuthentication
	permission_classes = IsAuthenticated,
	queryset = Shop.objects.all()
	serializer_class = ShopSerializer
	ordering = ['-created_at']

	def _check_subscription_status(self, shop):
		"""
		Vérifie si l'abonnement de la boutique est expiré.
		Si oui, désactive la boutique.
		Renvoie True si la boutique est active, False sinon.
		"""
		if not shop.is_active:
			return False
			
		# Désactivation temporaire de l'auto-désactivation (souhait utilisateur)
		# if shop.trial_end_date and shop.trial_end_date < timezone.now():
		# 	print(f"[AUTO-DESACTIVATION] Boutique {shop.id} ({shop.name}) expirée le {shop.trial_end_date}. Désactivation...")
		# 	shop.is_active = False
		# 	shop.save(update_fields=['is_active'])
		# 	return False
			
		return True

	def _check_subscription_status_and_raise(self, shop):
		"""
		Vérifie si l'abonnement est expiré et lève une erreur si c'est le cas.
		Utilisé pour bloquer l'accès (Paywall).
		"""
		# D'abord on met à jour le statut si nécessaire
		is_valid = self._check_subscription_status(shop)
		
		if not is_valid:
			# Si la boutique est inactive (expirée ou désactivée manuellement)
			# On renvoie une erreur 403 spécifique pour que le front affiche le Paywall
			from rest_framework.exceptions import PermissionDenied
			raise PermissionDenied(detail={
				"code": "SUBSCRIPTION_EXPIRED",
				"message": "Votre abonnement est expiré. Veuillez payer pour continuer.",
				"shop_id": shop.id
			})

	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		# Vérifier l'expiration en temps réel et BLOQUER si expiré
		try:
			self._check_subscription_status_and_raise(instance)
		except Exception as e:
			# Si c'est une 403, on laisse passer pour que le front gère
			# Si l'utilisateur est admin/agent, on le laisse peut-être voir ?
			# Pour l'instant on bloque tout le monde sauf superuser
			if not request.user.is_superuser:
				raise e
				
		serializer = self.get_serializer(instance)
		return Response(serializer.data)

	def list(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())
		
		# Vérifier l'expiration pour toutes les boutiques de la liste (optimisation possible mais nécessaire pour la cohérence)
		# On ne le fait que pour les boutiques actives pour éviter des écritures inutiles
		for shop in queryset:
			if shop.is_active:
				self._check_subscription_status(shop)

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)


	def get_queryset(self):
		user = self.request.user
		queryset = Shop.objects.select_related("owner", "owner__user", "owner__created_by")
		
		# Les superusers voient toutes les boutiques
		if user.is_superuser:
			return queryset
		
		# Vérifier si l'utilisateur est un agent
		is_agent = user.groups.filter(name='agent').exists() or (hasattr(user, 'account') and user.account and user.is_staff and not user.is_superuser)
		
		if is_agent:
			# Les agents voient leurs propres boutiques, les boutiques des utilisateurs qu'ils ont créés,
			# ET les boutiques qui leur sont explicitement assignées comme agent.
			queryset = queryset.filter(Q(owner__created_by=user) | Q(owner__user=user) | Q(agent__user=user))
		else:
			# Les utilisateurs normaux voient uniquement leurs propres boutiques (liste et détail)
			queryset = queryset.filter(owner__user=user)
		
		return queryset

	def _user_is_agent(self, user):
		return user.groups.filter(name='agent').exists() or (
			hasattr(user, 'account') and user.account and user.is_staff and not user.is_superuser
		)

	def partial_update(self, request, *args, **kwargs):
		"""
		Réservé aux admins et agents pour les champs sensibles.
		"""
		user = request.user
		is_agent = self._user_is_agent(user)
		
		# Vérifier les permissions pour les champs sensibles : uniquement admin et agent
		sensitive_fields = ["is_active", "subscription_plan", "trial_end_date", "shop_password"]
		if any(field in request.data for field in sensitive_fields) and not (user.is_superuser or is_agent):
			return Response(
				{
					"details": "Action non autorisée. Seuls les administrateurs et les agents peuvent modifier ces informations."
				},
				status=status.HTTP_403_FORBIDDEN,
			)

		# Restriction Agent : FREE uniquement
		if "subscription_plan" in request.data and is_agent and not user.is_superuser:
			if request.data.get("subscription_plan") != 'FREE':
				return Response(
					{"details": "Les agents ne peuvent activer que le plan Essai Gratuit (FREE)."},
					status=status.HTTP_403_FORBIDDEN
				)
		
		# Récupérer l'objet shop avant la mise à jour
		shop = self.get_object()
		
		# Extraire shop_password des données si présent et autorisé (admin/agent uniquement)
		shop_password_value = None
		if "shop_password" in request.data and (user.is_superuser or is_agent):
			shop_password_value = request.data.get("shop_password")
		
		# Si l'utilisateur n'est pas admin/agent, retirer shop_password des données s'il est présent (sécurité redondante)
		if not (user.is_superuser or is_agent) and "shop_password" in request.data:
			from django.http import QueryDict
			mutable_data = request.data.copy()
			if isinstance(mutable_data, QueryDict):
				mutable_data = mutable_data.dict()
			mutable_data.pop("shop_password", None)
			request._full_data = mutable_data
		
		# Appeler la méthode parente pour la mise à jour standard
		response = super().partial_update(request, *args, **kwargs)
		
		# S'assurer que shop_password est bien sauvegardé si présent (admin/agent uniquement)
		if shop_password_value is not None:
			# Si la valeur est une chaîne vide, la mettre à None, sinon utiliser la valeur
			shop.shop_password = None if shop_password_value == "" else shop_password_value
			shop.save(update_fields=['shop_password'])
			
		# Log de l'activation/changement de plan
		if any(field in request.data for field in ["is_active", "subscription_plan", "trial_end_date"]):
			shop.refresh_from_db()
			user_type = "admin" if user.is_superuser else "agent"
			print(f"[ACCREDITATION BOUTIQUE] Boutique {shop.id} modifiée par {user_type} {user.username}: active={shop.is_active}, plan={shop.subscription_plan}, fin_essai={shop.trial_end_date}")
			
			# Créer une notification pour le propriétaire
			from api.accounts.models import Notification
			if "is_active" in request.data and shop.is_active:
				Notification.objects.create(
					account=shop.owner,
					notification_type='SUCCESS',
					title="Boutique Activée",
					message=f"Félicitations ! Votre boutique {shop.name} a été activée par l'administration."
				)
		
		return response

	def update(self, request, *args, **kwargs):
		"""
		Réservé aux admins et agents pour les champs sensibles.
		"""
		user = request.user
		is_agent = self._user_is_agent(user)
		
		# Vérifier les permissions pour les champs sensibles : uniquement admin et agent
		sensitive_fields = ["is_active", "subscription_plan", "trial_end_date", "shop_password"]
		if any(field in request.data for field in sensitive_fields) and not (user.is_superuser or is_agent):
			return Response(
				{
					"details": "Action non autorisée. Seuls les administrateurs et les agents peuvent modifier ces informations."
				},
				status=status.HTTP_403_FORBIDDEN,
			)
		
		# Récupérer l'objet shop avant la mise à jour
		shop = self.get_object()
		
		# Extraire shop_password des données si présent et autorisé (admin/agent uniquement)
		shop_password_value = None
		if "shop_password" in request.data and (user.is_superuser or is_agent):
			shop_password_value = request.data.get("shop_password")
		
		# Si l'utilisateur n'est pas admin/agent, retirer shop_password des données
		if not (user.is_superuser or is_agent) and "shop_password" in request.data:
			from django.http import QueryDict
			mutable_data = request.data.copy()
			if isinstance(mutable_data, QueryDict):
				mutable_data = mutable_data.dict()
			mutable_data.pop("shop_password", None)
			request._full_data = mutable_data
		
		# Appeler la méthode parente pour la mise à jour standard
		response = super().update(request, *args, **kwargs)
		
		# S'assurer que shop_password est bien sauvegardé si présent (admin/agent uniquement)
		if shop_password_value is not None:
			shop.shop_password = None if shop_password_value == "" else shop_password_value
			shop.save(update_fields=['shop_password'])

		# Log de l'activation/changement de plan
		if any(field in request.data for field in ["is_active", "subscription_plan", "trial_end_date"]):
			shop.refresh_from_db()
			user_type = "admin" if user.is_superuser else "agent"
			print(f"[SHOP ACCREDITATION] Boutique {shop.id} modifiée par {user_type} {user.username}: active={shop.is_active}, plan={shop.subscription_plan}, fin_essai={shop.trial_end_date}")
			
			# Créer une notification pour le propriétaire
			from api.accounts.models import Notification
			if "is_active" in request.data and shop.is_active:
				Notification.objects.create(
					account=shop.owner,
					notification_type='SUCCESS',
					title="Boutique Activée",
					message=f"Félicitations ! Votre boutique {shop.name} a été activée par l'administration."
				)
		
		return response

	
	@transaction.atomic()
	def create(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		user = request.user
		
		# Récupérer le propriétaire depuis les données (pour les agents/admin)
		owner_id = serializer.validated_data.get("owner")
		if owner_id:
			try:
				account = Account.objects.get(id=owner_id, is_active=True)
			except Account.DoesNotExist:
				# Message clair en français pour l'utilisateur
				return Response(
					{"details": "Le compte propriétaire spécifié est introuvable ou inactif."},
					status=status.HTTP_400_BAD_REQUEST,
				)

			# Vérifier que l'agent/admin peut créer une boutique pour cet utilisateur
			is_agent = user.groups.filter(name='agent').exists() or (hasattr(user, 'account') and user.account and user.is_staff and not user.is_superuser)
			
			if is_agent and not user.is_superuser:
				# Les agents ne peuvent créer des boutiques que pour leurs propres utilisateurs
				if account.created_by != user:
					return Response(
						{"details": "Vous ne pouvez créer des boutiques que pour les utilisateurs que vous avez vous‑même créés."},
						status=status.HTTP_403_FORBIDDEN,
					)
		else:
			# Si aucun propriétaire n'est spécifié, utiliser l'utilisateur connecté (comportement par défaut)
			try:
				account = Account.objects.get(user=user, is_active=True)
			except Account.DoesNotExist:
				# Ancien message en kirundi remplacé par un message explicite en français
				return Response(
					{"details": "Votre compte utilisateur n’est pas autorisé à créer une boutique (compte introuvable ou inactif)."},
					status=status.HTTP_400_BAD_REQUEST,
				)

		# Mot de passe de la boutique : uniquement pour les admins/agents
		is_agent = user.groups.filter(name='agent').exists() or (
			hasattr(user, 'account') and user.account and user.is_staff and not user.is_superuser
		)
		raw_shop_password = serializer.validated_data.get("shop_password")
		if not (user.is_superuser or is_agent):
			# Les utilisateurs simples ne peuvent pas définir/modifier le mot de passe de la boutique
			raw_shop_password = None

		# Système d'essai gratuit par défaut (3 mois)
		now = timezone.now()
		trial_end = now + timedelta(days=90)
		
		shop = Shop(
			owner=account,
			name=serializer.validated_data.get("name"),
			province=serializer.validated_data.get("province"),
			commune=serializer.validated_data.get("commune"),
			quarter=serializer.validated_data.get("quarter"),
			address=serializer.validated_data.get("address"),
			is_active=True, # Activé par défaut selon la demande de l'utilisateur
			shop_password=raw_shop_password,
			trial_start_date=now,
			trial_end_date=trial_end,
			subscription_plan='FREE'
		)

		shop.save()
		
		# Créer une notification pour l'admin/agent (optionnel mais recommandé)
		Notification.objects.create(
			account=account,
			notification_type='INFO',
			title="Nouvelle boutique créée",
			message=f"Votre boutique {shop.name} a été créée avec succès et est déjà active."
		)

		serializer = self.get_serializer(shop).data
		return Response(serializer, status=status.HTTP_201_CREATED)
	

	@transaction.atomic()
	@csrf_exempt
	@action(
		methods=['GET'],
		detail=True,
		url_name=r'sales',
		url_path=r"sales",
		permission_classes=[IsAuthenticated],)
	def shopSales(self, request, pk):
		shop = self.get_object()
		if(shop.owner.user != request.user):
			# Message d'erreur en français si l'utilisateur n'est pas propriétaire de la boutique
			return Response(
				{"details": "Vous ne pouvez consulter les ventes que pour vos propres boutiques."},
				status=status.HTTP_400_BAD_REQUEST,
			)
		
		sales = Sales.objects.filter(created_at__gte=datetime.today())
		

		return Response({"status":"Contrôle terminé avec succès"}, status=status.HTTP_200_OK)

	
	@transaction.atomic()
	@csrf_exempt
	@action(
		methods=['POST'],
		detail=True,
		url_name=r'set_position',
		url_path=r"set_position",
		permission_classes=[IsAuthenticated],)
	def set_position(self, request, pk):
		shop = self.get_object()
		longitude = request.data.get("longitude")
		latitude = request.data.get("latitude")

		if(shop.owner.user != request.user):
			# Message d'erreur en français si l'utilisateur n'est pas propriétaire de la boutique
			return Response(
				{"details": "Vous ne pouvez définir la position GPS que pour vos propres boutiques."},
				status=status.HTTP_400_BAD_REQUEST,
			)
		
		shop.latitude = latitude
		shop.longitude = longitude
		shop.save()
		return Response({"status":"Position GPS mise à jour avec succès"}, status=status.HTTP_200_OK)
	

	@transaction.atomic()
	@csrf_exempt
	@action(
		methods=['GET'],
		detail=True,
		url_name=r'stats',
		url_path=r"stats",
		permission_classes=[IsAuthenticated],)
	def stats(self, request, pk):
		str_du = request.query_params.get('created_at__gte')
		str_au = request.query_params.get('created_at__lte')
		shop:Shop = self.get_object()
		# 1. PAYWALL : Restriction pour les comptes GRATUITS (Désactivée pour permettre l'essai complet)
		# if shop.subscription_plan == 'FREE':
		# 	return Response(
		# 		{"details": "Les statistiques avancées sont réservées aux membres Premium.", "code": "PREMIUM_REQUIRED"},
		# 		status=status.HTTP_403_FORBIDDEN
		# 	)

		sales={}
		supply={}
		supply_f=[]
		sales_f=[]
		b_sales=0
		b_supplies=0

		if(str_du and str_au):
			str_au = datetime.strptime(str_au, "%Y-%m-%d")+timedelta(days=1)
			str_au = str_au.strftime("%Y-%m-%d")

			sales_f = Sales.objects.filter(
				created_at__gte=str_du, created_at__lte=str_au, product__shop=shop.id
			)
			sales = sales_f.aggregate(
				total_sales=models.Sum('quantity'),
				total_amount=models.Sum('amount')
			)
			if len(sales_f)>0:
				b_sales = getBeneficeSales(sales_f)

			supply_f = Supply.objects.filter(
				created_at__gte=str_du, created_at__lte=str_au, product__shop=shop.id,
				quantity__gt=0, total_buy_price__gt=0,
			)
			supply = supply_f.aggregate(
				total_supplies=models.Sum('quantity'),
				total_amount=models.Sum('total_buy_price'),
			)
			if len(supply_f) > 0:
				b_supplies = getBeneficeSupplies(supply_f)


		else:
			today = datetime.now().date()
			if(not request.user.is_superuser):
				sales_f = Sales.objects.filter(
					created_at__date=today, product__shop=shop.id
				)
				sales = sales_f.aggregate(
					total_sales=models.Sum('quantity'),
					total_amount=models.Sum('amount')
				)
				if len(sales_f) > 0:
					b_sales = getBeneficeSales(sales_f)

				supply_f = Supply.objects.filter(
					created_at__date=today, product__shop=shop.id,
					quantity__gt=0, total_buy_price__gt=0,
				)
				supply = supply_f.aggregate(
					total_supplies=models.Sum('quantity'),
					total_amount=models.Sum('total_buy_price'),
				)
				if len(supply_f) > 0:
					b_supplies = getBeneficeSupplies(supply_f)
				
		# Dépenses générales
		today = datetime.now().date()
		general_expenses_qs = Expense.objects.filter(shop=shop)
		if str_du and str_au:
			general_expenses_qs = general_expenses_qs.filter(created_at__date__gte=str_du, created_at__date__lte=str_au)
		else:
			general_expenses_qs = general_expenses_qs.filter(created_at__date=today)
		
		total_general_expenses = general_expenses_qs.aggregate(total=models.Sum('amount'))['total'] or 0

		# Métriques globales (Stock et Articles)
		products_qs = Product.objects.filter(shop=shop)
		stock_stats = products_qs.aggregate(
			stock_volume=models.Sum('quantity'),
			stock_value=models.Sum(models.F('quantity') * models.F('sale_price')),
			stock_cost=models.Sum(models.F('quantity') * models.F('buy_price'))
		)
		active_articles = products_qs.filter(quantity__gt=0).count()
		critical_articles = products_qs.filter(quantity__gt=0, quantity__lt=5).count()

		# Calculs financiers finaux
		total_daily_sales = float(sales.get('total_amount') or 0)
		total_stock_expenses = float(supply.get('total_amount') or 0)
		total_general_expenses = float(total_general_expenses)
		total_expenses = total_stock_expenses + total_general_expenses
		total_profit = float(b_sales) - total_general_expenses

		# Dernière date de contrôle (Max des produits) & Fréquence
		last_control = products_qs.aggregate(last=models.Max('last_control_at'))['last']
		
		# Récupérer la fréquence de contrôle paramétrée
		control_freq_obj = ControlFrequency.objects.filter(shop=shop).first()
		control_freq_minutes = 0
		if control_freq_obj:
			control_freq_minutes = (control_freq_obj.days * 24 * 60) + (control_freq_obj.hours * 60) + control_freq_obj.minutes

		data = {
			"sales": sales,
			"b_sales": b_sales,
			"supply": supply,
			"b_supplies": b_supplies,
			"stock_volume": stock_stats['stock_volume'] or 0,
			"stock_value": stock_stats['stock_value'] or 0,
			"stock_cost": stock_stats['stock_cost'] or 0,
			"active_articles": active_articles,
			"critical_articles": critical_articles,
			"total_general_expenses": total_general_expenses,
			"total_expenses": total_expenses,
			"total_profit": total_profit,
			"subscription_plan": shop.subscription_plan,
			"trial_start_date": shop.trial_start_date,
			"trial_end_date": shop.trial_end_date,
			"last_control_at": last_control,
			"control_frequency_minutes": control_freq_minutes
		}
		return Response(data, 200)


	@action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
	@transaction.atomic
	def activate_subscription(self, request, pk=None):
		"""
		Active manuellement un abonnement ou une période d'essai pour une boutique.
		Accessible uniquement aux Admins et Agents.
		
		Paramètres (body):
		- plan: 'FREE', 'MONTHLY', '3MONTHS', '6MONTHS', 'YEARLY'
		- duration_days: (Optionnel) Durée personnalisée en jours (uniquement pour les agents en mode FREE)
		- duration_months: (Optionnel) Durée personnalisée en mois (uniquement pour les agents en mode FREE)
		"""
		shop = self.get_object()
		user = request.user
		is_agent = self._user_is_agent(user)

		# 1. Vérification des permissions (Admin ou Agent)
		if not (user.is_superuser or is_agent):
			return Response(
				{"details": "Action non autorisée. Réservé aux administrateurs et agents."},
				status=status.HTTP_403_FORBIDDEN
			)

		# Restriction Agent : FREE uniquement
		plan = request.data.get('plan')
		if is_agent and not user.is_superuser and plan != 'FREE':
			return Response(
				{"details": "Les agents ne peuvent activer que l'essai gratuit (FREE)."},
				status=status.HTTP_403_FORBIDDEN
			)
		
		# 2. Récupération et validation des données
		plan = request.data.get('plan')
		duration_days = request.data.get('duration_days') # Entier
		duration_months = request.data.get('duration_months') # Entier

		allowed_plans = ['FREE', 'MONTHLY', '3MONTHS', '6MONTHS', 'YEARLY']
		if plan not in allowed_plans:
			return Response(
				{"details": f"Plan invalide. Choix possibles : {', '.join(allowed_plans)}"},
				status=status.HTTP_400_BAD_REQUEST
			)

		# 3. Calcul de la date de fin
		now = timezone.now()
		end_date = now

		if plan == 'FREE':
			# Logique pour l'essai gratuit (Agent/Admin)
			# Par défaut 3 mois si rien n'est spécifié
			days_to_add = 90 
			
			if is_agent and (duration_days or duration_months):
				# Les agents peuvent personnaliser la durée de l'essai
				try:
					d_days = int(duration_days) if duration_days else 0
					d_months = int(duration_months) if duration_months else 0
					
					if d_days < 0 or d_months < 0:
						raise ValueError
						
					if d_days == 0 and d_months == 0:
						days_to_add = 90 # Fallback si 0
					else:
						# Calcul approximatif pour les mois (30 jours)
						days_to_add = d_days + (d_months * 30)
				except ValueError:
					return Response(
						{"details": "Les durées doivent être des nombres entiers positifs."},
						status=status.HTTP_400_BAD_REQUEST
					)
			
			end_date = now + timedelta(days=days_to_add)

		elif plan == 'MONTHLY':
			end_date = now + timedelta(days=30)
		elif plan == '3MONTHS':
			end_date = now + timedelta(days=90)
		elif plan == '6MONTHS':
			end_date = now + timedelta(days=180)
		elif plan == 'YEARLY':
			end_date = now + timedelta(days=365)

		# 4. Mise à jour de la boutique
		shop.is_active = True
		shop.subscription_plan = plan
		shop.trial_start_date = now
		shop.trial_end_date = end_date
		shop.save()

		# 5. Logging et Notification
		user_type = "Administrateur" if user.is_superuser else "Agent"
		plan_label = dict(Shop._meta.get_field('subscription_plan').choices).get(plan, plan)
		
		# Log console
		print(f"[ACTIVATION ABONNEMENT] Boutique {shop.id} activée par {user_type} {user.username}. Plan: {plan}, Fin: {end_date}")

		# Notification
		from api.accounts.models import Notification
		Notification.objects.create(
			account=shop.owner,
			notification_type='SUCCESS',
			title="Abonnement Activé",
			message=f"Votre souscription '{plan_label}' a été activée par un {user_type}. Elle est valide jusqu'au {end_date.strftime('%d/%m/%Y')}."
		)

		return Response({
			"details": "Abonnement activé avec succès.",
			"shop_id": shop.id,
			"plan": plan,
			"end_date": end_date,
			"is_active": True
		}, status=status.HTTP_200_OK)


	@action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
	@transaction.atomic
	def request_upgrade(self, request, pk=None):
		"""
		Permet au propriétaire d'une boutique de demander un passage en Premium.
		Notifie l'agent responsable et les administrateurs.
		"""
		shop = self.get_object()
		user = request.user

		# Vérifier que l'utilisateur est bien le propriétaire (ou gérant)
		if shop.owner.user != user:
			return Response(
				{"details": "Seul le propriétaire de la boutique peut faire cette demande."},
				status=status.HTTP_403_FORBIDDEN
			)

		contact_info = request.data.get('contact_info', '') 
		
		# Si pas d'info, on prend celles du user
		if not contact_info:
			contact_info = f"Tel: {shop.owner.phone_number or shop.owner.user.username} / Email: {shop.owner.user.email}"

		# 1. Notifier l'Agent responsable (s'il y en a un)
		from api.accounts.models import Notification
		
		agent_notified = False
		if shop.agent:
			Notification.objects.create(
				account=shop.agent,
				notification_type='WARNING', # Warning pour attirer l'attention
				title="🚀 Demande d'upgrade Premium",
				message=f"La boutique '{shop.name}' souhaite passer en Premium.\nContact client (Auto): {contact_info}",
				related_object_type='shop',
				related_object_id=shop.id
			)
			agent_notified = True

		# 2. Notifier tous les Administrateurs (Superusers)
		# On récupère les comptes liés aux superusers
		admin_accounts = Account.objects.filter(user__is_superuser=True)
		for admin in admin_accounts:
			# Éviter de notifier deux fois si l'admin est aussi l'agent (peu probable mais possible)
			if agent_notified and shop.agent == admin:
				continue
				
			Notification.objects.create(
				account=admin,
				notification_type='WARNING',
				title="🚀 Demande d'upgrade Premium",
				message=f"La boutique '{shop.name}' (Propriétaire: {shop.owner.user.username}) souhaite passer en Premium.\nContact (Auto): {contact_info}",
				related_object_type='shop',
				related_object_id=shop.id
			)

		return Response({
			"details": "Votre demande a été envoyée ! Un agent ou un administrateur vous contactera rapidement.",
			"success": True
		}, status=status.HTTP_200_OK)



class ControlFrequencyViewSet(viewsets.ModelViewSet):
	authentication_classes = SessionAuthentication, JWTAuthentication
	permission_classes = IsAuthenticated,
	queryset = ControlFrequency.objects.all()
	serializer_class = ControlFrequencySerializer


	def get_queryset(self):
		user = self.request.user
		queryset = ControlFrequency.objects.select_related("shop")
		if user.is_superuser:
			return queryset
		shop = self.request.query_params.get("shop")
		if shop:
			return queryset.filter(shop=shop)
		# Pour retrieve/update/destroy : pas de ?shop= ; autoriser les CF des boutiques de l'utilisateur
		if self.action in ("retrieve", "update", "partial_update", "destroy"):
			return queryset.filter(shop__owner__user=user)
		return queryset.none()