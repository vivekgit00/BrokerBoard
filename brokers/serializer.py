from rest_framework import serializers
from .models import DeltaBroker


class DeltaBrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeltaBroker
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }