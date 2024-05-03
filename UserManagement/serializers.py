from rest_framework import serializers
from .models import CustomUsers


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUsers
        fields = ['id','email', 'name', 'phone_number', 'profile_photo' ,'role', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = CustomUsers(
            email=self.validated_data['email'],
            name=self.validated_data.get('name', ''),
            phone_number=self.validated_data['phone_number'],
            profile_photo=self.validated_data.get('profile_photo', ''),
            country=self.validated_data.get('country', 'Ethiopia'),
            region=self.validated_data.get('region', ''),
            zone=self.validated_data.get('zone', ''),
            woreda=self.validated_data.get('woreda', ''),
            kebele=self.validated_data.get('kebele', ''),
            role=self.validated_data.get('role', 'guest'),
            user_status=self.validated_data.get('user_status', 'active')
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value

class CustomUsersUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ['email', 'name', 'phone_number', 'profile_photo', 'role']

    def validate_phone_number(self, value):
        # Add custom validation for phone_number if needed
        return value

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance