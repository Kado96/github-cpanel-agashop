from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Expense
from ..serializers import ExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['shop', 'expense_type']
    search_fields = ['description', 'receipt_number']
    ordering_fields = ['expense_date', 'amount', 'created_at']
    ordering = ['-expense_date']

    def get_queryset(self):
        from api.shops.utils import parse_date_range
        # Filtrer par boutique si shop_id est fourni en paramètre
        queryset = super().get_queryset()
        shop_id = self.request.query_params.get('shop')
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
            
        # Filtrage par plage de date (expense_date ou created_at)
        str_du = self.request.query_params.get('expense_date__gte') or self.request.query_params.get('created_at__gte')
        str_au = self.request.query_params.get('expense_date__lte') or self.request.query_params.get('created_at__lte')
        
        start_dt, end_dt = parse_date_range(str_du, str_au)
        if start_dt:
            queryset = queryset.filter(expense_date__gte=start_dt.date())
        if end_dt:
            queryset = queryset.filter(expense_date__lte=end_dt.date())
            
        return queryset

    def perform_create(self, serializer):
        # Associer automatiquement le compte de l'utilisateur qui crée la dépense
        account = None
        if hasattr(self.request.user, 'account'):
            account = self.request.user.account
        serializer.save(account=account)
