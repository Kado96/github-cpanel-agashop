from django.urls import path, include
from rest_framework import routers
from .viewsets import *

from .viewsets.NotificationViewSet import NotificationViewSet, LumiCashPaymentViewSet
from .viewsets.CommissionViewSet import CommissionViewSet

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
router.register("media", MediaViewSet, basename="media")
router.register("notifications", NotificationViewSet, basename="notifications")
router.register("lumicash", LumiCashPaymentViewSet, basename="lumicash")
router.register("commissions", CommissionViewSet, basename="commissions")


from .viewsets.MediaUploadView import MediaUploadView

urlpatterns = [
    path('backup/download/', BackupExportView.as_view(), name='backup-download'),
    path('shops/<str:shop_id>/products/<str:product_id>/upload-media/', MediaUploadView.as_view(), name='product-media-upload'),
    path('', include(router.urls)),
]

