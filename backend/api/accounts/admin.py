from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *

# Personnaliser l'admin User pour ajouter une action de changement de mot de passe
class CustomUserAdmin(BaseUserAdmin):
    actions = ['change_password_action']
    
    def change_password_action(self, request, queryset):
        """Action pour changer le mot de passe des utilisateurs sélectionnés"""
        if queryset.count() != 1:
            self.message_user(request, "Veuillez sélectionner exactement un utilisateur.", level=messages.ERROR)
            return
        
        user = queryset.first()
        # Rediriger vers la page de changement de mot de passe Django standard
        return HttpResponseRedirect(
            reverse('admin:auth_user_password_change', args=[user.pk])
        )
    
    change_password_action.short_description = "Changer le mot de passe (invalide les tokens JWT)"

# Désenregistrer l'admin User par défaut et réenregistrer avec notre version personnalisée
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_email', 'user_username', 'phone_number', 'email_validated', 'is_active', 'created_at')
    list_filter = ('is_active', 'email_validated', 'created_at')
    search_fields = ('user__email', 'user__username', 'phone_number')
    readonly_fields = ('created_at', 'updated_at', 'otp_code', 'otp_expire_at')
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user', 'role')
        }),
        ('Informations de contact', {
            'fields': ('phone_number', 'email_validated')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
        ('OTP', {
            'fields': ('otp_code', 'otp_expire_at'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email if obj.user else '-'
    user_email.short_description = 'Email'
    
    def user_username(self, obj):
        return obj.user.username if obj.user else '-'
    user_username.short_description = 'Username'
    
    actions = ['reset_password_action']
    
    def reset_password_action(self, request, queryset):
        """Action pour réinitialiser le mot de passe des comptes sélectionnés"""
        from api.accounts.viewsets import generate_password, blacklist_user_tokens
        from api.tools import send_custom_email
        
        count = 0
        for account in queryset:
            user = account.user
            new_password = generate_password(8)
            
            # Blacklister tous les tokens existants AVANT de changer le mot de passe
            blacklist_user_tokens(user)
            
            # Changer le mot de passe
            user.set_password(new_password)
            user.save()
            
            recipient_email = user.email or user.username
            if recipient_email and "@" in recipient_email:
                mail_data = {
                    "email": [recipient_email],
                    "password": new_password,
                }
                send_custom_email(mail_data, "reset_password.html")
                count += 1
        
        self.message_user(request, f"Mot de passe réinitialisé pour {count} compte(s). Tous les anciens tokens JWT ont été blacklistés et sont maintenant invalides.", level=messages.SUCCESS)
    reset_password_action.short_description = "Réinitialiser le mot de passe (blackliste les tokens)"