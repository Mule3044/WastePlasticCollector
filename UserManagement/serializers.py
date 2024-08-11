from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import serializers
from .models import CustomUsers
from django.conf import settings


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUsers
        fields = ['id','email', 'name', 'phone_number', 'profile_photo', 'latitude', 'longitude' ,'role', 'password', 'password2']
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
            latitude=self.validated_data.get('latitude', ''),
            longitude=self.validated_data.get('longitude', ''),
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


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUsers.objects.get(email=value)
        except CustomUsers.DoesNotExist:
            raise serializers.ValidationError("No user associated with this email address")
        return value

    def save(self):
        user = CustomUsers.objects.get(email=self.validated_data['email'])
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_message = f"Use the following token to reset your password:\n\nToken: {token}\nUID: {uid}"

        send_mail(
            'Password Reset Request',
            reset_message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def save(self):
        try:
            uid = force_str(urlsafe_base64_decode(self.validated_data['uid']))
            user = CustomUsers.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUsers.DoesNotExist):
            raise serializers.ValidationError("Invalid uid")
        
        if not default_token_generator.check_token(user, self.validated_data['token']):
            raise serializers.ValidationError("Invalid token")
        
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class CustomUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ['id', 'email', 'name', 'phone_number', 'role', 'user_status']


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


class AgentLocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ['id','latitude', 'longitude']

    def update(self, instance, validated_data):
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.save()
        return instance


class CustomUsersDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ['id','email', 'name', 'phone_number', 'profile_photo', 'country', 'region', 'zone', 'woreda', 'kebele', 'latitude', 'longitude', 'role', 'user_status']
