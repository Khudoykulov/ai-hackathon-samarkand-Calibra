from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlantTypeViewSet, PlantProfileViewSet

router = DefaultRouter()
router.register(r'types', PlantTypeViewSet)
router.register(r'profiles', PlantProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
