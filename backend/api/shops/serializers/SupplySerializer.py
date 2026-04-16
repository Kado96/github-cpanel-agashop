from .dependancies import *
from .ProductSerializer import CategorySerializer, SubCategorySerializer

class ProductMinimalSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source='product.sub_category.category', read_only=True)
    sub_category = SubCategorySerializer(source='product.sub_category', read_only=True)
    class Meta:
        model = Product
        fields = ["id", "name", "category", "sub_category"]

class SupplyCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False, allow_null=True)
    class Meta:
        model = Supply
        fields = ["id", "user", "product", "quantity", "total_buy_price", "sale_price", "created_at"]

class SupplySerializer(serializers.ModelSerializer):
    product = ProductMinimalSerializer(read_only=True)
    class Meta:
        model = Supply
        fields = "__all__"
