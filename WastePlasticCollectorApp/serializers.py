from rest_framework import serializers
from .models import WastePlastic, WastePlasticRequestor, Notification, RequestPickUp, TaskAssigned, ContentManagement
from UserManagement.serializers import CustomUsersSerializer

class WastePlasticSerializer(serializers.ModelSerializer):
    class Meta:
        model = WastePlastic
        fields = ['user', 'wastePlastic_type', 'collection_date', 'wastePlastic_size', 'pickUp_status']
        read_only_fields = ['id', 'collection_date']

class WastePlasticRequestorSerializer(serializers.ModelSerializer):
    requestor = CustomUsersSerializer()
    class Meta:
        model = WastePlasticRequestor
        fields = '__all__'


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


class ContentManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentManagement
        fields = '__all__'