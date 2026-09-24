from .dependencies import *
class UserViewSet(
		mixins.CreateModelMixin,
		mixins.RetrieveModelMixin,
		mixins.ListModelMixin,
		mixins.UpdateModelMixin,
		mixins.DestroyModelMixin,
		viewsets.GenericViewSet
	):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	authentication_classes = JWTAuthentication, SessionAuthentication
	permission_classes = IsAuthenticated,
	filter_backends = [filters.DjangoFilterBackend, ]
	filterset_fields = {
		'username': ['icontains']
	}

	def get_queryset(self):
		user = self.request.user
		queryset = User.objects.select_related('account').prefetch_related('groups')
		
		# Les superusers voient tous les utilisateurs
		if user.is_superuser:
			return queryset
		
		# Vérifier si l'utilisateur est un agent
		is_agent = user.groups.filter(name='agent').exists() or (hasattr(user, 'account') and user.account and user.is_staff and not user.is_superuser)
		
		if is_agent:
			# Les agents voient uniquement les utilisateurs qu'ils ont créés ET eux-mêmes
			from django.db.models import Q
			queryset = queryset.filter(Q(account__created_by=user) | Q(id=user.id))
		else:
			# Pour les autres utilisateurs (non-admin, non-agent), ils ne peuvent voir que leur propre profil
			# Vérifier si c'est une requête de récupération d'un utilisateur spécifique
			pk = self.kwargs.get('pk')
			if pk:
				# Vérifier si l'utilisateur demande son propre profil
				if str(pk) == str(user.id):
					return queryset.filter(id=pk)
				else:
					# Sinon, retourner un queryset vide (pas de permission)
					return queryset.none()
			else:
				# Liste : retourner uniquement son propre profil
				return queryset.filter(id=user.id)
		
		return queryset

	@action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
	def change_password(self, request):
		"""
		Permet à un utilisateur connecté de modifier son propre mot de passe.
		"""
		user = request.user
		old_password = request.data.get('old_password')
		new_password = request.data.get('new_password')

		if not new_password or len(str(new_password).strip()) < 4:
			return Response({'error': 'Le nouveau mot de passe doit contenir au moins 4 caractères.'}, status=status.HTTP_400_BAD_REQUEST)

		if old_password:
			if not user.check_password(old_password):
				return Response({'error': 'L\'ancien mot de passe est incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

		user.set_password(new_password.strip())
		user.save()
		return Response({'status': 'Mot de passe modifié avec succès.'})

	@action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
	def reset_user_password(self, request, pk=None):
		"""
		Permet à un administrateur ou agent de réinitialiser le mot de passe d'un utilisateur qu'il gère.
		"""
		target_user = self.get_object()
		new_password = request.data.get('new_password')

		if not new_password or len(str(new_password).strip()) < 4:
			return Response({'error': 'Le nouveau mot de passe doit contenir au moins 4 caractères.'}, status=status.HTTP_400_BAD_REQUEST)

		target_user.set_password(new_password.strip())
		target_user.save()
		return Response({'status': f'Le mot de passe de {target_user.username} a été mis à jour avec succès.'})

