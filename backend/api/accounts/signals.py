"""
Signals Django pour intercepter les changements de mot de passe
et blacklister automatiquement les tokens JWT
"""
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

@receiver(pre_save, sender=User)
def blacklist_tokens_on_password_change(sender, instance, **kwargs):
    """
    Signal qui intercepte le changement de mot de passe d'un utilisateur
    et blackliste automatiquement tous ses tokens JWT existants.
    """
    if instance.pk:  # L'utilisateur existe déjà en base
        try:
            old_user = User.objects.get(pk=instance.pk)
            # Vérifier si le mot de passe a changé
            if old_user.password != instance.password:
                # Blacklister tous les tokens de cet utilisateur
                outstanding_tokens = OutstandingToken.objects.filter(user=instance)
                for token in outstanding_tokens:
                    if not BlacklistedToken.objects.filter(token=token).exists():
                        BlacklistedToken.objects.get_or_create(token=token)
        except User.DoesNotExist:
            # L'utilisateur n'existe pas encore, pas de tokens à blacklister
            pass
