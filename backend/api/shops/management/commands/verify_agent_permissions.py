from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from api.shops.models import Shop
from api.accounts.models import Account
from django.utils import timezone
import time

class Command(BaseCommand):
    help = 'Verify Agent Permissions for Shop Management'

    def handle(self, *args, **options):
        from django.conf import settings
        if 'testserver' not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS += ['testserver']

        self.stdout.write("Starting Agent Permission Verification...")
        
        # Setup
        timestamp = int(time.time())
        agent_username = f"test_agent_{timestamp}"
        admin_username = f"test_admin_{timestamp}"
        password = "password123"

        # Create Groups if not exists
        agent_group, _ = Group.objects.get_or_create(name='agent')

        # Create Agent
        agent_user = User.objects.create_user(username=agent_username, password=password)
        agent_user.groups.add(agent_group)
        # Create Account for Agent
        if not hasattr(agent_user, 'account'):
             Account.objects.create(user=agent_user, phone_number=f"77{timestamp}")
        
        # Create Superuser (Admin)
        admin_user = User.objects.create_superuser(username=admin_username, password=password, email="admin@test.com")
        
        client = APIClient()

        # 1. Test Agent Creation -> Should be FREE by default
        self.stdout.write(f"Testing Shop Creation as Agent {agent_username}...")
        client.force_authenticate(user=agent_user)
        response = client.post('/api/shops/shops/', {
            "name": f"Shop Agent {timestamp}",
            "owner": agent_user.account.id, # Agent owns it for simplicity
            "province": "Bujumbura",
            "commune": "Mukaza",
            "quarter": "Rohero",
            "address": "Avenue de la Revolution"
        })
        
        shop_id = None
        if response.status_code == 201:
            shop_data = response.data
            if shop_data.get('subscription_plan') == 'FREE':
                self.stdout.write(self.style.SUCCESS("PASS: Agent created shop and it is FREE."))
                shop_id = shop_data['id']
            else:
                self.stdout.write(self.style.ERROR(f"FAIL: Shop created with plan {shop_data.get('subscription_plan')}"))
        else:
            self.stdout.write(self.style.ERROR(f"FAIL: Agent failed to create shop. {response.content}"))
            return # Cannot proceed

        # 2. Test Agent Update to MONTHLY -> Should Fail
        self.stdout.write(f"Testing Shop Update to MONTHLY as Agent on Shop {shop_id}...")
        response = client.patch(f'/api/shops/shops/{shop_id}/', {
            "subscription_plan": "MONTHLY"
        })
        
        if response.status_code == 403:
            self.stdout.write(self.style.SUCCESS("PASS: Agent update to MONTHLY forbidden (403)."))
        else:
            self.stdout.write(self.style.ERROR(f"FAIL: Agent update to MONTHLY returned {response.status_code}. Content: {response.content}"))

        # 3. Test Agent Activate Subscription to FREE -> Should Success
        self.stdout.write("Testing Agent Activate Subscription (FREE)...")
        response = client.post(f'/api/shops/shops/{shop_id}/activate_subscription/', {
            "plan": "FREE",
            "duration_months": 1
        })
        
        if response.status_code == 200:
             self.stdout.write(self.style.SUCCESS("PASS: Agent activated FREE subscription."))
        else:
             self.stdout.write(self.style.ERROR(f"FAIL: Agent failed to activate FREE. {response.status_code} - {response.content}"))

        # 4. Test Agent Activate Subscription to MONTHLY -> Should Fail
        self.stdout.write("Testing Agent Activate Subscription (MONTHLY)...")
        response = client.post(f'/api/shops/shops/{shop_id}/activate_subscription/', {
            "plan": "MONTHLY"
        })
        
        if response.status_code == 403:
             self.stdout.write(self.style.SUCCESS("PASS: Agent failed to activate MONTHLY (403)."))
        else:
             self.stdout.write(self.style.ERROR(f"FAIL: Agent activating MONTHLY returned {response.status_code}. Content: {response.content}"))

        # 5. Cleanup
        try:
            agent_user.delete()
            admin_user.delete()
            # Shop should be deleted via cascade from owner (agent_user.account)
            self.stdout.write("Cleanup successful.")
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Cleanup failed: {e}"))
