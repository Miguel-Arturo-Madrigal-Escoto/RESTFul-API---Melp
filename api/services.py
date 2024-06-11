from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.db.models import Avg
from django.db.models import StdDev
from .models import Restaurant


class StatisticsService:

    @staticmethod
    def get_neighbor_restaurants(latitude: float, longitude: float, radius: float) -> tuple:
        """
            Returns the number of restaurants that fall inside the circle with center [x,y] 
            and radius z.
        """
        center = Point(longitude, latitude)
        restaurants_filtered = Restaurant.objects.filter(
            location__distance_lte=(center, Distance(m=radius))
        )

        count_filtered = restaurants_filtered.count()
        restaurant_uuids = restaurants_filtered.values_list('id')

        return (count_filtered, restaurant_uuids)
    

    @staticmethod
    def calculate_avg_rating(restaurant_ids: list) -> float:
        """
            Returns the average rating of restaurants inside the circle.
        """
        rating = Restaurant.objects.filter(id__in=restaurant_ids).aggregate(avg=Avg('rating'))
        return rating['avg']
    

    @staticmethod
    def calculate_stdev_rating(restaurant_ids: list) -> float:
        """
            Returns the standard deviation of rating of restaurants inside the circle.
        """
        rating = Restaurant.objects.filter(id__in=restaurant_ids).aggregate(stdev=StdDev('rating'))
        return rating['stdev']
    
