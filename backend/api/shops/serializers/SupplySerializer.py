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
    # Mapping explicite des champs du BasicProduct pour le frontend
    name = serializers.ReadOnlyField(source='product.name')
    image = serializers.ReadOnlyField(source='product.image')
    category = MinimalCategorySerializer(source='product.sub_category.category', read_only=True)
    sub_category = MinimalSubCategorySerializer(source='product.sub_category', read_only=True)
    
    # Pour la compatibilité avec getSubCategoryId dans le frontend
    product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "image", "category", "sub_category", "product", "sale_price", "quantity"]

    def get_product(self, obj):
        # Simule la structure s.product.product attendue par le frontend
        if obj.product:
            return {
                "id": obj.product.id,
                "name": obj.product.name,
                "sub_category": {
                    "id": obj.product.sub_category.id if obj.product.sub_category else None,
                    "name": obj.product.sub_category.name if obj.product.sub_category else None
                }
            }
        return None

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
