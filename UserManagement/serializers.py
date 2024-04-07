from rest_framework import serializers
from .models import CustomUsers


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUsers
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'country', 'region', 'zone', 'woreda', 'kebele', 'role', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = CustomUsers(
            email=self.validated_data['email'],
            first_name=self.validated_data.get('first_name', ''),
            last_name=self.validated_data.get('last_name', ''),
            phone_number=self.validated_data['phone_number'],
            country=self.validated_data.get('country', 'Ethiopia'),
            region=self.validated_data.get('region', ''),
            zone=self.validated_data.get('zone', ''),
            woreda=self.validated_data.get('woreda', ''),
            kebele=self.validated_data.get('kebele', ''),
            role=self.validated_data.get('role', 'guest')
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