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
		if self.action in ["create", "update", "partial_update"]:
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

	def get_queryset(self):
		return Supply.objects.all().order_by('-created_at', '-id')

	def list(self, request, *args, **kwargs):
		# 1. Utilisation du queryset standard avec filtres
		queryset = self.filter_queryset(self.get_queryset())
		shop_id = request.query_params.get('shop')
		if shop_id:
			queryset = queryset.filter(product__shop_id=shop_id)

		# 2. Calcul des totaux
		tot = self._supply_totals(queryset)
		
		# 3. Pagination standard
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			response = self.get_paginated_response(serializer.data)
			response.data['totals'] = tot['totals']
			response.data['totals_quantity'] = tot['totals_quantity']
			return response

		# 4. Fallback non paginé
		serializer = self.get_serializer(queryset, many=True)
		return Response({
			'results': serializer.data,
			'totals': tot['totals'],
			'totals_quantity': tot['totals_quantity']
		})

	@transaction.atomic()
	def perform_create(self, serializer):
		from api.shops.utils import safe_parse_datetime
		instance = serializer.save()
		
		# Mise à jour du stock
		product = instance.product
		product.quantity += instance.quantity
		
		# Mise à jour du prix de vente si fourni
		sale_price = self.request.data.get('sale_price')
		if sale_price and float(sale_price) > 0:
			# Création d'un historique si le prix change
			old_price = product.sale_price
			new_price = float(sale_price)
			if old_price != new_price:
				SalePriceHistory.objects.create(
					product=product,
					old_price=old_price,
					new_price=new_price,
					user=self.request.user
				)
				product.sale_price = new_price
		
		# Forcer la date si fournie (format robuste)
		raw_date = self.request.data.get('created_at')
		if raw_date:
			parsed_date = safe_parse_datetime(raw_date)
			if parsed_date:
				instance.created_at = parsed_date
				instance.save(update_fields=['created_at'])

		product.save(update_fields=['quantity', 'sale_price'])

	@transaction.atomic()
	def perform_update(self, serializer):
		from api.shops.utils import safe_parse_datetime
		instance = self.get_object()
		
		# Ajustement du stock au besoin
		if 'quantity' in serializer.validated_data:
			new_qty = serializer.validated_data['quantity']
			diff = new_qty - instance.quantity
			product = instance.product
			product.quantity += diff
			product.save(update_fields=['quantity'])
			
		serializer.save()
		instance = serializer.instance

		# Mise à jour du prix de vente si fourni
		sale_price = self.request.data.get('sale_price')
		if sale_price and float(sale_price) > 0:
			product = instance.product
			old_price = product.sale_price
			new_price = float(sale_price)
			if old_price != new_price:
				SalePriceHistory.objects.create(
					product=product,
					old_price=old_price,
					new_price=new_price,
					user=self.request.user
				)
				product.sale_price = new_price
				product.save(update_fields=['sale_price'])

		# Date personnalisée
		new_date_str = self.request.data.get('created_at')
		if new_date_str:
			parsed_date = safe_parse_datetime(new_date_str)
			if parsed_date:
				instance.created_at = parsed_date
				instance.save(update_fields=['created_at'])

	@transaction.atomic()
	def perform_destroy(self, instance):
		# On retire la quantité achetée du stock
		product = instance.product
		product.quantity -= instance.quantity
		if product.quantity < 0:
			product.quantity = 0
		product.save(update_fields=['quantity'])
		instance.delete()