from django.core.management.base import BaseCommand
from django.utils import timezone
from api.shops.models import Shop

class Command(BaseCommand):
    help = 'Check and deactivate expired shop subscriptions'

    def handle(self, *args, **kwargs):
        self.stdout.write('Checking shop subscriptions...')
        
        now = timezone.now()
        
        # Trouver les boutiques actives dont la date d\'essai/abonnement est dépassée
        expired_shops = Shop.objects.filter(
            is_active=True,
            trial_end_date__lt=now
        )
        
        count = expired_shops.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No expired shops found.'))
            return
            
        self.stdout.write(f'Found {count} expired shops. Deactivating...')
        
        for shop in expired_shops:
            self.stdout.write(f'Deactivating shop: {shop.name} (Trial ended: {shop.trial_end_date})')
            shop.is_active = False
            shop.save()
            
        self.stdout.write(self.style.SUCCESS(f'Successfully deactivated {count} shops.'))
