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
from .serializers import RegistrationSerializer, PasswordChangeSerializer, CustomUsersUpdateSerializer,CustomUsersUpdateSerializer
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
      


class LoginView(APIView):
    def post(self, request):
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'message': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)

        username = request.data['username']
        password = request.data['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            response_data = {
                'message': 'Login Success', 
                'username': user.email, 
                'name': user.name,
                'phone_number': user.phone_number,
                'profile_photo': user.profile_photo.url if user.profile_photo else None,
                'user_status': user.user_status,
                'role': user.role,
                **auth_data}
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