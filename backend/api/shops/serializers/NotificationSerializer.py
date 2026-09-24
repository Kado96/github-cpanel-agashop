from rest_framework import serializers
from api.shops.models import ControlNotification, LumiCashTransaction

class ControlNotificationSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name', read_only=True)

    class Meta:
        model = ControlNotification
        fields = ['id', 'shop', 'shop_name', 'notification_type', 'title', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']


class LumiCashTransactionSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name', read_only=True)

    class Meta:
        model = LumiCashTransaction
        fields = ['id', 'shop', 'shop_name', 'phone_number', 'amount', 'plan', 'reference_id', 'lumicash_tx_id', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'reference_id', 'status', 'created_at', 'updated_at']
