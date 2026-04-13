from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.accounts'
    
    def ready(self):
        """Charger les signals lors du démarrage de l'application"""
        import api.accounts.signals