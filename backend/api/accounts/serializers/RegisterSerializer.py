from .dependencies import *
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.Serializer):
	# L'identifiant (username) peut être un nom ou un email
	username = serializers.CharField(
		validators=[UniqueValidator(queryset=User.objects.all(), message="Ce nom d'utilisateur est déjà pris.")],
		required=True,
		max_length=150
	)
	# L'email est obligatoire pour la réinitialisation du mot de passe
	email = serializers.EmailField(
		validators=[UniqueValidator(queryset=User.objects.all(), message="Cet email est déjà pris.")],
		required=True,
	)
	# Le numéro de téléphone n'est plus imposé comme unique
	phone_number = serializers.CharField(required=True, max_length=20)
	password = serializers.CharField(required=True, min_length=4)