from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import RegistrationView, LoginView, LogoutView,ChangePasswordView, UserListView, CustomUsersUpdateAPIView, UserDetailAPIView, PasswordResetRequestView, PasswordResetConfirmView, CustomUsersDeleteAPIView
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'UserManagement'

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('user-list', UserListView.as_view(), name='user_list'),
    path('user/update/<int:pk>/', CustomUsersUpdateAPIView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', CustomUsersDeleteAPIView.as_view(), name='delete_user'),
    path('user/<int:pk>/', UserDetailAPIView.as_view(), name='user_detail'),
    path('', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('change-password', ChangePasswordView.as_view(), name='change_password'),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
