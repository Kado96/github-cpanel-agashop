from .dependancies import *

# defined locally to avoid circular imports
class MinimalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class MinimalSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name"]

class ProductMinimalSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()
    # Simulated product object for frontend compatibility (supply.product.product)
    product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "image", "category", "sub_category", "product", "sale_price", "quantity"]

    def get_name(self, obj):
        return obj.product.name if (obj.product and hasattr(obj.product, 'name')) else "Produit inconnu"

    def get_image(self, obj):
        if obj.product and hasattr(obj.product, 'image') and obj.product.image:
            return obj.product.image.url if hasattr(obj.product.image, 'url') else str(obj.product.image)
        return None

    def get_category(self, obj):
        try:
            if obj.product and obj.product.sub_category and obj.product.sub_category.category:
                cat = obj.product.sub_category.category
                return {"id": cat.id, "name": cat.name}
        except:
            pass
        return None

    def get_sub_category(self, obj):
        try:
            if obj.product and obj.product.sub_category:
                sub = obj.product.sub_category
                return {"id": sub.id, "name": sub.name}
        except:
            pass
        return None

    def get_product(self, obj):
        if not obj.product:
            return None
        try:
            return {
                "id": obj.product.id,
                "name": obj.product.name,
                "sub_category": {
                    "id": obj.product.sub_category.id if obj.product.sub_category else None,
                    "name": obj.product.sub_category.name if obj.product.sub_category else None
                }
            }
        except:
            return {"id": obj.product.id, "name": getattr(obj.product, 'name', 'Inconnu')}

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
