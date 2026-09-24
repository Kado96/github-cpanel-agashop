from rest_framework import serializers
from api.shops.models import Commission

class CommissionSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name', read_only=True)
    agent_name = serializers.CharField(source='account.user.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Commission
        fields = ['id', 'shop', 'shop_name', 'account', 'agent_name', 'sale', 'commission_type', 'rate', 'amount', 'status', 'status_display', 'payment_date', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
