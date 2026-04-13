from .dependencies import serializers, User, Account
from django.contrib.auth.models import Group
from django.db.models import Q
	
class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=False, min_length=4)
	role = serializers.CharField(write_only=True, required=False)  # 'user', 'agent', 'admin'
	phone_number = serializers.SerializerMethodField(read_only=True)
	phone_number_write = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
	groups = serializers.SerializerMethodField(read_only=True)
	shops_count = serializers.SerializerMethodField(read_only=True)
	
	def get_phone_number(self, obj):
		"""Récupère le numéro de téléphone depuis l'Account associé"""
		try:
			return obj.account.phone_number if hasattr(obj, 'account') and obj.account else None
		except Account.DoesNotExist:
			return None
		except Exception:
			return None
	
	class Meta:
		model = User
		exclude = "last_login", "is_active", "date_joined", "user_permissions"
		depth = 1
		extra_kwargs = {
			'username': {'validators': []},
		}
	
	def validate_email(self, value):
		"""L'email est l'identifiant unique : un même email ne peut pas exister pour plusieurs comptes (admin, agent ou utilisateur)."""
		if not value or not value.strip():
			return value
		value = value.strip().lower()
		qs = User.objects.filter(email__iexact=value)
		if self.instance:
			qs = qs.exclude(pk=self.instance.pk)
		if qs.exists():
			raise serializers.ValidationError("Un utilisateur avec cet email existe déjà. Un email ne peut être associé qu'à un seul compte (admin, agent ou utilisateur).")
		return value
	
	def validate_username(self, value):
		"""Quand le username est un email, il doit être unique (un email = un seul compte)."""
		if not value or not value.strip():
			return value
		value = value.strip()
		if "@" not in value:
			return value
		normalized = value.lower()
		qs = User.objects.filter(
			Q(email__iexact=normalized) | Q(username__iexact=normalized)
		)
		if self.instance:
			qs = qs.exclude(pk=self.instance.pk)
		if qs.exists():
			raise serializers.ValidationError("Un utilisateur avec cet email existe déjà. Un email ne peut être associé qu'à un seul compte.")
		return value
	
	def get_groups(self, obj):
		return [group.name for group in obj.groups.all()]
	
	def get_shops_count(self, obj):
		"""
		Retourne le nombre total de boutiques liées à cet utilisateur.
		- owned_shops : boutiques dont il est propriétaire
		- managed_shops : boutiques qu'il gère en tant qu'agent
		"""
		try:
			account = obj.account
		except Account.DoesNotExist:
			return 0
		except Exception:
			return 0

		owned = getattr(account, "owned_shops", None)
		managed = getattr(account, "managed_shops", None)

		owned_count = owned.count() if owned is not None else 0
		managed_count = managed.count() if managed is not None else 0

		return owned_count + managed_count
	
	def create(self, validated_data):
		role = validated_data.pop('role', 'user')
		password = validated_data.pop('password', None)
		# Récupérer phone_number depuis phone_number_write ou phone_number
		phone_number = validated_data.pop('phone_number', None) or validated_data.pop('phone_number_write', None)
		
		# Récupérer l'utilisateur qui crée (agent ou admin)
		request = self.context.get('request')
		created_by = None
		if request and request.user:
			created_by = request.user
		
		user = User.objects.create(**validated_data)
		user.is_active = True  # Compte actif pour pouvoir se connecter
		if password:
			user.set_password(password)
		
		# Assigner le groupe selon le rôle
		if role == 'agent':
			group, created = Group.objects.get_or_create(name='agent')
			user.groups.add(group)
			user.is_staff = True
		elif role == 'admin':
			group, created = Group.objects.get_or_create(name='admin')
			user.groups.add(group)
			user.is_staff = True
			user.is_superuser = True
		
		user.save()
		
		# Créer un Account pour cet utilisateur avec le créateur
		try:
			account, created = Account.objects.get_or_create(
				user=user,
				defaults={
					"phone_number": phone_number,
					"created_by": created_by,  # Enregistrer qui a créé cet utilisateur
				},
			)
			# Si l'Account existe déjà, mettre à jour phone_number et created_by si nécessaire
			if not created:
				if phone_number:
					account.phone_number = phone_number
				if not account.created_by and created_by:
					account.created_by = created_by
				account.save()
		except Exception:
			# Si l'Account existe déjà, mettre à jour created_by si nécessaire
			try:
				account = Account.objects.get(user=user)
				if phone_number:
					account.phone_number = phone_number
				if not account.created_by and created_by:
					account.created_by = created_by
				account.save()
			except Exception:
				pass
		
		return user
	
	def update(self, instance, validated_data):
		role = validated_data.pop('role', None)
		password = validated_data.pop('password', None)
		# Récupérer phone_number depuis phone_number_write (le champ d'écriture)
		phone_number = validated_data.pop('phone_number_write', None)
		
		# Mettre à jour le numéro de téléphone dans l'Account si fourni
		if phone_number is not None:
			try:
				account = instance.account
				account.phone_number = phone_number
				account.save()
			except Account.DoesNotExist:
				# Créer un Account si il n'existe pas
				request = self.context.get('request')
				created_by = request.user if request and request.user else None
				Account.objects.create(
					user=instance,
					phone_number=phone_number,
					created_by=created_by
				)
			except Exception:
				pass
		
		# Log pour déboguer
		print(f"[USER UPDATE] Début de la mise à jour pour l'utilisateur {instance.username}")
		print(f"[USER UPDATE] Mot de passe reçu dans validated_data: {'OUI' if password else 'NON'}")
		if password:
			print(f"[USER UPDATE] Longueur du mot de passe reçu: {len(str(password))}")
		
		# Mettre à jour les champs de base
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		
		# Variable pour suivre si le mot de passe a été modifié
		password_was_changed = False
		
		# Traiter le mot de passe si fourni
		if password:
			# S'assurer que le mot de passe n'est pas une chaîne vide ou l'indicateur par défaut
			password_str = str(password).strip()
			print(f"[USER UPDATE] Mot de passe après trim: longueur={len(password_str)}, valeur={password_str[:3]}...")
			
			if password_str and password_str != '******** (mot de passe actuel)' and len(password_str) >= 4:
				print(f"[USER UPDATE] ✅ Mise à jour du mot de passe pour l'utilisateur {instance.username} (longueur: {len(password_str)})")
				instance.set_password(password_str)
				password_was_changed = True
				print(f"[USER UPDATE] ✅ set_password() appelé avec succès")
			else:
				print(f"[USER UPDATE] ❌ Mot de passe ignoré - Raison: vide={not password_str}, indicateur={password_str == '******** (mot de passe actuel)'}, longueur={len(password_str) if password_str else 0} (requis: 4)")
		
		# Mettre à jour le groupe selon le rôle
		if role:
			instance.groups.clear()
			if role == 'agent':
				group, created = Group.objects.get_or_create(name='agent')
				instance.groups.add(group)
				instance.is_staff = True
				instance.is_superuser = False
			elif role == 'admin':
				group, created = Group.objects.get_or_create(name='admin')
				instance.groups.add(group)
				instance.is_staff = True
				instance.is_superuser = True
			else:  # user
				instance.is_staff = False
				instance.is_superuser = False
		
		# Sauvegarder l'utilisateur (le mot de passe est hashé par set_password)
		instance.save()
		print(f"[USER UPDATE] ✅ Utilisateur {instance.username} sauvegardé avec succès dans la base de données")
		
		print(f"[USER UPDATE] ✅ Utilisateur {instance.username} sauvegardé avec succès dans la base de données")
		
		# Vérifier que le mot de passe a bien été sauvegardé en testant l'authentification
		if password_was_changed:
			password_str = str(password).strip()
			from django.contrib.auth import authenticate
			test_auth = authenticate(username=instance.username, password=password_str)
			if test_auth:
				print(f"[USER UPDATE] ✅ Vérification: le nouveau mot de passe fonctionne correctement pour {instance.username}")
			else:
				print(f"[USER UPDATE] ⚠️ ATTENTION: Le mot de passe n'a peut-être pas été sauvegardé correctement pour {instance.username}")
				# Réessayer avec une sauvegarde complète
				instance.save()
				test_auth2 = authenticate(username=instance.username, password=password_str)
				if test_auth2:
					print(f"[USER UPDATE] ✅ Après nouvelle sauvegarde: le mot de passe fonctionne maintenant")
				else:
					print(f"[USER UPDATE] ❌ ERREUR: Le mot de passe ne fonctionne toujours pas après nouvelle sauvegarde")
		
		return instance