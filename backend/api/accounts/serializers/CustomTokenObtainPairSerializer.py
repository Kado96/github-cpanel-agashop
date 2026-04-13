from .dependencies import *
from .AccountSerializer import BasicAccountSerializer
from api.tools import *
from random import randrange
from datetime import timedelta
import random
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import authenticate
from api.shops.serializers import ShopSerializer
from api.shops.models import Shop

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def generateOTP(account:Account):
        if not (account.otp_code and account.otp_expire_at and account.otp_expire_at > timezone.now()):
            account.last_otp_asked = timezone.now()
            otp = "%05d"%randrange(1000, 99999)
            account.otp_code = otp
            account.otp_expire_at = timezone.now() + timedelta(minutes=3)
            account.save()

        mail_data = {
			"email":[account.user.username],
			"otp":account.otp_code,
		}
        print(f"[OTP] : {account.otp_code}")
        send_custom_email(mail_data,"account_creation_otp.html")

    def validate(self, attrs):
        # Accepter "username" ou "email" dans la requête, et connexion par email ou nom d'utilisateur
        # Gérer str ou liste (FormData peut envoyer des listes)
        raw_username = attrs.get("username")
        raw_email = attrs.get("email")
        if isinstance(raw_username, list) and raw_username:
            login_id = raw_username[0]
        elif isinstance(raw_username, list):
            login_id = raw_email or ""
        else:
            login_id = raw_username or raw_email or ""
        if isinstance(login_id, str):
            login_id = login_id.strip()
        else:
            login_id = str(login_id or "").strip()
        password = attrs.get("password")
        if isinstance(password, list):
            password = password[0] if password else ""
        password = password or ""
        
        # Vérifier d'abord si l'utilisateur existe (actif ou non) pour donner un message d'erreur plus précis
        if login_id:
            # Chercher tous les utilisateurs correspondants (actifs et inactifs)
            all_users = User.objects.filter(
                Q(email__iexact=login_id) | Q(username__iexact=login_id)
            ).distinct()
            
            # Chercher uniquement les utilisateurs actifs
            active_candidates = [u for u in all_users if u.is_active]
            
            # Si aucun utilisateur n'existe avec cet email/username
            if not all_users.exists():
                from rest_framework_simplejwt.exceptions import AuthenticationFailed
                raise AuthenticationFailed(
                    "Aucun compte trouvé avec cet email ou nom d'utilisateur. Vérifiez vos identifiants ou créez un nouveau compte.",
                    code='no_such_user'
                )
            
            # Si l'utilisateur existe mais est inactif
            if not active_candidates:
                from rest_framework_simplejwt.exceptions import AuthenticationFailed
                raise AuthenticationFailed(
                    "Ce compte est désactivé. Contactez l'administrateur pour réactiver votre compte.",
                    code='user_inactive'
                )
            
            # Essayer d'authentifier avec les utilisateurs actifs
            authenticated_user = None
            for u in active_candidates:
                if authenticate(username=u.username, password=password):
                    authenticated_user = u
                    attrs = dict(attrs)
                    attrs["username"] = u.username
                    attrs["password"] = password
                    break
            
            # Si aucun utilisateur n'a pu être authentifié (mauvais mot de passe)
            if not authenticated_user:
                from rest_framework_simplejwt.exceptions import AuthenticationFailed
                raise AuthenticationFailed(
                    "Mot de passe incorrect. Si vous avez oublié votre mot de passe, utilisez la fonction 'Mot de passe oublié' pour le réinitialiser.",
                    code='invalid_password'
                )
        
        # Si tout va bien, appeler la méthode parente pour générer les tokens
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data['username'] = self.user.username
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['id'] = self.user.id
        
        # Gérer les groupes : d'abord les groupes Django, puis ajouter admin si superuser
        groups = [group.name for group in self.user.groups.all()]
        if self.user.is_superuser:
            groups.append("admin")
        data['groups'] = groups
        print(f"[LOGIN] User: {self.user.username}, Groups: {groups}, is_superuser: {self.user.is_superuser}, is_staff: {self.user.is_staff}")
        
        # Gérer l'Account (peut ne pas exister pour tous les utilisateurs, notamment les superusers)
        # Vérifier si l'Account existe via une requête plutôt que d'accéder directement à la relation
        try:
            account = Account.objects.get(user=self.user)
            if account:
                data['account'] = BasicAccountSerializer(account).data
                # Chercher la boutique associée à cet account
                try:
                    shop = Shop.objects.filter(owner=account).first()
                    if shop:
                        data["shop"] = ShopSerializer(shop, many=False).data
                except Exception as e:
                    # Erreur lors de la récupération de la boutique, ce n'est pas fatal
                    print(f"[LOGIN] Erreur lors de la récupération de la boutique: {e}")
                    pass
        except Account.DoesNotExist:
            # L'utilisateur n'a pas d'Account, ce n'est pas une erreur fatale (normal pour les superusers)
            pass
        except Exception as e:
            # Gérer toute autre erreur de manière gracieuse
            print(f"[LOGIN] Erreur lors de la récupération de l'account: {e}")
            import traceback
            traceback.print_exc()
            pass
        
        return data