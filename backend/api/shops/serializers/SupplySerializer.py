from .dependancies import *

class SupplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = "__all__"


class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = "__all__"
        depth = 2

