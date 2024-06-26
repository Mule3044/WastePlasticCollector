from rest_framework import generics
from django.db.models import Q
from django.db.models import Sum, Count
from django.utils import timezone
from django.db.models.functions import TruncMonth, TruncDay
import datetime
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models.functions import Cast
from django.db.models import FloatField
from geopy.distance import geodesic
from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import WastePlastic, WastePlasticRequestor, Notification, RequestPickUp, LookUp, TaskAssigned, FeedBack, ContentManagement, WastePlasticType
from .serializers import WastePlasticSerializer, WastePlasticRequestorCreateSerializer, WastePlasticRequestorListSerializer, NotificationSerializer, RequestPickUpSerializer, TaskAssignedSerializer, ContentManagementSerializer, WastePlasticTypeSerializer
from UserManagement.models import CustomUsers

# def index(request):
#     return render(request, 'WastePlasticCollectorApp/index.html')

def home(request):
    return render(request, 'WastePlasticCollectorApp/index.html')

def index(request):
    return render(request, 'WastePlasticCollectorApp/base_template.html')

def dashboard_content(request):
    login_user = request.user
    photo = login_user.profile_photo.url if login_user.profile_photo else None

    # Print the photo URL if it exists, otherwise print a message
    if photo:
        print(photo)
    else:
        print("No profile photo available")
        
    all_user_count = CustomUsers.objects.all().count()
    request_pickup_count = RequestPickUp.objects.all().count()
    collection_count = WastePlasticRequestor.objects.all().count()
    latest_tasks = TaskAssigned.objects.all().order_by('-assigned_date')[:10]
    assigned_task_count = TaskAssigned.objects.filter(task_status='completed').count()

    collectedWastPlastcs = WastePlasticRequestor.objects.all()

    total_collection = sum(item.wastePlastic_size for item in collectedWastPlastcs)
    carbon_emission = total_collection * 4.03239  # Conversion factor: 1kg of PET plastic = 4.03239kg of CO2

    # Retrieve the unit_price from the LookUp table
    lookup = get_object_or_404(LookUp)
    unit_price = lookup.unit_price

    # Calculate the reward
    reward = total_collection * unit_price

    today = timezone.now().date()
    one_week_ago = today - datetime.timedelta(days=7)

    # Fetch and aggregate data
    activity_data = (
        TaskAssigned.objects.filter(task_status='completed', assigned_date__range=(one_week_ago, today))
        .values('assigned_date')
        .annotate(total_size=Sum('requestId__wastePlastic_size'))
        .order_by('assigned_date')
    )

    # Prepare data for the graph
    week_days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    counts = {day: 0 for day in week_days}
    for data in activity_data:
        day_of_week = data['assigned_date'].strftime("%a").upper()[:3]
        counts[day_of_week] = max(0, round(data['total_size']))
    
    # Calculate monthly carbon emissions for the past year
    one_year_ago = today - datetime.timedelta(days=365)
    monthly_emissions = (
        WastePlasticRequestor.objects.filter(request_date__gte=one_year_ago)
        .annotate(month=TruncMonth('request_date'))
        .values('month')
        .annotate(total_size=Sum('wastePlastic_size'))
        .order_by('month')
    )

    # Prepare data for the monthly graph
    months = [
        'September', 'October', 'November', 'December', 'January', 'February', 
        'March', 'April', 'May', 'June', 'July', 'August'
    ]
    month_counts = {month: 0 for month in months}
    for data in monthly_emissions:
        month_name = data['month'].strftime("%B")
        if month_name in month_counts:
            month_counts[month_name] = max(0, round(data['total_size'] * 4.03239))


    context = {
        "login_user": login_user,
        "photo": photo,
        "all_user_count": all_user_count,
        "request_pickup_count": request_pickup_count,
        "collection_count": collection_count,
        "latest_tasks": latest_tasks,
        "total_collection": total_collection,
        "carbon_emission": carbon_emission,
        "reward": reward,
        "assigned_task_count":assigned_task_count,
        'days': list(counts.keys()),
        'counts': list(counts.values()),
        'months': list(month_counts.keys()),
        'month_counts': list(month_counts.values())
    }
    return render(request, "WastePlasticCollectorApp/dashboard_content.html", context)

def report_content(request):
    assigned_task_count = TaskAssigned.objects.filter(task_status='completed').count()
    today = timezone.now().date()
    one_week_ago = today - datetime.timedelta(days=7)

    # Fetch and aggregate data
    activity_data = (
        TaskAssigned.objects.filter(task_status='completed', assigned_date__range=(one_week_ago, today))
        .values('assigned_date')
        .annotate(total_size=Sum('requestId__wastePlastic_size'))
        .order_by('assigned_date')
    )

    # Prepare data for the graph
    week_days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    counts = {day: 0 for day in week_days}
    for data in activity_data:
        day_of_week = data['assigned_date'].strftime("%a").upper()[:3]
        counts[day_of_week] = max(0, round(data['total_size']))
    
    # Calculate monthly carbon emissions for the past year
    one_year_ago = today - datetime.timedelta(days=365)
    monthly_emissions = (
        WastePlasticRequestor.objects.filter(request_date__gte=one_year_ago)
        .annotate(month=TruncMonth('request_date'))
        .values('month')
        .annotate(total_size=Sum('wastePlastic_size'))
        .order_by('month')
    )

    # Prepare data for the monthly graph
    months = [
        'September', 'October', 'November', 'December', 'January', 'February', 
        'March', 'April', 'May', 'June', 'July', 'August'
    ]
    month_counts = {month: 0 for month in months}
    for data in monthly_emissions:
        month_name = data['month'].strftime("%B")
        if month_name in month_counts:
            month_counts[month_name] = max(0, round(data['total_size'] * 4.03239))


    context = {
        "assigned_task_count":assigned_task_count,
        'days': list(counts.keys()),
        'counts': list(counts.values()),
        'months': list(month_counts.keys()),
        'month_counts': list(month_counts.values())
    }
    return render(request, "WastePlasticCollectorApp/report_template.html", context)

def user_management(request):
    users = CustomUsers.objects.all()
    # Sum wastePlastic_size by requestor
    waste_plastic_sums = WastePlasticRequestor.objects.values('requestor').annotate(total_size=Sum('wastePlastic_size'))

    # Create a dictionary to easily look up the sum by requestor
    waste_plastic_sums_dict = {entry['requestor']: entry['total_size'] for entry in waste_plastic_sums}
    context = {
        "users": users,
        "waste_plastic_sums": waste_plastic_sums_dict,
    }
    return render(request, "WastePlasticCollectorApp/user_manage_template.html", context)

def agent_management(request):
    agents = CustomUsers.objects.filter(role="agent")

    # Aggregate wastePlastic_size by agent
    agent_waste_sums = WastePlasticRequestor.objects.filter(requestor__in=agents).values('requestor__id').annotate(total_waste=Sum('wastePlastic_size'))

    # Aggregate assigned tasks count by agent
    agent_task_counts = TaskAssigned.objects.filter(userId__in=agents).values('userId__id').annotate(total_tasks=Count('id'))

    # Create dictionaries to map agent IDs to their respective totals
    agent_waste_dict = {entry['requestor__id']: entry['total_waste'] for entry in agent_waste_sums}
    agent_task_count_dict = {entry['userId__id']: entry['total_tasks'] for entry in agent_task_counts}

    context = {
        "agents": agents,
        "agent_waste_dict": agent_waste_dict,
        "agent_task_count_dict": agent_task_count_dict,
    }
    return render(request, "WastePlasticCollectorApp/agent_manage_template.html", context)

def collection_request(request):
    assigned_agents = TaskAssigned.objects.all()

    context = {
        "assigned_agents": assigned_agents,
    }
    return render(request, "WastePlasticCollectorApp/collection_request_template.html", context)

def feedback(request):
    feedbaks = FeedBack.objects.all()

    context = {
        "feedbaks": feedbaks,
    }
    return render(request, "WastePlasticCollectorApp/feedback_template.html", context)

def content_management(request):
    contents = ContentManagement.objects.all()

    context = {
        "contents": contents,
    }
    return render(request, "WastePlasticCollectorApp/content_management_template.html", context)

class WastePlasticCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = WastePlastic.objects.all()
    serializer_class = WastePlasticSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'success': True,
                'message': 'Waste plastic created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to create waste plastic',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class WastePlasticListAPIView(generics.ListAPIView):
    queryset = WastePlastic.objects.all()
    serializer_class = WastePlasticSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve waste plastic list',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WastePlasticDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = WastePlastic.objects.all()
    serializer_class = WastePlasticSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'success': True,
                'message': 'Waste plastic details retrieved successfully',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve waste plastic details',
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)


class WastePlasticUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = WastePlastic.objects.all()
    serializer_class = WastePlasticSerializer
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
                'message': 'Waste plastic updated successfully',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to update waste plastic',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class WastePlasticDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = WastePlastic.objects.all()
    serializer_class = WastePlasticSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'success': True,
                'message': 'Waste plastic deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to delete waste plastic',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)



class WastePlasticRequestorCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = WastePlasticRequestor.objects.all()
    serializer_class = WastePlasticRequestorCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'success': True,
                'message': 'Waste plastic requestor created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to create waste plastic requestor',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class WastePlasticRequestorListAPIView(generics.ListAPIView):
    queryset = WastePlasticRequestor.objects.all()
    serializer_class = WastePlasticRequestorListSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve waste plastic requestor list',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WastePlasticRequestorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = WastePlasticRequestor.objects.all()
    serializer_class = WastePlasticRequestorListSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'success': True,
                'message': 'Waste plastic requestor details retrieved successfully',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve waste plastic requestor details',
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)


class WastePlasticRequestorUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = WastePlasticRequestor.objects.all()
    serializer_class = WastePlasticRequestorCreateSerializer
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
                'message': 'Waste plastic requestor updated successfully',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to update waste plastic requestor',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class WastePlasticRequestorDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = WastePlasticRequestor.objects.all()
    serializer_class = WastePlasticRequestorCreateSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'success': True,
                'message': 'Waste plastic requestor deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to delete waste plastic requestor',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class FilterByLatestWastPlasticRequestorAPIView(generics.ListAPIView):
    queryset = WastePlasticRequestor.objects.all()
    serializer_class = WastePlasticRequestorCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        try:
            requestor_id = self.kwargs.get('requestor_id')
            role = self.kwargs.get('role')
            queryset = WastePlasticRequestor.objects.filter(requestor_id=requestor_id, requestor__role=role)
            return queryset
        except Exception as e:
            return WastePlasticRequestor.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset().order_by('-request_date')[:10]
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve latest waste plastic requestors',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HistoryAPIView(generics.ListAPIView):
    serializer_class = WastePlasticRequestorCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        try:
            requestor_id = self.kwargs.get('requestor_id')
            role = self.kwargs.get('role')
            queryset = WastePlasticRequestor.objects.filter(requestor_id=requestor_id, requestor__role=role)
            return queryset
        except Exception as e:
            return WastePlasticRequestor.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            
            total_collection = sum(item['wastePlastic_size'] for item in serializer.data)
            carbon_emission = total_collection * 4.03239  # Conversion factor: 1kg of PET plastic = 4.03239kg of CO2

            # Retrieve the unit_price from the LookUp table
            lookup = get_object_or_404(LookUp)
            unit_price = lookup.unit_price

            # Calculate the reward
            reward = total_collection * unit_price
            
            return Response({
                'success': True,
                'data': serializer.data,
                'total_collection': total_collection,
                'carbon_emission': carbon_emission,
                'reward': reward
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve waste plastic requestors',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'success': True, 
                'message': 'Notification created successfully', 
                'data': serializer.data
                }, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({
                'success': False, 
                'message': 'Failed to create notification', 
                'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

class NotificationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'success': True, 
                'message': 'Notification deleted successfully'
                }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'success': False, 
                'message': 'Failed to delete notification', 
                'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)



class NotificationListAPIView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve notification',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NotificationListByUserAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        try:
            user_id = self.kwargs.get('user_id')
            queryset = Notification.objects.filter(userId_id=user_id)
            return queryset
        except Exception as e:
            return Notification.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve notifications',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RequestPickUpCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = RequestPickUp.objects.all()
    serializer_class = RequestPickUpSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'success': True,
                'message': 'Request PickUp created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to create request pick up',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class RequestPickUpListAPIView(generics.ListAPIView):
    queryset = RequestPickUp.objects.all()
    serializer_class = RequestPickUpSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RequestPickUpByIdListAPIView(generics.ListAPIView):
    queryset = RequestPickUp.objects.all()
    serializer_class = RequestPickUpSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        try:
            requestor_id = self.kwargs.get('requestId')
            queryset = WastePlasticRequestor.objects.filter(requestor_id=requestor_id, requestor__role="agent")
            return queryset
        except Exception as e:
            return WastePlasticRequestor.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RequestPickUpByDistanceAPIView(generics.ListAPIView):
    serializer_class = RequestPickUpSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        requestor_id = self.kwargs.get('requestor_id')
        requestor = WastePlasticRequestor.objects.get(id=requestor_id)
        requestor_coords = (requestor.latitude, requestor.longitude)
        
        # Annotate and order RequestPickUp instances by distance
        return RequestPickUp.objects.all().annotate(
            distance=Cast(
                (requestor.latitude - models.F('latitude')) ** 2 + 
                (requestor.longitude - models.F('longitude')) ** 2,
                FloatField()
            )
        ).order_by('distance')[:3]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve request pickups by distance',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RequestPickUpUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = RequestPickUp.objects.all()
    serializer_class = RequestPickUpSerializer
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
                'message': 'Request pick up updated successfully',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to update request pick up',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class TaskAssignedListAPIView(generics.ListAPIView):
    queryset = TaskAssigned.objects.all()
    serializer_class = TaskAssignedSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        try:
            requestor_id = self.kwargs.get('requestorId_id')
            queryset = TaskAssigned.objects.filter(requestId__requestor_id=requestor_id, requestId__requestor__role="agent")
            return queryset
        except Exception as e:
            return TaskAssigned.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve task assigned data',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskAssignedUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = TaskAssigned.objects.all()
    serializer_class = TaskAssignedSerializer
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
                'message': 'Task assigned updated successfully',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to update task assigned',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ContentManagementListAPIView(generics.ListAPIView):
    queryset = ContentManagement.objects.all()
    serializer_class = ContentManagementSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WastePlasticTypeListAPIView(generics.ListAPIView):
    queryset = WastePlasticType.objects.all()
    serializer_class = WastePlasticTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)