
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from api.accounts.viewsets import CustomTokenObtainPairView, RegisterViewSet

from . import settings

admin.site.site_header = 'AGASHOP ADMINISTRATION'
admin.site.index_title = 'Agashop Admin'
admin.site.site_title = 'Administration'

class AgashopView(APIView):
    def get(self, request, *args, **kwargs):
        custom_links = {
            'accounts': request.build_absolute_uri('accounts/'),
            'shops': request.build_absolute_uri('shops/'),
            
        }
        return Response(custom_links)

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', AgashopView.as_view()),
    path('api/accounts/', include("api.accounts.urls")),
    path('api/shops/', include("api.shops.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('api/login/', CustomTokenObtainPairView.as_view(), name="login"),
    path('api/register/', RegisterViewSet.as_view(), name="register"),
    path('api/refresh/', TokenRefreshView.as_view()),
    path('api/logout/', TokenBlacklistView.as_view(), name="logout"),  # Pour blacklister le token lors du logout
    re_path(
        "^(?!media)(?!admin)(?!api)(?!ussd)(?!static)(?!silk).*$",
        TemplateView.as_view(template_name='index.html')
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
