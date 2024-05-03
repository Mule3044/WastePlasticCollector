from rest_framework import serializers
from .models import WastePlastic, WastePlasticRequestor, Notification, RequestPickUp

class WastePlasticSerializer(serializers.ModelSerializer):
    class Meta:
        model = WastePlastic
        fields = ['user', 'wastePlastic_type', 'collection_date', 'wastePlastic_size', 'pickUp_status']
        read_only_fields = ['id', 'collection_date']

class WastePlasticRequestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = WastePlasticRequestor
        fields = ['requestor', 'wastePlastic_type', 'request_date', 'wastePlastic_size', 'wastePlastic_address', 'unique_location', 'latitude', 'longitude', 'pickUp_status']
        read_only_fields = ['id', 'request_date']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class RequestPickUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestPickUp
        fields = '__all__'