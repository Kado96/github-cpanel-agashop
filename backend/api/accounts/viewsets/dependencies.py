from rest_framework import viewsets, mixins, status, views
from rest_framework.filters import SearchFilter
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, BasePermission
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt

from api.accounts.serializers import *
from api.accounts.models import *