from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.http import HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, authentication, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import ListAPIView
from .utils import get_tokens_for_user
from .serializers import RegistrationSerializer, PasswordChangeSerializer, CustomUsersUpdateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.authtoken.models import Token
from .models import CustomUsers
# Create your views here.


class RegistrationView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request):
        return render(request, 'UserManagement/user_registration.html')

    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'success': True, 
                    'success_message': "User created successfully!", 
                    'data': {
                        'id': user.id,
                        **serializer.data
                    }
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to register user',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = CustomUsers.objects.all()
    serializer_class = RegistrationSerializer


class CustomUsersUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = CustomUsers.objects.all()
    serializer_class = CustomUsersUpdateSerializer
    partial = True

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                'success': True,
                'message': 'User updated successfully',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to update user',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
      
class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        try:
            user = CustomUsers.objects.get(email=username)
        except CustomUsers.DoesNotExist:
            try:
                user = CustomUsers.objects.get(phone_naumber=username)
            except CustomUsers.DoesNotExist:
                pass
        
        if user is not None and user.check_password(password):
            return user
        return None

class LoginView(APIView):
    def get(self, request):
        return render(request, 'UserManagement/login.html')
    
    def post(self, request):
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)

        username = request.data['username']
        password = request.data['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.user_status == 'active' and user.role != 'guest':
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            profile_data = {}
            if user.profile_photo:
                # Construct the absolute URL for the profile photo
                profile_photo_url = request.build_absolute_uri(user.profile_photo.url)
                profile_data['profile_photo'] = profile_photo_url
            if user.email:
                profile_data['username'] = user.email
            elif user.phone_number:
                profile_data['phone_number'] = user.phone_number
            profile_data['role'] = user.role
            
            response_data = {'msg': 'Login Success', **profile_data, **auth_data}
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
      
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


      
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
            serializer.is_valid(raise_exception=True)
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({
                'success': True,
                "message": "Password changed successfully.",
                'data': serializer.data
                }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'success': False,
                "message": "Failed to change password.",
                "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)