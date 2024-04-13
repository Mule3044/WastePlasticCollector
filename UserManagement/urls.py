from django.urls import path
from .views import RegistrationView, LoginView, LogoutView,ChangePasswordView, UserListView
from rest_framework_simplejwt import views as jwt_views

app_name = 'UserManagement'

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('user-list', UserListView.as_view(), name='user_list'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('change-password', ChangePasswordView.as_view(), name='change_password'),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]