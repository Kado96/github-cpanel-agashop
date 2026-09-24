import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from api.shops.models import ControlNotification

logger = logging.getLogger(__name__)

@receiver(post_save, sender=ControlNotification)
def send_notification_email_on_creation(sender, instance, created, **kwargs):
    """
    Envoie automatiquement un email à l'utilisateur propriétaire de la boutique
    (et à l'agent le cas échéant) dès qu'une notification de contrôle ou d'application est générée.
    """
    if not created:
        return

    try:
        shop = instance.shop
        owner = shop.owner.user if shop and hasattr(shop, 'owner') and shop.owner else None

        recipients = []
        if owner and owner.email:
            recipients.append(owner.email)

        # Si un agent suit la boutique, l'inclure aussi
        if shop.agent and hasattr(shop.agent, 'user') and shop.agent.user.email:
            if shop.agent.user.email not in recipients:
                recipients.append(shop.agent.user.email)

        if not recipients:
            logger.info(f"[EMAIL SIGNAL] Aucun destinataire email trouvé pour la boutique {shop.name}.")
            return

        subject = f"[AgaShop] {instance.title}"
        plain_body = f"Bonjour,\n\nNotification concernant votre boutique '{shop.name}' :\n\n{instance.title}\n\n{instance.message}\n\nCordialement,\nL'équipe AgaShop"

        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
              <div style="background-color: #FD7100; padding: 15px; text-align: center; border-radius: 6px 6px 0 0;">
                <h2 style="color: #ffffff; margin: 0;">AGASHOP</h2>
              </div>
              <div style="padding: 20px;">
                <h3 style="color: #FD7100;">{instance.title}</h3>
                <p><strong>Boutique :</strong> {shop.name}</p>
                <p>{instance.message}</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;" />
                <p style="font-size: 0.85em; color: #777;">Cet email automatique a été généré par l'application AgaShop.</p>
              </div>
            </div>
          </body>
        </html>
        """

        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_body,
            from_email=None,
            to=recipients
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=True)
        logger.info(f"[EMAIL SIGNAL] Notification par email envoyée à {recipients} pour {shop.name}.")

    except Exception as e:
        logger.error(f"[EMAIL SIGNAL ERROR] Échec de l'envoi d'email pour la notification #{instance.id}: {str(e)}")
