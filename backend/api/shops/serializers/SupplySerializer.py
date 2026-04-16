from .dependancies import *

class SupplyCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False, allow_null=True)
    class Meta:
        model = Supply
        fields = ["id", "user", "product", "quantity", "total_buy_price", "sale_price", "created_at"]


class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = "__all__"
        depth = 2

