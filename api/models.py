import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    rating = models.SmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(4)
        ]
    )
    name = models.CharField(max_length=100)
    site = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    state = models.CharField(max_length=30)
    lat = models.FloatField()
    lng = models.FloatField()