from django.db import models
from django.utils import timezone
from api.accounts.models import Account, User


class Shop(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(Account, blank=True, on_delete=models.CASCADE, related_name='owned_shops')
    agent = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name='managed_shops', help_text="Agent qui suit cette boutique")
    name = models.CharField(max_length=100)
    province = models.CharField(max_length=50, null=True ,blank=True)
    commune = models.CharField(max_length=50, null=True ,blank=True)
    quarter = models.CharField(max_length=50, null=True ,blank=True)
    address = models.CharField(max_length=50, null=True ,blank=True)
    is_active = models.BooleanField(default=True)
    payment_mode_active = models.BooleanField(default=True, help_text="Active ou désactive le mode de paiement pour cette boutique.")
    # Mot de passe / code d'accès de la boutique (géré uniquement par les admins/agents)
    shop_password = models.CharField(max_length=50, null=True, blank=True, help_text="Mot de passe de la boutique, modifiable uniquement par les administrateurs et les agents.")

    longitude = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.CharField(max_length=100, null=True, blank=True)

    # Système d'abonnement et essai gratuit
    trial_start_date = models.DateTimeField(null=True, blank=True)
    trial_end_date = models.DateTimeField(null=True, blank=True)
    subscription_plan = models.CharField(max_length=20, default='FREE', choices=[
        ('FREE', 'Essai Gratuit'),
        ('MONTHLY', 'Mensuel'),
        ('3MONTHS', '3 Mois'),
        ('6MONTHS', '6 Mois'),
        ('YEARLY', 'Annuel'),
    ])

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}"

class ControlFrequency(models.Model):
    id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    days = models.PositiveIntegerField(default=0)
    hours = models.PositiveIntegerField(default=0)
    minutes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.days}j - {self.hours}h - {self.minutes}min"
    
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
class SubCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.category.name}  : {self.name}"

class BasicProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    sub_category = models.ForeignKey(SubCategory, null=True, blank=True, on_delete=models.CASCADE)
    image = models.FileField(upload_to="images/", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} "


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(BasicProduct, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    in_unity = models.CharField(max_length=50, null=True, blank=True)
    out_unity = models.CharField(max_length=50, null=True, blank=True)
    rapport = models.IntegerField(default=1, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    sale_price = models.FloatField(default=0)
    buy_price = models.FloatField(default=0)

    last_control_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.product}"

    class Meta:
        unique_together = "shop","product","sale_price"

class SalePriceHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    old_price = models.FloatField(default=0)
    new_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self) -> str:
        return f"{self.product.shop.name} - {self.old_price} -> {self.new_price}"

class Supply(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total_buy_price = models.FloatField(default=0)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f" Achat du {self.created_at} de {self.product.name} - qt : {self.quantity} "


class Sales(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    amount =  models.FloatField(default=0.0)
    buy_price = models.FloatField(default=0.0, help_text="Prix d'achat unitaire au moment de la vente pour le calcul du bénéfice")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f" Vente de {self.product.name} - qt : {self.quantity} montant : {self.amount}"


class Expense(models.Model):
    """Dépenses des boutiques"""
    EXPENSE_TYPES = (
        ('RENT', 'Loyer'),
        ('UTILITIES', 'Services publics (eau, électricité)'),
        ('SALARY', 'Salaires'),
        ('TRANSPORT', 'Transport'),
        ('MARKETING', 'Marketing/Publicité'),
        ('MAINTENANCE', 'Maintenance/Réparation'),
        ('SUPPLIES', 'Fournitures'),
        ('OTHER', 'Autre'),
    )
    
    id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='expenses')
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPES, default='OTHER')
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    expense_date = models.DateField()
    receipt_number = models.CharField(max_length=100, blank=True, null=True)
    receipt_file = models.FileField(upload_to="expenses/receipts/", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.shop.name} - {self.get_expense_type_display()} - {self.amount}"
    
    class Meta:
        verbose_name = "Dépense"
        verbose_name_plural = "Dépenses"
        ordering = ['-expense_date', '-created_at']
        indexes = [
            models.Index(fields=['shop', '-expense_date']),
            models.Index(fields=['expense_type', '-expense_date']),
        ]


class Commission(models.Model):
    """Commissions sur les ventes"""
    COMMISSION_TYPES = (
        ('PERCENTAGE', 'Pourcentage'),
        ('FIXED', 'Montant fixe'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'En attente'),
        ('PAID', 'Payé'),
        ('CANCELLED', 'Annulé'),
    )
    
    id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='commissions')
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='commissions')
    sale = models.ForeignKey(Sales, on_delete=models.SET_NULL, null=True, blank=True, related_name='commissions')
    
    commission_type = models.CharField(max_length=20, choices=COMMISSION_TYPES, default='PERCENTAGE')
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Pourcentage ou montant fixe
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Montant calculé de la commission
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.shop.name} - Commission: {self.amount} ({self.get_status_display()})"
    
    def calculate_commission(self, sale_amount):
        """Calcule la commission basée sur le type"""
        if self.commission_type == 'PERCENTAGE':
            return (sale_amount * self.rate) / 100
        else:  # FIXED
            return self.rate
    
    class Meta:
        verbose_name = "Commission"
        verbose_name_plural = "Commissions"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['shop', 'status', '-created_at']),
            models.Index(fields=['account', '-created_at']),
        ]


class History(models.Model):
    id = models.BigAutoField(primary_key=True)
    shop_name = models.CharField(max_length=30)
    shop_owner = models.CharField(max_length=30)
    shop_id = models.IntegerField()

    province = models.CharField(max_length=50, null=True ,blank=True)
    commune = models.CharField(max_length=50, null=True ,blank=True)
    quarter = models.CharField(max_length=50, null=True ,blank=True)
    address = models.CharField(max_length=50, null=True ,blank=True)
    longitude = models.CharField(max_length=30, null=True, blank=True)
    latitude = models.CharField(max_length=30, null=True, blank=True)

    action = models.CharField(max_length=50)
    category = models.CharField(max_length=50, null=True, blank=True)
    sub_category = models.CharField(max_length=50, null=True, blank=True)
    product_name = models.CharField(max_length=50)
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    unity_price = models.IntegerField(null=True)
    total_price = models.IntegerField(null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
