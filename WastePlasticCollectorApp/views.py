from rest_framework import generics
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import WastePlastic, WastePlasticRequestor
from .serializers import WastePlasticSerializer, WastePlasticRequestorSerializer
from .forms import WastePlasticForm, WastePlasticRequestorForm


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


