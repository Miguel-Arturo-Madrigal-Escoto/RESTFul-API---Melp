from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
from .models import Restaurant
from .serializers import RestaurantSerializer
from .services import StatisticsService
from .constants import RESTAURANT_STATISTICS_ERR

# 1. CREATE USER miguel WITH PASSWORD 'postgres';
# 2. ALTER ROLE <user_name> SUPERUSER;

# 3. sudo apt-get install postgis*
# 4. sudo apt-get install binutils libproj-dev gdal-bin

# Create your views here.
class RestaurantsViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

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
            return Response(RESTAURANT_STATISTICS_ERR, status=status.HTTP_400_BAD_REQUEST)
    
