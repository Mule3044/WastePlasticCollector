from rest_framework import serializers
from .models import WastePlastic, WastePlasticRequestor

class WastePlasticSerializer(serializers.ModelSerializer):
    class Meta:
        model = WastePlastic
        fields = ['user', 'wastePlastic_type', 'collection_date', 'wastePlastic_size', 'status']
        read_only_fields = ['id', 'collection_date']

class WastePlasticRequestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = WastePlasticRequestor
        fields = ['requestor', 'wastePlastic_type', 'request_date', 'wastePlastic_size', 'wastePlastic_address', 'unique_location', 'latitude', 'longitude', 'message', 'recent_activity', 'request_history']
        read_only_fields = ['id', 'request_date']
