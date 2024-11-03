from rest_framework import serializers
from django.utils import timezone
from .models import WastePlastic, WastePlasticRequestor, Notification, RequestPickUp, TaskAssigned, ContentManagement, WastePlasticType
from UserManagement.serializers import CustomUsersSerializer


class WastePlasticTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WastePlasticType
        fields = '__all__'


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
    wastePlastic_type = WastePlasticTypeSerializer()
    class Meta:
        model = WastePlasticRequestor
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class NotificationListSerializer(serializers.ModelSerializer):
    userId = CustomUsersSerializer()
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
    # userId = CustomUsersSerializer()
    requestId = WastePlasticRequestorListSerializer()

    class Meta:
        model = TaskAssigned
        fields = '__all__'


class ContentManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentManagement
        fields = '__all__'


class MomoPaymentSerializer(serializers.Serializer):
    amount = serializers.CharField(max_length=20)
    currency = serializers.CharField(max_length=10)
    partyId = serializers.CharField(max_length=20)
    payerMessage = serializers.CharField(max_length=255, required=False)
    payeeNote = serializers.CharField(max_length=255, required=False)