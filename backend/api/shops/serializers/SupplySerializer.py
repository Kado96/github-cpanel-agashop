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
class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = "__all__"
    
    def to_representation(self, instance):
        """
        Version 100% manuelle qui évite les plantages internes de DRF sur les champs automatiques.
        Ne fait jamais appel à super().to_representation en cas d'erreur.
        """
        try:
            p = instance.product
            bp = p.product if p else None
            sc = bp.sub_category if bp else None
            cat = sc.category if sc else None
            
            created_at = None
            if instance.created_at:
                created_at = instance.created_at.isoformat()
                if not created_at.endswith('Z') and '+' not in created_at:
                    created_at += 'Z'
            
            return {
                "id": instance.id,
                "quantity": instance.quantity,
                "total_buy_price": instance.total_buy_price,
                "sale_price": instance.sale_price,
                "created_at": created_at,
                "user": getattr(instance, 'user_id', None),
                "product": {
                    "id": getattr(p, 'id', getattr(instance, 'product_id', None)),
                    "name": getattr(bp, 'name', "Produit inconnu"),
                    "sale_price": getattr(p, 'sale_price', 0),
                    "quantity": getattr(p, 'quantity', 0),
                    "product": {
                        "id": getattr(bp, 'id', None),
                        "name": getattr(bp, 'name', "Produit inconnu"),
                        "image": bp.image.url if (bp and getattr(bp, 'image', None)) else None,
                        "sub_category": {
                            "id": getattr(sc, 'id', None),
                            "name": getattr(sc, 'name', None),
                            "category": {
                                "id": getattr(cat, 'id', None),
                                "name": getattr(cat, 'name', None)
                            }
                        }
                    }
                }
            }
        except Exception as e:
            # Fallback absolu si un getter manuel pète (très improbable avec les getattr)
            return {
                "id": getattr(instance, 'id', None),
                "quantity": getattr(instance, 'quantity', 0),
                "total_buy_price": getattr(instance, 'total_buy_price', 0),
                "product": None,
                "error": str(e)
            }

class SupplyCreateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création et la mise à jour des approvisionnements.
    Supporte les mises à jour partielles (PATCH) sans exiger le produit ou l'utilisateur.
    """
    created_at = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Supply
        fields = ["user", "product", "quantity", "total_buy_price", "sale_price", "created_at"]
        extra_kwargs = {
            'product': {'required': False},
            'user': {'required': False, 'allow_null': True},
            'quantity': {'required': False},
            'total_buy_price': {'required': False},
        }
