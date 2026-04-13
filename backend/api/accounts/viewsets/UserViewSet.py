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
