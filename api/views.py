from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Restaurant
from .serializers import RestaurantSerializer
from .validators import Validators
from .services import StatisticsService
from .constants import (
    RESTAURANT_STATISTICS_FORMAT_ERR,
    RESTAURANT_INTERNAL_SERVER_ERR,
    RESTAURANT_NOT_FOUND,
    RESTAURANT_HEALTH_CHECK
)


# Create your views here.
class HealthCheck(APIView):
    def get(self, request: Request):
        return Response(RESTAURANT_HEALTH_CHECK, status=status.HTTP_200_OK)
    
    
class RestaurantsViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def list(self, request: Request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request: Request, pk=None):
        Validators.validate_uuid(pk)
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            serializer = self.get_serializer(restaurant, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response(RESTAURANT_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(RESTAURANT_INTERNAL_SERVER_ERR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request: Request, pk=None):
        Validators.validate_uuid(pk)
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            serializer = self.get_serializer(restaurant, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Restaurant.DoesNotExist:
            return Response(RESTAURANT_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(RESTAURANT_INTERNAL_SERVER_ERR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
    def destroy(self, request: Request, pk=None):
        Validators.validate_uuid(pk)
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            restaurant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Restaurant.DoesNotExist:
            return Response(RESTAURANT_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(RESTAURANT_INTERNAL_SERVER_ERR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

    @action(methods=['GET'], detail=False)
    def statistics(self, request: Request):
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        radius = request.query_params.get('radius', None)

        try:
            count, restaurant_ids = StatisticsService.get_neighbor_restaurants(
                float(latitude),
                float(longitude),
                float(radius)
            )
            average = StatisticsService.calculate_avg_rating(restaurant_ids)
            std = StatisticsService.calculate_stdev_rating(restaurant_ids)
            response = { 'count': count, 'avg': average, 'std': std }
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response(RESTAURANT_STATISTICS_FORMAT_ERR, status=status.HTTP_400_BAD_REQUEST)
