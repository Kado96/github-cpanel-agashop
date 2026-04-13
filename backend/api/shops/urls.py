from django.urls import path, include
from rest_framework import routers
from .viewsets import *

router = routers.DefaultRouter()

router.register("shops", ShopViewSet, basename="shops")
router.register("control-frequency", ControlFrequencyViewSet, basename="frequency-controls")
router.register("provinces", ProvincesViewSet, basename="provinces")
router.register("sales", SalesViewSet, basename="sales")
router.register("products", ProductViewSet, basename="products")
router.register("basic-products", BasicProductViewSet, basename="basic-products")
router.register("supplies", SupplyViewSet, basename="supplies")
router.register("categories", CategoryViewSet, basename="categories")
router.register("sub-categories", SubCategoryViewSet, basename="sub-categories")
router.register("history", HistoryViewSet, basename="history")
router.register("expenses", ExpenseViewSet, basename="expenses")

urlpatterns = [
    path('', include(router.urls)),
]
