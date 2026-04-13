from django.core.mail import send_mail, EmailMultiAlternatives  # type: ignore[reportMissingImports]
from django.template.loader import render_to_string  # type: ignore[reportMissingImports]
from django.utils.html import strip_tags  # type: ignore[reportMissingImports]

def send_custom_email(mail_data, template):
    # Définir un contexte par défaut pour éviter les variables non liées
    context: dict = {}

    # Charger le template et le rendre avec le contexte
    if template == "reset_password.html":
        context = {
            "password": mail_data["password"],
        }
    elif template == "account_creation_otp.html":
        context = {
            "otp": mail_data["otp"],
        }
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    to = mail_data['email']

    # Envoi du mail avec encodage explicite UTF-8
    subject = 'AGASHOP'
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=None,
        to=to,
    )
    email.encoding = 'utf-8'
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)
