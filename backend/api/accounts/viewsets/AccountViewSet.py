from .dependencies import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone
from api.shops.models import Shop
from api.shops.serializers import ShopSerializer
from api.tools import send_custom_email

import random
import string

def generate_password(length=8):
    if length < 4:
        raise ValueError("Password length should be at least 4 characters.")

    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def blacklist_user_tokens(user):
    """
    Blackliste tous les tokens JWT d'un utilisateur.
    Utilise le système de blacklist de rest_framework_simplejwt.
    """
    try:
        # Récupérer tous les tokens en cours pour cet utilisateur
        outstanding_tokens = OutstandingToken.objects.filter(user=user)
        
        # Blacklister chaque token
        for token in outstanding_tokens:
            # Vérifier si le token n'est pas déjà blacklisté
            if not BlacklistedToken.objects.filter(token=token).exists():
                BlacklistedToken.objects.get_or_create(token=token)
        
        return True
    except Exception as e:
        print(f"[TOKEN BLACKLIST ERROR] Erreur lors de la blacklist des tokens: {e}")
        return False


class AccountViewSet(viewsets.ModelViewSet):
	serializer_class = AccountSerializer
	authentication_classes = JWTAuthentication, SessionAuthentication
	permission_classes = [IsAuthenticated]
	ordering = ['-id']
	filter_backends = [filters.DjangoFilterBackend, ]
	filterset_fields = {
		'user': ['exact'],
		'updated_at': ['gte', 'lte'],
		'id': ['gt'],
	}

	def get_queryset(self):
		user = self.request.user
		queryset = Account.objects.select_related("user", "created_by")
		
		# Les superusers voient tous les comptes
		if user.is_superuser:
			return queryset
		
		# Vérifier si l'utilisateur est un agent
		is_agent = user.groups.filter(name='agent').exists() or (hasattr(user, 'account') and user.account and user.is_staff and not user.is_superuser)
		
		if is_agent:
			# Les agents voient uniquement les comptes des utilisateurs qu'ils ont créés
			queryset = queryset.filter(created_by=user)
		else:
			# Pour les autres utilisateurs, ils ne peuvent voir que leur propre compte
			try:
				pk = vars(self.request)["parser_context"]["kwargs"]["pk"]
				return queryset.filter(id=pk)
			except Exception:
				return queryset.filter(user=user)
		
		return queryset

	@transaction.atomic()
	@csrf_exempt
	@action(
		methods=['POST'],
		detail=False,
		url_name=r'verify_otp',
		url_path=r"verify_otp",
		serializer_class=OTPSerializer,
		permission_classes=[IsAuthenticated])
	def verifyOTP(self, request):
		serializer = OTPSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		otp_code = serializer.validated_data["otp_code"]
		account:Account = request.user.account
		if(account.otp_expire_at < timezone.now()):
			return Response({"status":"code OTP expiré"},status=status.HTTP_403_FORBIDDEN)
		if(account.otp_code == otp_code):
			shop = Shop(
				owner=account,
				name=f"Boutique de {account.user.email}",
				is_active=True
			)
			shop.save()

			account.otp_code = ""
			account.otp_expire_at = None
			account.email_validated = True
			account.save()
			refresh = RefreshToken.for_user(request.user)
			
			# Gérer les groupes : d'abord les groupes Django, puis ajouter admin si superuser
			groups = [group.name for group in request.user.groups.all()]
			if request.user.is_superuser:
				groups.append("admin")
			
			session_data = {
				"refresh": str(refresh),
				"access": str(refresh.access_token),
				"complete": False,
				"groups": groups,
				"id": request.user.id,
				"username": request.user.username,
				"account": account.id,
				"first_name": account.user.first_name,
				"last_name": account.user.last_name,
				"shop":ShopSerializer(shop, many=False).data
			}
			return Response(session_data, status=status.HTTP_200_OK)
		return Response({"status":"code OTP incorrect"}, status=status.HTTP_403_FORBIDDEN)

	@csrf_exempt
	@action(
		methods=['GET'],
		detail=False,
		url_name=r'resend_otp',
		url_path=r"resend_otp",
		permission_classes=[IsAuthenticated])
	def resendOTP(self, request):
		account:Account = request.user.account
		CustomTokenObtainPairSerializer.generateOTP(account)
		return Response({"status":"Code envoyé avec success !"}, status=status.HTTP_200_OK)

	@csrf_exempt
	@action(
		methods=['POST'],
		detail=False,
		url_name=r'reset-password',
		url_path=r"reset-password",
		permission_classes=[AllowAny],
		serializer_class=ResetPasswordSerializer)
	def reset_password(self, request):
		serializer = ResetPasswordSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		email = (serializer.validated_data["email"] or "").strip()
		# Recherche par User (email ou username), pour permettre la réinitialisation
		# aux utilisateurs simples, agents ET admins (même sans Account)
		user = User.objects.filter(
			Q(email__iexact=email) | Q(username__iexact=email),
			is_active=True
		).first()
		if not user:
			# Adresse e-mail inconnue pour tout type de compte
			return Response(
				{"status": "Email incorrect", "details": "Aucun compte actif ne correspond à cette adresse e-mail."},
				status=status.HTTP_403_FORBIDDEN,
			)
		else:
			new_password = generate_password(8)
			
			# Blacklister tous les tokens existants AVANT de changer le mot de passe
			blacklist_user_tokens(user)
			
			# Changer le mot de passe
			user.set_password(new_password)
			user.save()

			# Choisir la meilleure adresse email disponible pour l'envoi
			recipient_email = user.email or user.username
			if not recipient_email or "@" not in recipient_email:
				# Message clair en français pour le frontend (ForgotPasswordPage) et pour errorOrRefresh
				return Response(
					{
						"status": "Ce compte n'a pas d'adresse e-mail valide pour l'envoi du mot de passe.",
						"details": "Ce compte n'a pas d'adresse e-mail valide. Contactez l'administrateur pour mettre à jour l'adresse e-mail avant de réinitialiser le mot de passe.",
					},
					status=status.HTTP_400_BAD_REQUEST,
				)

			mail_data = {
				"email": [recipient_email],
				"password": new_password,
			}
			print(f"[PASSWORD RESET] user={user.username} email={recipient_email} new_password={new_password}")
			print(f"[PASSWORD RESET] Les anciens tokens JWT sont maintenant invalides pour cet utilisateur.")

			email_sent = True
			try:
				send_custom_email(mail_data, "reset_password.html")
			except Exception as e:
				# SMTP non disponible (erreur fréquente en prod ou en local)
				print(f"[PASSWORD RESET] ERREUR ENVOI EMAIL: {e}")
				email_sent = False

			if email_sent:
				status_msg = "Mot de passe de réinitialisation envoyé avec succès ! Vérifiez votre boîte mail. Les anciennes sessions sont maintenant invalides."
			else:
				status_msg = (
					"Le mot de passe a été réinitialisé et les anciennes sessions invalidées, "
					"mais l'envoi de l'e-mail a échoué. Contactez l'administrateur pour récupérer le nouveau mot de passe."
				)

			return Response(
				{
					"status": status_msg,
					"email_sent": email_sent,
				},
				status=status.HTTP_200_OK
			)

	@transaction.atomic()
	@csrf_exempt
	@action(
		methods=['POST'],
		detail=True,
		url_name=r'force-reset-password',
		url_path=r"force-reset-password",
		permission_classes=[IsAuthenticated],
	)
	def force_reset_password(self, request, pk=None):
		"""
		Permet à un administrateur ou à un agent de réinitialiser le mot de passe
		d'un utilisateur simple depuis l'application (AGASHOP Admin).
		Un nouveau mot de passe aléatoire est généré, les anciens tokens JWT sont
		invalidés et un e-mail est envoyé à l'utilisateur.
		"""
		account: Account = self.get_object()
		target_user: User = account.user

		# Vérifier les droits de l'utilisateur connecté
		user = request.user
		is_superuser = user.is_superuser
		is_agent = user.groups.filter(name='agent').exists() or (
			hasattr(user, 'account') and user.account and user.is_staff and not user.is_superuser
		)

		if not (is_superuser or is_agent):
			return Response(
				{
					"status": "Action non autorisée.",
					"details": "Seuls les administrateurs et les agents peuvent réinitialiser le mot de passe d'un utilisateur.",
				},
				status=status.HTTP_403_FORBIDDEN,
			)

		# Les agents ne peuvent gérer que les comptes qu'ils ont créés
		if is_agent and not is_superuser and account.created_by_id and account.created_by_id != user.id:
			return Response(
				{
					"status": "Action non autorisée.",
					"details": "Vous ne pouvez réinitialiser le mot de passe que des utilisateurs que vous avez vous‑même créés.",
				},
				status=status.HTTP_403_FORBIDDEN,
			)

		# Générer un nouveau mot de passe et invalider les anciens tokens
		new_password = generate_password(8)
		blacklist_user_tokens(target_user)
		target_user.set_password(new_password)
		target_user.save()

		# Choisir la meilleure adresse email disponible pour l'envoi
		recipient_email = target_user.email or target_user.username
		if not recipient_email or "@" not in recipient_email:
			return Response(
				{
					"status": "Ce compte n'a pas d'adresse e-mail valide pour l'envoi du mot de passe.",
					"details": "Ce compte n'a pas d'adresse e-mail valide. Demandez à l'utilisateur ou à l'administrateur de mettre à jour l'adresse e-mail avant de réinitialiser le mot de passe.",
					"email_sent": False,
				},
				status=status.HTTP_400_BAD_REQUEST,
			)

		mail_data = {
			"email": [recipient_email],
			"password": new_password,
		}

		print(f"[ADMIN PASSWORD RESET] by={user.username} target={target_user.username} email={recipient_email} new_password={new_password}")

		email_sent = True
		try:
			send_custom_email(mail_data, "reset_password.html")
		except Exception as e:
			print(f"[ADMIN PASSWORD RESET] ERREUR ENVOI EMAIL: {e}")
			email_sent = False

		if email_sent:
			status_msg = "Mot de passe réinitialisé et envoyé à l'utilisateur par e-mail. Les anciennes sessions sont maintenant invalides."
		else:
			status_msg = (
				"Le mot de passe a été réinitialisé et les anciennes sessions invalidées, "
				"mais l'envoi de l'e-mail a échoué. Vous devez communiquer ce nouveau mot de passe à l'utilisateur par un autre canal."
			)

		# On renvoie explicitement le nouveau mot de passe dans la réponse API,
		# UNIQUEMENT pour cet endpoint réservé aux admins/agents.
		return Response(
			{
				"status": status_msg,
				"email_sent": email_sent,
				"new_password": new_password,
			},
			status=status.HTTP_200_OK,
		)