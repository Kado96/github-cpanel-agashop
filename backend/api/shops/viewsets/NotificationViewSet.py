import uuid
from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.shops.models import Shop, ControlNotification, LumiCashTransaction
from api.shops.serializers.NotificationSerializer import ControlNotificationSerializer, LumiCashTransactionSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour consulter et gérer les notifications post-contrôle.
    """
    serializer_class = ControlNotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ControlNotification.objects.all()
        # Si c'est un propriétaire ou agent
        return ControlNotification.objects.filter(shop__owner__user=user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marquée comme lue'})

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        queryset = self.get_queryset().filter(is_read=False)
        count = queryset.update(is_read=True)
        return Response({'status': f'{count} notifications marquées comme lues'})


class LumiCashPaymentViewSet(viewsets.ViewSet):
    """
    ViewSet pour la gestion des paiements d'abonnement AgaShop via LumiCash.
    """

    PLAN_PRICES = {
        'MONTHLY': 15000.00,   # 15,000 BIF
        '3MONTHS': 40000.00,   # 40,000 BIF
        '6MONTHS': 75000.00,   # 75,000 BIF
        'YEARLY': 140000.00,   # 140,000 BIF
    }

    PLAN_DAYS = {
        'MONTHLY': 30,
        '3MONTHS': 90,
        '6MONTHS': 180,
        'YEARLY': 365,
    }

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def initiate(self, request):
        """
        Inicie une demande de paiement LumiCash pour un plan d'abonnement.
        """
        shop_id = request.data.get('shop_id')
        plan = request.data.get('plan')
        phone_number = request.data.get('phone_number')

        if not shop_id or not plan or not phone_number:
            return Response({'error': 'shop_id, plan et phone_number sont obligatoires.'}, status=status.HTTP_400_BAD_REQUEST)

        if plan not in self.PLAN_PRICES:
            return Response({'error': f'Plan invalide. Choix: {list(self.PLAN_PRICES.keys())}'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            shop = Shop.objects.get(id=shop_id)
        except Shop.DoesNotExist:
            return Response({'error': 'Boutique introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        reference_id = f"AGASHOP-{uuid.uuid4().hex[:8].upper()}"
        amount = self.PLAN_PRICES[plan]

        tx = LumiCashTransaction.objects.create(
            shop=shop,
            phone_number=phone_number,
            amount=amount,
            plan=plan,
            reference_id=reference_id,
            status='PENDING'
        )

        # Création d'une notification d'initiation
        ControlNotification.objects.create(
            shop=shop,
            notification_type='SYSTEM',
            title="Paiement LumiCash Initié",
            message=f"Paiement de {amount:,.0f} BIF initié via {phone_number} pour le plan {plan}. Référence: {reference_id}."
        )

        return Response({
            'message': 'Demande de paiement LumiCash créée avec succès.',
            'reference_id': reference_id,
            'amount': amount,
            'plan': plan,
            'status': tx.status,
            'instruction': f"Validez l'invite USSD reçue sur votre téléphone {phone_number} pour valider le paiement."
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def callback(self, request):
        """
        Callback/Webhook appelé par la passerelle LumiCash après validation USSD.
        """
        reference_id = request.data.get('reference_id')
        lumicash_tx_id = request.data.get('lumicash_tx_id')
        status_code = request.data.get('status') # 'SUCCESS' ou 'FAILED'

        if not reference_id:
            return Response({'error': 'reference_id requis.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tx = LumiCashTransaction.objects.get(reference_id=reference_id)
        except LumiCashTransaction.DoesNotExist:
            return Response({'error': 'Transaction introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        if status_code == 'SUCCESS':
            tx.status = 'SUCCESS'
            tx.lumicash_tx_id = lumicash_tx_id
            tx.save()

            # Activation de l'abonnement de la boutique
            shop = tx.shop
            shop.subscription_plan = tx.plan
            shop.is_active = True
            
            # Calcul de la nouvelle date d'expiration
            days_to_add = self.PLAN_DAYS.get(tx.plan, 30)
            now = timezone.now()
            if shop.trial_end_date and shop.trial_end_date > now:
                shop.trial_end_date = shop.trial_end_date + timedelta(days=days_to_add)
            else:
                shop.trial_end_date = now + timedelta(days=days_to_add)
            
            shop.save()

            # Calcul et attribution de la commission à l'agent qui gère la boutique
            if shop.agent:
                from decimal import Decimal
                rate_percentage = Decimal('10.00')  # 10% de commission par défaut sur les abonnements amenés par l'agent
                commission_amount = (Decimal(str(tx.amount)) * rate_percentage) / Decimal('100')
                from api.shops.models import Commission
                Commission.objects.create(
                    shop=shop,
                    account=shop.agent,
                    commission_type='PERCENTAGE',
                    rate=rate_percentage,
                    amount=commission_amount,
                    status='PENDING',
                    notes=f"Commission 10% sur souscription {tx.get_plan_display()} via LumiCash ({tx.amount} BIF)"
                )
                ControlNotification.objects.create(
                    shop=shop,
                    notification_type='SYSTEM',
                    title="💰 Commission Agent Générée",
                    message=f"Une commission de {commission_amount:,.0f} BIF a été attribuée à l'agent {shop.agent}."
                )


            # Émission de la notification post-contrôle / post-paiement
            ControlNotification.objects.create(
                shop=shop,
                notification_type='SUBSCRIPTION_ACTIVATED',
                title="🎉 Abonnement LumiCash Activé !",
                message=f"Votre abonnement {tx.get_plan_display()} a été activé avec succès via LumiCash ({tx.amount:,.0f} BIF). Date d'expiration: {shop.trial_end_date.strftime('%d/%m/%Y')}."
            )

            return Response({'status': 'Abonnement activé avec succès.'})

        else:
            tx.status = 'FAILED'
            tx.save()
            ControlNotification.objects.create(
                shop=tx.shop,
                notification_type='WARNING',
                title="❌ Échec du Paiement LumiCash",
                message=f"La transaction LumiCash (Réf: {reference_id}) a échoué ou a été annulée."
            )
            return Response({'status': 'Paiement marqué comme échoué.'})
