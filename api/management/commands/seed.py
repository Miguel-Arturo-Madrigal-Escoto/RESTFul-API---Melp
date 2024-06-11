from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.gis.geos import Point
from api.models import Restaurant
import pandas as pd


class Command(BaseCommand):
    help = 'Seeds the database with the CSV content.'

    def handle(self, *args, **kwargs):
        restaurants_file = f'{ settings.BASE_DIR }/restaurantes.csv'
        restaurants_data = pd.read_csv(restaurants_file)

        restaurants = [
            Restaurant(
                id=row['id'],
                rating=row['rating'],
                name=row['name'],
                site=row['site'],
                email=row['email'],
                phone=row['phone'],
                street=row['street'],
                city=row['city'],
                state=row['state'],
                lat=row['lat'],
                lng=row['lng'],
                location=Point(row['lng'], row['lat'])
            )
            for _, row in restaurants_data.iterrows()
        ]

        Restaurant.objects.bulk_create(restaurants)
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded { len(restaurants) } restaurants.'))