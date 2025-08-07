from django.db import models

class PlantType(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    
    # Optimal growing conditions
    optimal_soil_moisture_min = models.FloatField(default=60)
    optimal_soil_moisture_max = models.FloatField(default=70)
    optimal_temperature_min = models.FloatField(default=18)
    optimal_temperature_max = models.FloatField(default=28)
    optimal_ph_min = models.FloatField(default=6.5)
    optimal_ph_max = models.FloatField(default=7.2)
    
    # Irrigation settings
    irrigation_frequency_hours = models.IntegerField(default=24)
    irrigation_duration_minutes = models.IntegerField(default=15)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class PlantProfile(models.Model):
    plant_type = models.ForeignKey(PlantType, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    planted_date = models.DateField()
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.plant_type.name} - {self.location}"
