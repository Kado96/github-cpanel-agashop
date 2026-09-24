from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.shops.models import Commission
from api.shops.serializers.CommissionSerializer import CommissionSerializer


class CommissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion et le suivi des commissions des agents apporteurs d'affaires.
    """
    serializer_class = CommissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Commission.objects.all()
        # Si c'est un agent, il ne voit que ses propres commissions
        return Commission.objects.filter(account__user=user)
