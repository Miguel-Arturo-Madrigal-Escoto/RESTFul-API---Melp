from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
# from django.contrib.gis.geos import Point
# from django.contrib.gis.measure import Distance
from geopy.distance import geodesic
from .models import Restaurant
from .serializers import RestaurantSerializer


# Create your views here.
class RestaurantsViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    @action(methods=['GET'], detail=False)
    def statistics(self, request: Request):
        pass
    