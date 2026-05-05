from .dependancies import *
from ..serializers.ProductSerializer import ProductMediaSerializer
from ..models import ProductMedia

class MediaViewSet(viewsets.ModelViewSet):
    queryset = ProductMedia.objects.all()
    serializer_class = ProductMediaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # On pourrait filtrer ici par utilisateur ou boutique si nécessaire
        return ProductMedia.objects.all()
