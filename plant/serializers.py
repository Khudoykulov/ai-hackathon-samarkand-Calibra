from rest_framework import serializers
from .models import PlantType, PlantProfile

class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantType
        fields = '__all__'

class PlantProfileSerializer(serializers.ModelSerializer):
    plant_type = PlantTypeSerializer(read_only=True)
    
    class Meta:
        model = PlantProfile
        fields = '__all__'
