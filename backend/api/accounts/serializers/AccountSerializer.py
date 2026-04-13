from .dependencies import *
from .UserSerializer import UserSerializer
class BasicAccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = "id", "phone_number",

	def to_representation(self, obj:Account):
		data = super().to_representation(obj)
		data["complete"] = obj.complete()	
		return data
class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		exclude = 'otp_code',
		read_only_fields = "is_active", "insecured", "otp_expire_at",
	
	def to_representation(self, obj:Account):
		data = super().to_representation(obj)
		data["complete"] = obj.complete()	
		data['user'] = UserSerializer(obj.user).data		
		return data

class OTPSerializer(serializers.Serializer):
	otp_code = serializers.CharField(min_length=5, max_length=5)

class ResetPasswordSerializer(serializers.Serializer):
	email = serializers.EmailField()