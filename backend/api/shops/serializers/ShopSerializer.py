from .dependancies import *

class ShopSerializer(serializers.ModelSerializer):
	class Meta:
		model = Shop
		fields = "__all__"
		depth = 2

class ControlFrequencySerializer(serializers.ModelSerializer):
	class Meta:
		model = ControlFrequency
		fields = "__all__"