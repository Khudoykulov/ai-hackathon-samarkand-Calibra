from django.db import models
from django.utils import timezone
import uuid


class SensorType(models.TextChoices):
    SOIL_MOISTURE = 'soil_moisture', 'Soil Moisture'
    SOIL_TEMPERATURE = 'soil_temperature', 'Soil Temperature'
    AIR_TEMPERATURE = 'air_temperature', 'Air Temperature'
    AIR_HUMIDITY = 'air_humidity', 'Air Humidity'
    PH_LEVEL = 'ph_level', 'pH Level'
    CONDUCTIVITY = 'conductivity', 'Conductivity'
    LIGHT_INTENSITY = 'light_intensity', 'Light Intensity'
    RAIN_SENSOR = 'rain_sensor', 'Rain Sensor'


class SensorStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    MAINTENANCE = 'maintenance', 'Maintenance'
    ERROR = 'error', 'Error'


class Sensor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    sensor_type = models.CharField(max_length=20, choices=SensorType.choices)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=SensorStatus.choices, default=SensorStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sensors'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_sensor_type_display()})"


class SensorReading(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    value = models.FloatField()
    unit = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=timezone.now)
    is_anomaly = models.BooleanField(default=False)

    class Meta:
        db_table = 'sensor_readings'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sensor', '-timestamp']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.sensor.name}: {self.value} {self.unit} at {self.timestamp}"


class WeatherData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    temperature = models.FloatField()  # Celsius
    humidity = models.FloatField()  # Percentage
    pressure = models.FloatField()  # hPa
    wind_speed = models.FloatField()  # km/h
    wind_direction = models.CharField(max_length=10)
    rainfall = models.FloatField(default=0.0)  # mm
    solar_radiation = models.FloatField(default=0.0)  # W/m²
    uv_index = models.FloatField(default=0.0)
    visibility = models.FloatField(default=10.0)  # km
    cloud_cover = models.IntegerField(default=0)  # percentage
    weather_condition = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'weather_data'
        ordering = ['-timestamp']

    def __str__(self):
        return f"Weather at {self.timestamp}: {self.temperature}°C, {self.humidity}%"


class WeatherForecast(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    forecast_date = models.DateField()
    min_temperature = models.FloatField()
    max_temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall_probability = models.IntegerField()  # percentage
    rainfall_amount = models.FloatField(default=0.0)  # mm
    wind_speed = models.FloatField()
    weather_condition = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'weather_forecast'
        ordering = ['forecast_date']
        unique_together = ['forecast_date']

    def __str__(self):
        return f"Forecast for {self.forecast_date}: {self.min_temperature}-{self.max_temperature}°C"
