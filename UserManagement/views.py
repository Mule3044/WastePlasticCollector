from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.backends import ModelBackend
from django.http import HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, status, authentication, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .utils import get_tokens_for_user
from .serializers import RegistrationSerializer, PasswordChangeSerializer, CustomUsersUpdateSerializer,CustomUsersUpdateSerializer, CustomUsersDetailSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer, CustomUsersDeleteSerializer
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


class CustomUsersUpdateAPIView(LoginRequiredMixin, generics.RetrieveUpdateAPIView):
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


class CustomUsersDeleteAPIView(LoginRequiredMixin, generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = CustomUsers.objects.all()
    serializer_class = CustomUsersDeleteSerializer

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'success': True,
                'message': 'User deleted successfully'
            }, status=status.HTTP_200_OK)
        except CustomUsers.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to delete user',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.delete()


class CheckUserExistsView(APIView):
    """
    Endpoint to check if a user exists based on email or phoneNumber.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # Get the email or username from the request data
        identifier = request.data.get('email') or request.data.get('phone_number')
        
        if not identifier:
            return Response({
                'success': False,
                'message': 'Email or Username is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user exists
        user_exists = CustomUsers.objects.filter(email=identifier).exists() or \
                      CustomUsers.objects.filter(phone_number=identifier).exists()

        if user_exists:
            return Response({
                'success': True,
                'message': 'User exists.'
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'message': 'User does not exist.'
        }, status=status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    def get(self, request):
        return render(request, 'UserManagement/login.html')
    def post(self, request):
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'message': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)

        username = request.data['username']
        password = request.data['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)            
            auth_data = get_tokens_for_user(request.user)
            response = Response({
                'message': 'Login Success', 
                'id': user.id, 
                'username': user.email, 
                'name': user.name,
                'phone_number': user.phone_number,
                'profile_photo': user.profile_photo.url if user.profile_photo else None,
                'user_status': user.user_status,
                'role': user.role,
                **auth_data}, status=status.HTTP_200_OK)

            # Set tokens as cookies
            response.set_cookie('access_token', auth_data['access_token'], httponly=True)
            response.set_cookie('refresh_token', auth_data['refresh_token'], httponly=True)

            return response
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


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = CustomUsers.objects.all()
    serializer_class = CustomUsersDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'success': True,
                'message': 'User details retrieved successfully',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve user details',
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)


class PasswordResetRequestView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Password reset link sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
