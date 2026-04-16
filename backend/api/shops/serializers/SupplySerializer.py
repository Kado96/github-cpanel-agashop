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
    # 'product' est le lien vers BasicProduct dans votre modèle
    product = MinimalBasicProductDetailSerializer(read_only=True)
    name = serializers.ReadOnlyField(source='product.name')
    
    class Meta:
        model = Product
        fields = ["id", "name", "product", "sale_price", "quantity"]

# 3. Le Serializer principal pour la liste des Achats
class SupplySerializer(serializers.ModelSerializer):
    product = ProductMinimalSerializer(read_only=True)
    user_name = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Supply
        fields = "__all__"

# 4. Pour la création (plus léger)
class SupplyCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False, allow_null=True)
    class Meta:
        model = Supply
        fields = ["id", "user", "product", "quantity", "total_buy_price", "sale_price", "created_at"]
