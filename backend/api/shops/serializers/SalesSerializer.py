from .dependancies import *
from .ProductSerializer import ProductSerializer

class SalesSerializer(serializers.ModelSerializer):
	product = ProductSerializer(read_only=True)

	class Meta:
		model = Sales
		fields = "__all__"
