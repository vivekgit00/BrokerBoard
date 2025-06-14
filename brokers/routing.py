from django.urls import re_path
from .consumer import DeltaConsumer

websocket_urlpatterns = [
    re_path(r'ws/delta/$', DeltaConsumer.as_asgi()),
]
