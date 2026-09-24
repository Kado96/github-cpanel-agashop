from .dependancies import *
from django.utils import timezone
from datetime import timezone as tz

class SubCategoryWithCategorySerializer(serializers.ModelSerializer):
	category_name = serializers.CharField(source='category.name', read_only=True)
	class Meta:
		model = SubCategory
		fields = ("id", "name", "category", "category_name")

class ProductMediaSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductMedia
		fields = "__all__"

class BasicProductSerializer(serializers.ModelSerializer):
	sub_category = SubCategoryWithCategorySerializer(read_only=True)
	media_details = ProductMediaSerializer(source='media', read_only=True)
	image_url = serializers.SerializerMethodField()

	class Meta:
		model = BasicProduct
		fields = "__all__"
		
	def get_image_url(self, obj):
		request = self.context.get('request')

		# 1. Vérification des métadonnées de stockage centralisé (FileMetadata)
		try:
			from api.shops.models import FileMetadata
			from django.conf import settings

			storage_meta = FileMetadata.objects.filter(product_id=str(obj.id)).first()
			if storage_meta and storage_meta.external_file_id:
				ext_id = storage_meta.external_file_id
				if ext_id.startswith('http://') or ext_id.startswith('https://'):
					return ext_id
				
				provider = getattr(settings, 'STORAGE_PROVIDER', 'LOCAL')
				if provider == 'SUPABASE_S3':
					endpoint = getattr(settings, 'SUPABASE_S3_ENDPOINT_URL', '')
					bucket = getattr(settings, 'SUPABASE_S3_BUCKET_NAME', 'media')
					if endpoint and '.supabase.co' in endpoint:
						project_ref = endpoint.split('.')[0].replace('https://', '')
						return f"https://{project_ref}.supabase.co/storage/v1/object/public/{bucket}/{ext_id}"
					return f"{endpoint}/{bucket}/{ext_id}"
				elif provider == 'GOOGLE_DRIVE':
					return f"https://drive.google.com/uc?export=view&id={ext_id}"
		except Exception as e:
			pass


		# 2. Priorité au système de média local
		if obj.media and obj.media.file:
			url = obj.media.file.url
		# 3. Fallback sur l'ancien champ image
		elif obj.image:
			url = obj.image.url
		else:
			return None
			
		if request:
			return request.build_absolute_uri(url)
		return url




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
		controlled = False 
		now = timezone.now()
		
		# On utilise un cache contextuel pour éviter de requêter la fréquence à chaque produit
		frequency = None
		if 'frequency_cache' in self.context:
			frequency = self.context['frequency_cache'].get(obj.shop_id)
		else:
			frequency = ControlFrequency.objects.filter(shop=obj.shop).first()
		
		if obj.last_control_at:
			delta = now - obj.last_control_at
			
			# Tolérance augmentée à 60s pour la production
			if delta.total_seconds() < 60:
				controlled = True
			elif frequency:
				f = frequency
				if f.minutes > 0:
					diff_minutes = delta.total_seconds() / 60
					controlled = diff_minutes <= f.minutes
				elif f.hours > 0:
					diff_hours = delta.total_seconds() / 3600
					controlled = diff_hours <= f.hours
				elif f.days > 0:
					diff_days = (now.date() - obj.last_control_at.date()).days
					controlled = diff_days <= f.days
		
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
	quantity = serializers.FloatField(required=True)


class SupplyProductSerializer(serializers.Serializer):
	quantity = serializers.FloatField(required=True)
	total_buy_price = serializers.FloatField(required=True)
	sale_price = serializers.FloatField(required=False, allow_null=True)
	created_at = serializers.DateTimeField(required=False, allow_null=True)