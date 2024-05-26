from rest_framework import serializers
from .models import WastePlastic, WastePlasticRequestor, Notification, RequestPickUp, TaskAssigned

class WastePlasticSerializer(serializers.ModelSerializer):
    class Meta:
        model = WastePlastic
        fields = ['user', 'wastePlastic_type', 'collection_date', 'wastePlastic_size', 'pickUp_status']
        read_only_fields = ['id', 'collection_date']

class WastePlasticRequestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = WastePlasticRequestor
        fields = ['id','requestor', 'wastePlastic_type', 'request_date', 'request_time', 'wastePlastic_size', 'wastePlastic_address', 'unique_location', 'latitude', 'longitude', 'pickUp_status']
        read_only_fields = ['id', 'request_date']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class RequestPickUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestPickUp
        fields = '__all__'


class TaskAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAssigned
        fields = '__all__'