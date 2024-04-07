from django.contrib.auth.backends import ModelBackend
from .models import CustomUsers

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        try:
            user = CustomUsers.objects.get(email=username)
        except CustomUsers.DoesNotExist:
            try:
                user = CustomUsers.objects.get(phone_number=username)
            except CustomUsers.DoesNotExist:
                pass
        
        if user is not None and user.check_password(password):
            return user
        return None
