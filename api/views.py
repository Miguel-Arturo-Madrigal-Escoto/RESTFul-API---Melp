from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
# from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
#from django.contrib.gis.db.models.functions import Distance
from .models import Restaurant
from .serializers import RestaurantSerializer
from geopy.distance import geodesic


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
        latitude = float(request.query_params.get('latitude'))
        longitude = float(request.query_params.get('longitude'))
        radius = float(request.query_params.get('radius'))

        location = Point(longitude, latitude)
        restaurants_filtered = Restaurant.objects.filter(location__distance_lte=(location, Distance(m=radius)))
        return Response(restaurants_filtered.count())
    
