from rest_framework import serializers
from .models import Sensor, SensorReading, WeatherData, WeatherForecast


class SensorSerializer(serializers.ModelSerializer):
    sensor_type_display = serializers.CharField(source='get_sensor_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Sensor
        fields = '__all__'


class SensorReadingSerializer(serializers.ModelSerializer):
    sensor_name = serializers.CharField(source='sensor.name', read_only=True)
    sensor_type = serializers.CharField(source='sensor.sensor_type', read_only=True)

    class Meta:
        model = SensorReading
        fields = '__all__'


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'


class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = '__all__'


class DashboardDataSerializer(serializers.Serializer):
    current_weather = WeatherDataSerializer()
    sensor_readings = SensorReadingSerializer(many=True)
    forecast = WeatherForecastSerializer(many=True)
    system_status = serializers.DictField()
