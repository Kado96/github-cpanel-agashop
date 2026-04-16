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
class ProductDetailSerializer(serializers.ModelSerializer):
    # Mapping direct pour éviter tout malentendu
    name = serializers.ReadOnlyField(source='product.name')
    image_url = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()
    
    # Champ 'product' imbriqué pour supply.product.product
    product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "image_url", "category", "sub_category", "product", "sale_price", "quantity"]

    def get_image_url(self, obj):
        try: return obj.product.image.url if obj.product.image else None
        except: return None

    def get_category(self, obj):
        if not obj.product or not obj.product.sub_category: return None
        return {"id": obj.product.sub_category.category.id, "name": obj.product.sub_category.category.name}

    def get_sub_category(self, obj):
        if not obj.product: return None
        return {"id": obj.product.sub_category.id, "name": obj.product.sub_category.name}

    def get_product(self, obj):
        if not obj.product: return None
        return {"id": obj.product.id, "name": obj.product.name}

class SupplySerializer(serializers.ModelSerializer):
    # 'product' est le cœur du problème d'affichage
    product_detail = ProductDetailSerializer(source='product', read_only=True)
    
    class Meta:
        model = Supply
        fields = ["id", "user", "product", "product_detail", "quantity", "total_buy_price", "sale_price", "created_at"]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # On injecte l'objet détaillé à la place de l'ID pour le frontend
        if 'product_detail' in data:
            data['product'] = data.pop('product_detail')
        return data

# 4. Pour la création (plus léger)
class SupplyCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False, allow_null=True)
    class Meta:
        model = Supply
        fields = ["id", "user", "product", "quantity", "total_buy_price", "sale_price", "created_at"]
