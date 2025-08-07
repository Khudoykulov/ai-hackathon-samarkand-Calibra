from django.db import models
from django.utils import timezone


class AIAnalysis(models.Model):
    DECISION_CHOICES = [
        ('no_action', 'No Action Required'),
        ('irrigation_needed', 'Irrigation Needed'),
        ('urgent_irrigation', 'Urgent Irrigation Required'),
        ('stop_irrigation', 'Stop Irrigation'),
        ('adjust_schedule', 'Adjust Schedule'),
        ('maintenance_required', 'Maintenance Required'),
    ]

    CONFIDENCE_CHOICES = [
        ('low', 'Low (< 70%)'),
        ('medium', 'Medium (70-85%)'),
        ('high', 'High (85-95%)'),
        ('very_high', 'Very High (> 95%)'),
    ]

    decision = models.CharField(max_length=50, choices=DECISION_CHOICES)
    confidence_level = models.CharField(max_length=20, choices=CONFIDENCE_CHOICES)
    confidence_percentage = models.FloatField()

    reasoning = models.TextField()
    recommendations = models.JSONField(default=list)

    # Input data used for analysis
    soil_moisture = models.FloatField()
    air_temperature = models.FloatField()
    air_humidity = models.FloatField()
    weather_forecast = models.JSONField(default=dict)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"AI Analysis {self.id} - {self.decision}"


class AIModel(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    description = models.TextField()

    accuracy_percentage = models.FloatField(default=0)
    training_data_count = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_trained = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} v{self.version}"


class AILearningData(models.Model):
    # Environmental data
    soil_moisture = models.FloatField()
    air_temperature = models.FloatField()
    air_humidity = models.FloatField()
    ph_level = models.FloatField()

    # Weather data
    rainfall = models.FloatField()
    solar_radiation = models.FloatField()
    wind_speed = models.FloatField()

    # Action taken
    irrigation_applied = models.BooleanField()
    irrigation_duration = models.IntegerField(default=0)

    # Outcome
    plant_health_score = models.FloatField(null=True, blank=True)
    water_efficiency = models.FloatField(null=True, blank=True)

    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Learning Data {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
