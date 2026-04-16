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
        Version ultra-robuste qui ne plante JAMAIS, même si des données manquent.
        """
        try:
            # 1. Structure de base
            ret = super().to_representation(instance)
            
            # 2. Accès sécurisé aux relations
            p = instance.product
            bp = p.product if p else None  # BasicProduct
            sc = bp.sub_category if bp else None
            cat = sc.category if sc else None
            
            # 3. Construction de l'objet attendu par le frontend
            # Structure : supply.product.product.sub_category.category
            ret['product'] = {
                "id": p.id if p else instance.product_id,
                "name": bp.name if bp else "Produit inconnu",
                "sale_price": p.sale_price if p else 0,
                "quantity": p.quantity if p else 0,
                "product": {
                    "id": bp.id if bp else None,
                    "name": bp.name if bp else "Produit inconnu",
                    "image": bp.image.url if (bp and bp.image) else None,
                    "sub_category": {
                        "id": sc.id if sc else None,
                        "name": sc.name if sc else None,
                        "category": {
                            "id": cat.id if cat else None,
                            "name": cat.name if cat else None
                        }
                    }
                }
            }
            return ret
        except Exception:
            # Secours ultime : on renvoie la version standard si la personnalisation échoue
            return super().to_representation(instance)

class SupplyCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False, allow_null=True)
    class Meta:
        model = Supply
        fields = ["id", "user", "product", "quantity", "total_buy_price", "sale_price", "created_at"]

# 4. Pour la création (plus léger)
class SupplyCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False, allow_null=True)
    class Meta:
        model = Supply
        fields = ["id", "user", "product", "quantity", "total_buy_price", "sale_price", "created_at"]
