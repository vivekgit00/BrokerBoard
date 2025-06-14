from .views import DeltaBrokerView , DeltaWebsocket
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'brokers', DeltaBrokerView, basename='brokers')
router.register("market", DeltaWebsocket, basename="market")

urlpatterns = router.urls