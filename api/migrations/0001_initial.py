# Generated by Django 5.0.6 on 2024-06-11 06:26

import django.contrib.gis.db.models.fields
import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('rating', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)])),
                ('name', models.CharField(max_length=100)),
                ('site', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=30)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
    ]
