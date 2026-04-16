from .dependancies import *

# 1. Classes minimales pour éviter les imports circulaires
class MinimalCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class MinimalSubCategoryDetailSerializer(serializers.ModelSerializer):
    category = MinimalCategoryDetailSerializer(read_only=True)
    class Meta:
        model = SubCategory
        fields = ["id", "name", "category"]

class MinimalBasicProductDetailSerializer(serializers.ModelSerializer):
    sub_category = MinimalSubCategoryDetailSerializer(read_only=True)
    class Meta:
        model = BasicProduct
        fields = ["id", "name", "image", "sub_category"]

# 2. Le Serializer de Produit (Boutique) imbriqué
class ProductMinimalSerializer(serializers.ModelSerializer):
    # 'product' est le champ qui contient BasicProduct
    product = serializers.SerializerMethodField()
    name = serializers.ReadOnlyField(source='product.name')
    
    class Meta:
        model = Product
        fields = ["id", "name", "product", "sale_price", "quantity"]

    def get_product(self, obj):
        if not obj.product: return None
        return {
            "id": obj.product.id,
            "name": obj.product.name,
            "image": obj.product.image.url if obj.product.image else None,
            "sub_category": {
                "id": obj.product.sub_category.id if obj.product.sub_category else None,
                "name": obj.product.sub_category.name if obj.product.sub_category else None,
                "category": {
                    "id": obj.product.sub_category.category.id if obj.product.sub_category and obj.product.sub_category.category else None,
                    "name": obj.product.sub_category.category.name if obj.product.sub_category and obj.product.sub_category.category else None,
                }
            }
        }

class SupplySerializer(serializers.ModelSerializer):
    # 'product' est le champ qui contient Product
    product_data = ProductMinimalSerializer(source='product', read_only=True)
    
    class Meta:
        model = Supply
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # On remplace 'product' par les données détaillées pour le frontend
        if 'product_data' in data:
            data['product'] = data.pop('product_data')
        return data

# 4. Pour la création (plus léger)
class SupplyCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False, allow_null=True)
    class Meta:
        model = Supply
        fields = ["id", "user", "product", "quantity", "total_buy_price", "sale_price", "created_at"]
