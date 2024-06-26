from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path('wasteplasticrequestor/latest/<int:requestor_id>/<str:role>/', views.FilterByLatestWastPlasticRequestorAPIView.as_view(), name='filter_by_latest'),
    path('wasteplasticrequestor/history/<int:requestor_id>/<str:role>/', views.HistoryAPIView.as_view(), name='filter_by_role'),
    path('wasteplasticrequestor/requestpickup/create/', views.RequestPickUpCreateAPIView.as_view(), name='pickup_create'),
    path('wasteplasticrequestor/requestpickup/', views.RequestPickUpListAPIView.as_view(), name='pickup_list'),
    path('wasteplasticrequestor/requestpickup/<int:requestor_id>/', views.RequestPickUpByIdListAPIView.as_view(), name='pickup_list_by_id'),
    path('wasteplasticrequestor/filterByDistance/<int:requestor_id>/', views.RequestPickUpByDistanceAPIView.as_view(), name='filter_by_distance'),
    path('wasteplasticrequestor/requestpickup/update/<int:pk>/', views.RequestPickUpUpdateAPIView.as_view(), name='pickup_update'),
    path('notifications/create/', views.NotificationListCreateView.as_view(), name='notification_create'),
    path('notifications/', views.NotificationListAPIView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/', views.NotificationRetrieveUpdateDestroyView.as_view(), name='notification_detail'),
    path('notificationsByUser/<int:user_id>/', views.NotificationListByUserAPIView.as_view(), name='notification_list_byUser'),
    path('taskassigned/<int:requestorId_id>/', views.TaskAssignedListAPIView.as_view(), name='taskassigned_list'),
    path('taskassigned/update/<int:requestor_id>/', views.TaskAssignedUpdateAPIView.as_view(), name='taskassigned_update'),
    path('contentManagement/', views.ContentManagementListAPIView.as_view(), name='content_management'),
    path('wastePlasticType/', views.WastePlasticTypeListAPIView.as_view(), name='wastePlastic_type'),


    #Dashboard
    path('index/', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('', views.dashboard_content, name='dashboard'),
    path('users/', views.user_management, name='user_manage'),
    path('agents/', views.agent_management, name='agent_manage'),
    path('collection-request/', views.collection_request, name='collection_request'),
    path('feedback/', views.feedback, name='feedback'),
    path('content/', views.content_management, name='content_management'),
    path('report/', views.report_content, name='report'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
