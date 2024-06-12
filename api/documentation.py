from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from api.constants import (
    RESTAURANT_STATISTICS_FORMAT_ERR,
    RESTAURANT_NOT_FOUND,
    RESTAURANT_INTERNAL_SERVER_ERR,
    RESTAURANT_HEALTH_CHECK
)
from .serializers import RestaurantSerializer


ENDPOINTS_DOCUMENTATION = {
    'health': {
        'description': 'Returns a 200 - OK response if the application is up and running.',
        'responses': {
            200: {
                'example': RESTAURANT_HEALTH_CHECK
            }
        }
    },
    'list': {
        'description': 'Retrieves all the restaurants',
        'responses': {
            200: {
                'example': [
                    {
                        "id": "4e17896d-a26f-44ae-a8a4-5fbd5cde79b0",
                        "rating": 0,
                        "name": "Hernández - Lira",
                        "site": "http://graciela.com.mx",
                        "email": "Brandon_Vigil@hotmail.com",
                        "phone": "570 746 998",
                        "city": "Mateofurt",
                        "street": "93725 Erick Arroyo",
                        "state": "Hidalgo",
                        "lat": 19.437904276995,
                        "lng": -99.1286576775023
                    },
                    {
                        "id": "2b8f5a44-1e8b-44ec-9b25-0edc5b64b7e6",
                        "rating": 3,
                        "name": "Hurtado, Rolón and Segovia",
                        "site": "https://elías.org",
                        "email": "RosaMara_Figueroa@corpfolder.com",
                        "phone": "559.867.074",
                        "city": "Marco Antonioland",
                        "street": "039 Susana Polígono",
                        "state": "Colima",
                        "lat": 19.433497663015,
                        "lng": -99.1285135065721
                    },
                ]
            }
        }
    },
    'retrieve': {
        'description': 'Retrieves the restaurant with the given UUID if exists.',
        'responses': {
            200: RestaurantSerializer,
            404: {
                'example': RESTAURANT_NOT_FOUND
            },
            500: {
                'example': RESTAURANT_INTERNAL_SERVER_ERR
            }
        }
    },
    'create': {
        'description': 'Creates a new restaurant in the database based on the provided JSON in the body object.',
        'responses': {
            200: RestaurantSerializer,
            400: {
                'example': {
                    "rating": [
                        "Ensure this value is less than or equal to 4."
                    ],
                    "name": [
                        "This field may not be blank."
                    ],
                    "site": [
                        "This field may not be blank."
                    ],
                    "email": [
                        "Enter a valid email address."
                    ],
                    "phone": [
                        "This field may not be blank."
                    ],
                    "city": [
                        "This field may not be blank."
                    ],
                    "street": [
                        "This field may not be blank."
                    ],
                    "state": [
                        "This field may not be blank."
                    ],
                    "lat": [
                        "A valid number is required."
                    ],
                    "lng": [
                        "A valid number is required."
                    ]
                }
            }
        }
    },
    'partial_update': {
        'description': 'Updates the restaurant with the given UUID based on the provided JSON in the body object.',
        'responses': {
            200: RestaurantSerializer,
            404: {
                'example': RESTAURANT_NOT_FOUND
            },
            500: {
                'example': RESTAURANT_INTERNAL_SERVER_ERR
            }
        }
    },
    'destroy': {
        'description': 'Deletes the restaurant with the given UUID.',
        'responses': {
            204: {
                'example': ''
            },
            404: {
                'example': RESTAURANT_NOT_FOUND
            },
            500: {
                'example': RESTAURANT_INTERNAL_SERVER_ERR
            }
        }
    },
    'statistics': {
        'description': 'Returns the neighbor restaurants inside the [x,y] center within a specific radius, as \
            well as the average rating inside the circle and the standard derivation of the arting.',
        'responses': {
            200: {
                'example': {
                    'count': 10,
                    'avg': 2.3,
                    'std': 1.4
                }
            },
            404: {
                'example': RESTAURANT_STATISTICS_FORMAT_ERR
            }
        },
        'parameters': [
            OpenApiParameter(
                name='latitude',
                type=OpenApiTypes.FLOAT,
                location=OpenApiParameter.QUERY,
                examples=[
                    OpenApiExample(
                        name='Latitude example',
                        value=19.4392401826759
                    ),
                ]
            ),
            OpenApiParameter(
                name='longitude',
                type=OpenApiTypes.FLOAT,
                location=OpenApiParameter.QUERY,
                examples=[
                    OpenApiExample(
                        name='Longitude example',
                        value=-99.1331904409434
                    ),
                ]
            ),
            OpenApiParameter(
                name='radius',
                type=OpenApiTypes.FLOAT ,
                location=OpenApiParameter.QUERY,
                description='Radius',
                examples=[
                    OpenApiExample(
                        name='Radius example',
                        value=1000
                    ),
                ]
            )
        ]
    }
}