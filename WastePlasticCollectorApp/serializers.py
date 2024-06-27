from rest_framework import serializers
from .models import WastePlastic, WastePlasticRequestor, Notification, RequestPickUp, TaskAssigned, ContentManagement, WastePlasticType
from UserManagement.serializers import CustomUsersSerializer

class WastePlasticSerializer(serializers.ModelSerializer):
    class Meta:
        model = WastePlastic
        fields = ['user', 'wastePlastic_type', 'collection_date', 'wastePlastic_size', 'pickUp_status']
        read_only_fields = ['id', 'collection_date']

class WastePlasticRequestorCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = WastePlasticRequestor
        fields = '__all__'

class WastePlasticRequestorListSerializer(serializers.ModelSerializer):
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


class RequestPickUpListSerializer(serializers.ModelSerializer):
    userId = CustomUsersSerializer()
    class Meta:
        model = RequestPickUp
        fields = '__all__'


class TaskAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAssigned
        fields = '__all__'


class TaskAssignedListSerializer(serializers.ModelSerializer):
    userId = CustomUsersSerializer()
    class Meta:
        model = TaskAssigned
        fields = '__all__'


class ContentManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentManagement
        fields = '__all__'


class WastePlasticTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WastePlasticType
        fields = '__all__'