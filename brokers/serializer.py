from rest_framework import serializers
from .models import DeltaBroker, Orders


class DeltaBrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeltaBroker
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'