from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.accounts.models import Account, User
from api.shops.models import Shop, ControlNotification, LumiCashTransaction, Commission


class LumiCashNotificationTestCase(TestCase):
    def setUp(self):
        self.agent_user = User.objects.create_user(username='agentuser', password='password123')
        self.agent_account = Account.objects.create(user=self.agent_user, phone_number='+25769000000')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.account = Account.objects.create(user=self.user, phone_number='+25761000000')
        self.shop = Shop.objects.create(owner=self.account, agent=self.agent_account, name='Boutique Test')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_lumicash_initiate_and_callback(self):
        # 1. Initiations
        response = self.client.post('/api/shops/lumicash/initiate/', {
            'shop_id': self.shop.id,
            'plan': 'MONTHLY',
            'phone_number': '+25761000000'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reference_id = response.data['reference_id']

        # Vérification création notification initiation
        self.assertTrue(ControlNotification.objects.filter(shop=self.shop, notification_type='SYSTEM').exists())

        # 2. Callback de succès LumiCash
        callback_resp = self.client.post('/api/shops/lumicash/callback/', {
            'reference_id': reference_id,
            'lumicash_tx_id': 'LUMI-TX-998877',
            'status': 'SUCCESS'
        })
        self.assertEqual(callback_resp.status_code, status.HTTP_200_OK)

        # Vérification mise à jour boutique
        self.shop.refresh_from_db()
        self.assertEqual(self.shop.subscription_plan, 'MONTHLY')
        self.assertTrue(self.shop.is_active)

        # Vérification création commission agent (10% de 15000 = 1500 BIF)
        commission = Commission.objects.filter(shop=self.shop, account=self.agent_account).first()
        self.assertIsNotNone(commission)
        self.assertEqual(float(commission.amount), 1500.0)

        # Vérification notification d'activation
        self.assertTrue(ControlNotification.objects.filter(shop=self.shop, notification_type='SUBSCRIPTION_ACTIVATED').exists())

