import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agashop.settings')
django.setup()

from django.contrib.auth.models import User, Group
from api.accounts.models import Account
from api.shops.models import Shop

def check_user(username):
    try:
        user = User.objects.get(username=username)
        print(f"User: {user.username} (ID: {user.id})")
        print(f"  Groups: {[g.name for g in user.groups.all()]}")
        print(f"  Is Staff: {user.is_staff}")
        print(f"  Is Superuser: {user.is_superuser}")
        
        try:
            account = Account.objects.get(user=user)
            print(f"  Account ID: {account.id}")
            print(f"  Account Active: {account.is_active}")
            print(f"  Created By: {account.created_by}")
        except Account.DoesNotExist:
            print("  Account: DOES NOT EXIST")
            
        # Shops where user is owner
        owned_shops = Shop.objects.filter(owner__user=user)
        print(f"  Owned Shops: {[(s.name, s.is_active, s.trial_end_date) for s in owned_shops]}")
        
        # Shops where user is agent
        managed_shops = Shop.objects.filter(agent__user=user)
        print(f"  Managed Shops: {[(s.name, s.is_active, s.trial_end_date) for s in managed_shops]}")
        
        # Shops for accounts created by this user
        created_accounts_shops = Shop.objects.filter(owner__created_by=user)
        print(f"  Shops of Created Users: {[s.name for s in created_accounts_shops]}")
        
    except User.DoesNotExist:
        print(f"User {username} NOT FOUND")

print("--- DONALD ---")
def check_all_shops():
    print("\n--- ALL SHOPS IN DB ---")
    shops = Shop.objects.all()
    print(f"Total shops: {shops.count()}")
    for s in shops:
        print(f"Shop ID: {s.id}, Name: {s.name}, Active: {s.is_active}")
        print(f"  Owner Account ID: {s.owner_id}")
        print(f"  Owner User: {s.owner.user.username} (ID: {s.owner.user_id})")
        print(f"  Owner Account Created By: {s.owner.created_by}")
        print(f"  Agent Account ID: {s.agent_id}")
        if s.agent:
            print(f"  Agent User: {s.agent.user.username} (ID: {s.agent.user_id})")

check_user('donald')
check_user('fanuel')
check_all_shops()
