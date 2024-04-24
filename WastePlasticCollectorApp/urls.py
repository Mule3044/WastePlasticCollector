from django.urls import path
from . import views

urlpatterns = [
    # API endpoints for WastePlastic model
    path('wasteplastic/', views.WastePlasticListAPIView.as_view(), name='wasteplastic_list'),
    path('wasteplastic/create/', views.WastePlasticCreateAPIView.as_view(), name='wasteplastic_create'),
    path('wasteplastic/<int:pk>/', views.WastePlasticDetailAPIView.as_view(), name='wasteplastic_detail'),
    path('wasteplastic/update/<int:pk>/', views.WastePlasticUpdateAPIView.as_view(), name='wasteplastic_update'),
    path('wasteplastic/delete/<int:pk>/', views.WastePlasticDeleteAPIView.as_view(), name='wasteplastic_delete'),

    # API endpoints for WastePlasticRequestor
    path('wasteplasticrequestor/', views.WastePlasticRequestorListAPIView.as_view(), name='wasteplasticrequestor_list'),
    path('wasteplasticrequestor/create/', views.WastePlasticRequestorCreateAPIView.as_view(), name='wasteplasticrequestor_create'),
    path('wasteplasticrequestor/<int:pk>/', views.WastePlasticRequestorDetailAPIView.as_view(), name='wasteplasticrequestor_detail'),
    path('wasteplasticrequestor/update/<int:pk>/', views.WastePlasticRequestorUpdateAPIView.as_view(), name='wasteplasticrequestor_update'),
    path('wasteplasticrequestor/delete/<int:pk>/', views.WastePlasticRequestorDeleteAPIView.as_view(), name='wasteplasticrequestor_delete'),
    path('home/', views.index, name='index'),
    path('notifications/', views.NotificationListCreateView.as_view(), name='notification_create'),
    path('notifications/<int:pk>/', views.NotificationRetrieveUpdateDestroyView.as_view(), name='notification_detail'),
]
