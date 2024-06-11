from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
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
from .documentation import ENDPOINTS_DOCUMENTATION


# Create your views here.
class HealthCheck(APIView):
    @extend_schema(
        description=ENDPOINTS_DOCUMENTATION['health']['description'],
        responses=ENDPOINTS_DOCUMENTATION['health']['responses']
    )
    def get(self, request: Request):
        return Response(RESTAURANT_HEALTH_CHECK, status=status.HTTP_200_OK)
    
    
class RestaurantsViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    @extend_schema(
        description=ENDPOINTS_DOCUMENTATION['list']['description'],
        responses=ENDPOINTS_DOCUMENTATION['list']['responses']
    )
    def list(self, request: Request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @extend_schema(
        description=ENDPOINTS_DOCUMENTATION['retrieve']['description'],
        responses=ENDPOINTS_DOCUMENTATION['retrieve']['responses']
    )
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
    

    @extend_schema(
        description=ENDPOINTS_DOCUMENTATION['create']['description'],
        responses=ENDPOINTS_DOCUMENTATION['create']['responses']
    )
    def create(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @extend_schema(
        description=ENDPOINTS_DOCUMENTATION['partial_update']['description'],
        responses=ENDPOINTS_DOCUMENTATION['partial_update']['responses']
    )
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
    

    @extend_schema(
        description=ENDPOINTS_DOCUMENTATION['destroy']['description'],
        responses=ENDPOINTS_DOCUMENTATION['destroy']['responses']
    )
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


    @extend_schema(
        description=ENDPOINTS_DOCUMENTATION['statistics']['description'],
        responses=ENDPOINTS_DOCUMENTATION['statistics']['responses'],
        parameters=ENDPOINTS_DOCUMENTATION['statistics']['parameters']
    )
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
