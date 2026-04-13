from .dependancies import *
from datetime import timezone as tz

class SubCategoryWithCategorySerializer(serializers.ModelSerializer):
	category_name = serializers.CharField(source='category.name', read_only=True)
	class Meta:
		model = SubCategory
		fields = ("id", "name", "category", "category_name")

class BasicProductSerializer(serializers.ModelSerializer):
	sub_category = SubCategoryWithCategorySerializer(read_only=True)
	class Meta:
		model = BasicProduct
		fields = "__all__"
		
	def get_image_url(self, obj):
		request = self.context.get('request')
		if obj.image:
			return request.build_absolute_uri(obj.image.url) if request else obj.image.url
		return None


class ProductCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
	product = BasicProductSerializer()
	class Meta:
		model = Product
		fields = "__all__"

	def to_representation(self, obj):
		representation = super(ProductSerializer, self).to_representation(obj)
		controlled = None
		
		if obj.last_control_at:
			frequency = ControlFrequency.objects.filter(shop=obj.shop)
			if frequency:
				f = frequency[0]
				now = datetime.now(tz=tz.utc)
				delta = now - obj.last_control_at
				if f.minutes > 0:
					representation["control_minutes"] = f.minutes
					diff_minutes = delta.total_seconds() / 60
					controlled = diff_minutes <= f.minutes
				elif f.hours > 0:
					representation["control_hours"] = f.hours
					diff_hours = delta.total_seconds() / 3600
					controlled = diff_hours <= f.hours
				elif f.days > 0:
					representation["control_days"] = f.days
					diff_days = (now.date() - obj.last_control_at.date()).days
					controlled = diff_days <= f.days
		else:
			controlled = False

		representation["controlled"] = controlled
		return representation

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = "__all__"

	def to_representation(self, obj):
		representation = super().to_representation(obj)
		sub_categories = SubCategory.objects.filter(category=obj.id)
		representation["subCategories"] = SubCategorySerializerCustom(sub_categories, many=True).data
		return representation


class SubCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = SubCategory
		fields = "__all__"

class SubCategorySerializerCustom(serializers.ModelSerializer):
	class Meta:
		model = SubCategory
		fields = "id","name"

class ControlProductSerializer(serializers.Serializer):
	quantity = serializers.IntegerField(required=True)


class SupplyProductSerializer(serializers.Serializer):
	quantity = serializers.IntegerField(required=True)
	total_buy_price = serializers.FloatField(required=True)