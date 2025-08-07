from rest_framework import viewsets
from .models import PlantType, PlantProfile
from .serializers import PlantTypeSerializer, PlantProfileSerializer

class PlantTypeViewSet(viewsets.ModelViewSet):
    queryset = PlantType.objects.all()
    serializer_class = PlantTypeSerializer

class PlantProfileViewSet(viewsets.ModelViewSet):
    queryset = PlantProfile.objects.all()
    serializer_class = PlantProfileSerializer
