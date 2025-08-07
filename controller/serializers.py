from rest_framework import serializers
from .models import IrrigationSystem, IrrigationEvent, SystemControl

class IrrigationSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrrigationSystem
        fields = '__all__'

class IrrigationEventSerializer(serializers.ModelSerializer):
    system_name = serializers.CharField(source='system.name', read_only=True)
    
    class Meta:
        model = IrrigationEvent
        fields = '__all__'

class SystemControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemControl
        fields = '__all__'
