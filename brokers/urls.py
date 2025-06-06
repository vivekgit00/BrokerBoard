from .views import DeltaBrokerView
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'brokers', DeltaBrokerView, basename='brokers')

urlpatterns = router.urls