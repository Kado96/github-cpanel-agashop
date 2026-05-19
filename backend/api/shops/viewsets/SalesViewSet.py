from .dependancies import *
from django.utils.timezone import now

def getBenefice(data):
	benefice = 0
	for s in data:
		# Utiliser le prix d'achat enregistré lors de la vente, sinon repli sur le prix actuel du produit
		buy_price = s.buy_price if hasattr(s, 'buy_price') and s.buy_price > 0 else s.product.buy_price
		pat = buy_price * s.quantity
		benefice += (s.amount - pat)

	return benefice

class SalesViewSet(viewsets.ModelViewSet):
	authentication_classes = SessionAuthentication, JWTAuthentication
	permission_classes = IsAuthenticated,
	queryset = Sales.objects.all()
	serializer_class = SalesSerializer
	ordering = ['-created_at']
	filter_backends = [filters.DjangoFilterBackend, ]
	filterset_fields = {
		'product': ['exact'],
		'id': ['gt'],
	}

	def list(self, request, *args, **kwargs):
		from api.shops.utils import parse_date_range
		str_du = request.query_params.get('created_at__gte')
		str_au = request.query_params.get('created_at__lte')
		shop = request.query_params.get('shop')

		queryset = self.filter_queryset(self.get_queryset())
		
		if shop:
			queryset = queryset.filter(product__shop=shop)
			
			start_dt, end_dt = parse_date_range(str_du, str_au)
			if start_dt:
				queryset = queryset.filter(created_at__gte=start_dt)
			if end_dt:
				queryset = queryset.filter(created_at__lte=end_dt)
				
			queryset = queryset.order_by('-id')

		no_pagination = request.query_params.get('no_pagination') == 'true'
		if no_pagination:
			page = None
		else:
			page = self.paginate_queryset(queryset)

		if page is not None:
			serializer = self.get_serializer(
				page,
				many=True,
				context = {'request': request}
			)

			response = self.get_paginated_response(serializer.data)
			pvt = queryset.aggregate(sum=models.Sum('amount'))['sum']
			benefice = getBenefice(queryset)
			totals = {"pvt":pvt,"benefice":benefice}
			response.data["totals"] = totals
			return response

		response = super().list(request, args, kwargs)
		pvt = queryset.aggregate(sum=models.Sum('amount'))['sum']
		benefice = getBenefice(queryset)
		totals = {"pvt":pvt,"benefice":benefice}

		response.data["totals"] = totals
		return response

	@transaction.atomic()
	def perform_create(self, serializer):
		from api.shops.utils import safe_parse_datetime
		instance = serializer.save()
		
		# Forcer la date si fournie (format robuste)
		raw_date = self.request.data.get('created_at')
		if raw_date:
			parsed_date = safe_parse_datetime(raw_date)
			if parsed_date:
				instance.created_at = parsed_date
				instance.save(update_fields=['created_at'])
