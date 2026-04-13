from django.db import models
from django.contrib.auth.models import User

SEXES = (
    ("H", "HOMME"),
    ("F", "FEMME"),
    ("N/A", "NON APPLICABLE")
)

class Role(models.Model):
    """Rôles utilisateurs (Admin, Gérant, Vendeur, etc.)"""
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.JSONField(default=dict, blank=True)  # Permissions spécifiques au rôle
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"
        ordering = ['name']


class Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='accounts')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_accounts', help_text="Agent ou admin qui a créé cet utilisateur")
    
    # Le numéro de téléphone n'est plus unique pour permettre la réutilisation
    # du même numéro sur plusieurs comptes. La validation d'unicité est gérée
    # uniquement côté email/username.
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    otp_code = models.CharField(max_length=5, editable=False, null=True)
    otp_expire_at = models.DateTimeField(blank=True, null=True)   
    email_validated = models.BooleanField(default=False)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"

    def complete(self):
        return (
            bool(self.phone_number) and
            bool(self.email_validated)
        )


class Subscription(models.Model):
    """Abonnements des utilisateurs/boutiques"""
    SUBSCRIPTION_TYPES = (
        ('FREE', 'Gratuit'),
        ('BASIC', 'Basique'),
        ('PREMIUM', 'Premium'),
        ('ENTERPRISE', 'Entreprise'),
    )
    
    STATUS_CHOICES = (
        ('ACTIVE', 'Actif'),
        ('EXPIRED', 'Expiré'),
        ('CANCELLED', 'Annulé'),
        ('PENDING', 'En attente'),
    )
    
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='subscriptions')
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES, default='FREE')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    features = models.JSONField(default=dict, blank=True)  # Fonctionnalités incluses
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.account.user.username} - {self.get_subscription_type_display()}"
    
    @property
    def is_active(self):
        from django.utils import timezone
        return self.status == 'ACTIVE' and (self.end_date is None or self.end_date > timezone.now())
    
    class Meta:
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
        ordering = ['-created_at']


class Notification(models.Model):
    """Notifications pour les utilisateurs"""
    NOTIFICATION_TYPES = (
        ('INFO', 'Information'),
        ('WARNING', 'Avertissement'),
        ('ERROR', 'Erreur'),
        ('SUCCESS', 'Succès'),
        ('SYSTEM', 'Système'),
    )
    
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='INFO')
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    
    # Liens optionnels
    link_url = models.URLField(blank=True, null=True)
    related_object_type = models.CharField(max_length=50, blank=True, null=True)  # 'shop', 'product', etc.
    related_object_id = models.IntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.account.user.username} - {self.title}"
    
    def mark_as_read(self):
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save()
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['account', 'is_read', '-created_at']),
        ]
