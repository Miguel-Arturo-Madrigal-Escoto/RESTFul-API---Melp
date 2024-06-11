from rest_framework.routers import DefaultRouter
from .views import RestaurantsViewSet


router = DefaultRouter()
router.register('restaurants', RestaurantsViewSet)

urlpatterns = router.urls
