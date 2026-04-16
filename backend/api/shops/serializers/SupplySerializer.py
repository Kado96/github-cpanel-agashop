from .dependancies import *

class ProductMinimalSerializer(serializers.ModelSerializer):
    # Utilisation de ReadOnlyField avec source : plus performant et robuste
    name = serializers.ReadOnlyField(source='product.name', default="Produit inconnu")
    image_url = serializers.SerializerMethodField()
    category_name = serializers.ReadOnlyField(source='product.sub_category.category.name', default=None)
    sub_category_name = serializers.ReadOnlyField(source='product.sub_category.name', default=None)
    
    # Simulation de la structure imbriquée attendue par le frontend
    product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "image_url", "category_name", "sub_category_name", "product", "sale_price", "quantity"]

    def get_image_url(self, obj):
        try:
            if obj.product and obj.product.image:
                return obj.product.image.url
        except:
            pass
        return None

    def get_product(self, obj):
        # Pour supply.product.product.sub_category
        if not obj.product: return None
        return {
            "id": obj.product.id,
            "name": obj.product.name,
            "sub_category": {
                "id": obj.product.sub_category.id if obj.product.sub_category else None,
                "name": obj.product.sub_category.name if obj.product.sub_category else None
            }
        }

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
