from rest_framework import generics
from django.db.models import Q
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from .models import WastePlastic, WastePlasticRequestor, Notification, RequestPickUp
from .serializers import WastePlasticSerializer, WastePlasticRequestorSerializer, NotificationSerializer, RequestPickUpSerializer
from UserManagement.models import CustomUsers


def index(request):
    return render(request, 'WastePlasticCollectorApp/index.html')

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
    serializer_class = WastePlasticRequestorSerializer

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
    serializer_class = WastePlasticRequestorSerializer
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
    serializer_class = WastePlasticRequestorSerializer

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
    serializer_class = WastePlasticRequestorSerializer
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
    serializer_class = WastePlasticRequestorSerializer

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
    serializer_class = WastePlasticRequestorSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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



class FilterByRoleAndUserIdAPIView(generics.ListAPIView):
    serializer_class = WastePlasticRequestorSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        try:
            # Get the requestor_id from URL parameter
            requestor_id = self.kwargs.get('requestor_id')

            # Filter WastePlasticRequestor objects by requestor_id
            queryset = WastePlasticRequestor.objects.filter(requestor_id=requestor_id, requestor__role='agent')
            return queryset
        except Exception as e:
            # Return an empty queryset if there's an error
            return WastePlasticRequestor.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            waste_plastic_collection = serializer.data
            print(waste_plastic_collection)
            total_collection=0
            # carbon_emition = total_collection/1000
            for i in serializer.data:
                total_collection += i['wastePlastic_size']
            return Response({
                'success': True,
                'data': serializer.data,
                'total_collection': total_collection,
                'carbon_emition': total_collection/100
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