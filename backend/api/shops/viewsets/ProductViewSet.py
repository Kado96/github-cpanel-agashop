from .dependancies import *
from django.conf import settings
from django.core.files import File
import os
import unicodedata
from django.db.models import Sum, F, FloatField


def _normalize_for_filename(s):
	"""Normalise une chaîne pour la comparaison avec des noms de fichiers (sans accents, minuscules, espaces -> _)."""
	if not s:
		return ""
	s = unicodedata.normalize("NFD", s)
	s = "".join(c for c in s if unicodedata.category(c) != "Mn")
	return s.lower().strip().replace(" ", "_").replace("-", "_")


def find_image_for_product_name(product_name):
	"""
	Cherche dans MEDIA_ROOT/images/ un fichier dont le nom correspond au produit.
	Retourne le chemin absolu du fichier ou None.
	"""
	if not product_name or not product_name.strip():
		return None
	media_images = os.path.join(settings.MEDIA_ROOT, "images")
	if not os.path.isdir(media_images):
		return None
	normalized_name = _normalize_for_filename(product_name)
	# Fichiers image courants
	allowed_ext = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp")
	for filename in os.listdir(media_images):
		fpath = os.path.join(media_images, filename)
		if os.path.isdir(fpath):
			continue
		base, ext = os.path.splitext(filename)
		if ext.lower() not in allowed_ext:
			continue
		normalized_base = _normalize_for_filename(base)
		if normalized_base == normalized_name or normalized_name in normalized_base or normalized_base in normalized_name:
			return fpath
	return None


class BasicProductViewSet(viewsets.ModelViewSet):
	authentication_classes = (SessionAuthentication, JWTAuthentication)
	permission_classes = (IsAuthenticated,)
	# Ordre alphabétique par défaut + id pour un ordre stable et prévisible
	queryset = BasicProduct.objects.all().order_by("name", "id")
	serializer_class = BasicProductSerializer
	filter_backends = [filters.DjangoFilterBackend]
	filterset_fields = {
		"name": ["icontains"],
		"sub_category": ["exact"],
		"created_at": ["gte", "lte"],
		"id": ["gt"],
	}

	def create(self, request, *args, **kwargs):
		"""
		Évite les doublons de produits de base:
		- Même nom (insensible à la casse, espaces trim) ET même sous-catégorie => on réutilise l'existant
		- Si une nouvelle image est fournie, on met à jour l'image de l'existant
		"""
		try:
			raw_name = request.data.get("name") or ""
			name = raw_name.strip()
			sub_category_id = request.data.get("sub_category")

			if name and sub_category_id:
				existing = BasicProduct.objects.filter(
					name__iexact=name,
					sub_category_id=sub_category_id
				).first()

				if existing is not None:
					# Mise à jour de l'image si une nouvelle est fournie
					image_file = request.FILES.get("image")
					if image_file:
						existing.image = image_file
						existing.save(update_fields=["image", "updated_at"])
					elif not existing.image and name:
						# Si pas d'image en base, tenter de la retrouver sur disque
						image_path = find_image_for_product_name(name)
						if image_path:
							with open(image_path, "rb") as f:
								existing.image.save(os.path.basename(image_path), File(f), save=True)

					serializer = self.get_serializer(existing)
					return Response(serializer.data, status=status.HTTP_200_OK)
		except Exception:
			# En cas de problème, on retombe sur le comportement standard
			pass

		# Comportement standard: création + auto-image dans perform_create
		return super().create(request, *args, **kwargs)

	def perform_create(self, serializer):
		instance = serializer.save()
		if not instance.image and instance.name:
			image_path = find_image_for_product_name(instance.name)
			if image_path:
				with open(image_path, "rb") as f:
					instance.image.save(os.path.basename(image_path), File(f), save=True)

class ProductViewSet(viewsets.ModelViewSet):
	authentication_classes = SessionAuthentication, JWTAuthentication
	permission_classes = IsAuthenticated,
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	ordering = ['-created_at']
	filter_backends = [filters.DjangoFilterBackend, ]
	filterset_fields = {
		'shop': ['exact'],
		'name': ['icontains'],
		'product__name': ['icontains'],
		'product__sub_category': ['exact'],
		'updated_at': ['gte', 'lte'],
		'id': ['gt'],
	}


	def list(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())
		
		# Calcul des agrégats pour éviter au front de tout recalculer
		# Valeur de vente totale : somme(quantité * prix_vente)
		# Valeur d'achat totale : somme(quantité * prix_achat)
		stats = queryset.aggregate(
			total_value=Sum(F('quantity') * F('sale_price'), output_field=FloatField()),
			total_cost=Sum(F('quantity') * F('buy_price'), output_field=FloatField()),
			total_quantity=Sum('quantity')
		)

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			resp = self.get_paginated_response(serializer.data)
			resp.data['totals'] = {
				'market_value': stats['total_value'] or 0,
				'cost_value': stats['total_cost'] or 0,
				'quantity': stats['total_quantity'] or 0
			}
			return resp

		serializer = self.get_serializer(queryset, many=True)
		return Response({
			'results': serializer.data,
			'totals': {
				'market_value': stats['total_value'] or 0,
				'cost_value': stats['total_cost'] or 0,
				'quantity': stats['total_quantity'] or 0
			}
		})
	def get_serializer_context(self):
		context = super().get_serializer_context()
		# On met en cache toutes les fréquences de contrôle pour éviter le problème N+1
		# dans le ProductSerializer.
		context['frequency_cache'] = {
			f.shop_id: f for f in ControlFrequency.objects.all()
		}
		return context

	def get_serializer_class(self):
		if self.action == "create":
			return ProductCreateSerializer
		return ProductSerializer

	@transaction.atomic()
	def create(self, request):
		# Si le produit est déjà dans la boutique (même shop, product, sale_price), retourner 200 avec l'existant pour éviter 400
		try:
			shop_id = request.data.get("shop")
			product_id = request.data.get("product")
			sale_price = float(request.data.get("sale_price", 0))
			if shop_id is not None and product_id is not None:
				existing = Product.objects.filter(
					shop_id=shop_id, product_id=product_id, sale_price=sale_price
				).select_related("shop", "product").first()
				if existing:
					return Response(
						ProductSerializer(existing).data,
						status=status.HTTP_200_OK
					)
		except (TypeError, ValueError):
			pass
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		shop:Shop = serializer.validated_data.get("shop")
		if not shop.is_active:
			return Response({"details":"Imangazini yanyu  ntiremererwa gukora"}, status=status.HTTP_400_BAD_REQUEST)
		if not shop.owner.is_active:
			return Response({"details":"Konte yanyu ntiremererwa gukora"}, status=status.HTTP_400_BAD_REQUEST)
		basic_product = serializer.validated_data.get("product")
		sale_price = serializer.validated_data.get("sale_price", 0)
		product = Product(
			shop=serializer.validated_data.get("shop"),
			product=basic_product,
			name=basic_product.name,
			quantity=serializer.validated_data.get("quantity"),
			sale_price=sale_price,
			buy_price=serializer.validated_data.get("buy_price"),
			last_control_at=None
		)

		product.save()
		supply = Supply(
			user=request.user,
			product = product,
			quantity = serializer.validated_data.get("quantity"),
			total_buy_price = serializer.validated_data.get("quantity")*serializer.validated_data.get("buy_price")
		)
		# Gestion de l'historique de la date pour le nouvel ajout
		from api.shops.utils import safe_parse_datetime
		raw_created_at = request.data.get("created_at")
		created_at = safe_parse_datetime(raw_created_at) or timezone.now()

		supply.created_at = created_at
		supply.save()

		# sub_category peut être None (BasicProduct.sub_category est null=True)
		sub_cat = basic_product.sub_category
		category_name = sub_cat.category.name if sub_cat else None
		sub_category_name = sub_cat.name if sub_cat else None
		# History attend IntegerField pour unity_price et total_price
		unity = product.buy_price
		total = supply.total_buy_price
		History.objects.create(
			shop_name=product.shop.name,
			shop_owner=product.shop.owner.user.username,
			shop_id=product.shop.id,

			province=product.shop.province,
			commune=product.shop.commune,
			quarter=product.shop.quarter,
			address=product.shop.address,
			longitude=product.shop.longitude,
			latitude=product.shop.latitude,

			action="Achat",
			category=category_name,
			sub_category=sub_category_name,
			product_name=product.name or basic_product.name,
			product_id=product.id,
			quantity=serializer.validated_data.get("quantity"),

			unity_price=int(unity) if unity is not None else None,
			total_price=int(total) if total is not None else None,
			created_at=created_at
		)

		serializer = ProductSerializer(product).data
		return Response(serializer, status=status.HTTP_201_CREATED)
	

	@transaction.atomic()
	@csrf_exempt
	@action(
		methods=['POST'],
		detail=True,
		url_name=r'control',
		url_path=r"control",
		permission_classes=[IsAuthenticated],
		serializer_class=ControlProductSerializer)
	def controlProduct(self, request, pk):
		serializer = ControlProductSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		product = self.get_object()

		quantity = int(serializer.validated_data["quantity"])

		control_frequency = ControlFrequency.objects.filter(shop=product.shop)
		if not control_frequency.exists():
			return Response(
				{"details": "Veuillez d'abord ajouter la fréquence de contrôle"},
				status=status.HTTP_400_BAD_REQUEST,
			)

		if quantity < 0:
			return Response(
				{"details": "La quantité restante ne peut pas être négative."},
				status=status.HTTP_400_BAD_REQUEST,
			)
		# Toujours mettre à jour la date de contrôle
		from django.utils import timezone
		now_time = timezone.now()
		
		# On récupère l'objet frais pour garantir l'enregistrement
		product_to_update = Product.objects.get(pk=product.id)
		old_qty = product_to_update.quantity
		
		product_to_update.last_control_at = now_time
		product_to_update.quantity = quantity
		product_to_update.save()

		if quantity < old_qty:
			qt_vendu = old_qty - quantity
			sale_price = float(product_to_update.sale_price) if product_to_update.sale_price is not None else 0.0
			amount = sale_price * qt_vendu

			Sales.objects.create(
				user=request.user,
				product=product_to_update,
				quantity=qt_vendu,
				buy_price=float(product_to_update.buy_price),
				amount=amount
			)
			
			History.objects.create(
				shop_name=product_to_update.shop.name,
				shop_owner=product_to_update.shop.owner.user.username,
				shop_id=product_to_update.shop.id,
				action="Vente (Contrôle)",
				product_name=product_to_update.name,
				product_id=product_to_update.id,
				quantity=qt_vendu,
				unity_price=int(sale_price),
				total_price=int(amount)
			)

		elif quantity > old_qty:
			qt_ajout = quantity - old_qty
			buy_price = float(product_to_update.buy_price) if product_to_update.buy_price is not None else 0.0
			total_buy_price = buy_price * qt_ajout

			Supply.objects.create(
				user=request.user,
				product=product_to_update,
				quantity=qt_ajout,
				total_buy_price=total_buy_price
			)

			History.objects.create(
				shop_name=product_to_update.shop.name,
				shop_owner=product_to_update.shop.owner.user.username,
				shop_id=product_to_update.shop.id,
				action="Achat (Contrôle)",
				product_name=product_to_update.name,
				product_id=product_to_update.id,
				quantity=qt_ajout,
				unity_price=int(buy_price),
				total_price=int(total_buy_price)
			)
		
		return Response({"status":"Contrôle terminé avec succès"}, status=status.HTTP_200_OK)
	


	@transaction.atomic()
	@csrf_exempt
	@action(
		methods=['POST'],
		detail=True,
		url_name=r'supply',
		url_path=r"supply",
		permission_classes=[IsAuthenticated],
		serializer_class=SupplyProductSerializer)
	def supplyProduct(self, request, pk):
		serializer = SupplyProductSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		product:Product = self.get_object()
		quantity = serializer.validated_data.get("quantity")
		total_buy_price = serializer.validated_data.get("total_buy_price")
		from api.shops.utils import safe_parse_datetime
		from django.utils import timezone
		
		raw_created_at = request.data.get("created_at")
		created_at = safe_parse_datetime(raw_created_at) or timezone.now()

		product.quantity += quantity
		
		# Mise à jour du prix d'achat
		product.buy_price = round(total_buy_price/quantity)
		
		# Mise à jour du prix de vente si fourni (nouveau besoin utilisateur)
		sale_price = request.data.get('sale_price')
		if sale_price and float(sale_price) > 0:
			new_sale_price = float(sale_price)
			if product.sale_price != new_sale_price:
				SalePriceHistory.objects.create(
					product=product,
					old_price=product.sale_price,
					new_price=new_sale_price,
					user=request.user
				)
				product.sale_price = new_sale_price

		product.save()
				
		supply = Supply(
			user=request.user,
			product = product,
			quantity = quantity,
			total_buy_price = total_buy_price,
			created_at=created_at
		)
		supply.save()

		sub_cat = product.product.sub_category if product.product else None
		category_name = sub_cat.category.name if sub_cat and sub_cat.category else None
		sub_category_name = sub_cat.name if sub_cat else None
		unity = round(total_buy_price / quantity)
		total_int = int(round(total_buy_price))

		History.objects.create(
			shop_name=product.shop.name,
			shop_owner=product.shop.owner.user.username,
			shop_id=product.shop.id,

			province=product.shop.province,
			commune=product.shop.commune,
			quarter=product.shop.quarter,
			address=product.shop.address,
			longitude=product.shop.longitude,
			latitude=product.shop.latitude,

			action="Achat",
			category=category_name,
			sub_category=sub_category_name,
			product_name=product.name or (product.product.name if product.product else ""),
			product_id=product.id,
			quantity=quantity,

			unity_price=unity,
			total_price=total_int,
			created_at=created_at
		)

		return Response({"status":"Wahejeje kurangura"}, status=status.HTTP_200_OK)
	

	@transaction.atomic()
	@csrf_exempt
	@action(
		methods=['GET'],
		detail=True,
		url_name=r'stock',
		url_path=r"stock",
		permission_classes=[IsAuthenticated])
	def stockProduct(self, request, pk):
		product = self.get_object()

		stocks = Supply.objects.filter(product=product)

		serializer = SupplySerializer(stocks, many=True)
	
		return Response(serializer.data, status=status.HTTP_200_OK)


	@transaction.atomic()
	@csrf_exempt
	@action(
		methods=['POST'],
		detail=True,
		url_name=r'change-sale-price',
		url_path=r"change-sale-price",
		permission_classes=[IsAuthenticated])
	def changeSalePrice(self, request, pk):
		print(request.data)
		product = self.get_object()
		new_price = request.data['new_price']
		new_buy_price = request.data['new_buy_price']
		if(new_price!=product.sale_price):
			SalePriceHistory.objects.create(
				user=request.user,
				product=product,
				old_price=product.sale_price,
				new_price=new_price,
			)
			product.sale_price=new_price

		if(new_buy_price!=product.buy_price):
			product.buy_price=new_buy_price
			supply = Supply.objects.filter(
				product=product,
				created_at__date=product.created_at
			)
			if(supply.exists()):
				supply = supply[0]
				supply.total_buy_price=supply.quantity*new_buy_price
				supply.save()

		product.save()
		return Response(status=status.HTTP_200_OK)

	@transaction.atomic()
	@csrf_exempt
	@action(
		methods=['POST'],
		detail=True,
		url_name=r'cancel-control',
		url_path=r"cancel-control",
		permission_classes=[IsAuthenticated])
	def cancel_control(self, request, pk):
		product = self.get_object()
		
		# On réinitialise la date pour qu'il réapparaisse dans "Non contrôlés"
		product.last_control_at = None
		
		# On cherche la dernière action historique de type "Contrôle" pour ce produit
		last_history = History.objects.filter(
			product_id=product.id,
			action__icontains="Contrôle"
		).order_by('-created_at').first()
		
		if last_history:
			if "Vente" in last_history.action:
				# Restauration du stock (on rajoute la quantité vendue)
				product.quantity += last_history.quantity
				# Suppression de la vente correspondante
				last_sale = Sales.objects.filter(
					product=product,
					quantity=last_history.quantity
				).order_by('-created_at').first()
				if last_sale:
					last_sale.delete()
					
			elif "Achat" in last_history.action:
				# Restauration du stock (on retire la quantité achetée)
				product.quantity -= last_history.quantity
				# Suppression de l'approvisionnement (Supply) correspondant
				last_supply = Supply.objects.filter(
					product=product,
					quantity=last_history.quantity
				).order_by('-created_at').first()
				if last_supply:
					last_supply.delete()
			
			# Suppression de l'entrée d'historique
			last_history.delete()

		product.save()
		return Response({"status": "Kontrole yasubijwe inyuma"}, status=status.HTTP_200_OK)
	
class CategoryViewSet(viewsets.ModelViewSet):
	authentication_classes = SessionAuthentication, JWTAuthentication
	permission_classes = IsAuthenticated,
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	ordering = ['name']
	filter_backends = [filters.DjangoFilterBackend, ]
	filterset_fields = {
		'name': ['contains'],
		'id': ['gt'],
	}

class SubCategoryViewSet(viewsets.ModelViewSet):
	authentication_classes = SessionAuthentication, JWTAuthentication
	permission_classes = IsAuthenticated,
	queryset = SubCategory.objects.all()
	serializer_class = SubCategorySerializer
	ordering = ['category', 'name']
	filter_backends = [filters.DjangoFilterBackend, ]
	filterset_fields = {
		'category': ['exact'],
		'updated_at': ['gte', 'lte'],
		'id': ['gt'],
	}