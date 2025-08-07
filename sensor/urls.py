from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorViewSet, WeatherViewSet, SensorReadingViewSet

router = DefaultRouter()
router.register(r'sensors', SensorViewSet)
router.register(r'readings', SensorReadingViewSet)
router.register(r'weather', WeatherViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
