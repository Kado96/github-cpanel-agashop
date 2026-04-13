from .dependancies import *
from django.db import models as db_models


class SupplyViewSet(viewsets.ModelViewSet):
	authentication_classes = SessionAuthentication, JWTAuthentication
	permission_classes = IsAuthenticated,
	queryset = Supply.objects.all()
	serializer_class = SupplySerializer
	ordering = ['-created_at']
	filterset_fields = {
		'product': ['exact'],
		'created_at': ['gte', 'lte'],
		'id': ['gt'],
	}

	def get_serializer_class(self):
		if self.action == "create":
			return SupplyCreateSerializer
		return SupplySerializer

	def _supply_totals(self, queryset):
		"""Totaux sur achats affichés (quantity > 0, total_buy_price > 0)."""
		displayed = queryset.filter(quantity__gt=0, total_buy_price__gt=0)
		agg = displayed.aggregate(
			sum_pat=db_models.Sum('total_buy_price'),
			sum_qty=db_models.Sum('quantity'),
		)
		return {'totals': agg['sum_pat'] or 0, 'totals_quantity': agg['sum_qty'] or 0}

	def list(self, request, *args, **kwargs):
		shop = request.query_params.get('shop')
		str_du = request.query_params.get('created_at__gte')
		str_au = request.query_params.get('created_at__lte')		
		queryset = self.filter_queryset(self.get_queryset())
		if(shop):
			if(str_du and str_au):
				str_au = datetime.strptime(str_au, "%Y-%m-%d")+timedelta(days=1)
				str_au = str_au.strftime("%Y-%m-%d")
				queryset = self.queryset = self.queryset.filter(
					created_at__gte=str_du, created_at__lte=str_au, product__shop=shop
				).order_by('-id')
			else:
				today = datetime.now().date()
				if(not request.user.is_superuser):
					queryset = self.queryset.filter(
						product__shop=shop,
					).order_by('-id')
				else:
					queryset = self.queryset.filter(
						product__shop=shop, user=request.user
					).order_by('-id')

		tot = self._supply_totals(queryset)
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(
				page,
				many=True,
				context={'request': request},
			)
			response = self.get_paginated_response(serializer.data)
			response.data['totals'] = tot['totals']
			response.data['totals_quantity'] = tot['totals_quantity']
			return response

		response.data['totals'] = tot['totals']
		response.data['totals_quantity'] = tot['totals_quantity']
		return response

	@transaction.atomic()
	def perform_update(self, serializer):
		instance = self.get_object()
		# Si la quantité change, on ajuste le stock du produit
		if 'quantity' in serializer.validated_data:
			new_qty = serializer.validated_data['quantity']
			diff = new_qty - instance.quantity
			product = instance.product
			product.quantity += diff
			product.save(update_fields=['quantity'])
			
		serializer.save()

	@transaction.atomic()
	def perform_destroy(self, instance):
		# On retire la quantité achetée du stock
		product = instance.product
		product.quantity -= instance.quantity
		# On évite un stock négatif (optionnel, mais recommandé)
		if product.quantity < 0:
			product.quantity = 0
		product.save(update_fields=['quantity'])
		
		instance.delete()