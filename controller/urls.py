from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IrrigationSystemViewSet, IrrigationEventViewSet, SystemControlViewSet

router = DefaultRouter()
router.register(r'systems', IrrigationSystemViewSet)
router.register(r'events', IrrigationEventViewSet)
router.register(r'controls', SystemControlViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
