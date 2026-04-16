from .dependancies import *

# Defined locally to break circular dependencies with ProductSerializer
class MinimalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class MinimalSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name"]

class ProductMinimalSerializer(serializers.ModelSerializer):
    # Traversal: Product model has a field 'product' pointing to BasicProduct
    category = MinimalCategorySerializer(source='product.sub_category.category', read_only=True)
    sub_category = MinimalSubCategorySerializer(source='product.sub_category', read_only=True)
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
