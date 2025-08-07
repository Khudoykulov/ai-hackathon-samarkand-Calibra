from django.db import models
from django.utils import timezone

class IrrigationSystem(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_automatic = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.location}"

class IrrigationEvent(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    TRIGGER_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('ai_decision', 'AI Decision'),
        ('scheduled', 'Scheduled'),
    ]
    
    system = models.ForeignKey(IrrigationSystem, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    trigger_type = models.CharField(max_length=20, choices=TRIGGER_CHOICES, default='automatic')
    
    scheduled_start = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField()
    
    water_amount_liters = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Irrigation {self.id} - {self.status}"

class SystemControl(models.Model):
    COMMAND_CHOICES = [
        ('start_irrigation', 'Start Irrigation'),
        ('stop_irrigation', 'Stop Irrigation'),
        ('emergency_stop', 'Emergency Stop'),
        ('system_restart', 'System Restart'),
        ('calibrate_sensors', 'Calibrate Sensors'),
        ('test_mode', 'Test Mode'),
    ]
    
    command = models.CharField(max_length=50, choices=COMMAND_CHOICES)
    parameters = models.JSONField(default=dict, blank=True)
    executed_at = models.DateTimeField(default=timezone.now)
    success = models.BooleanField(default=False)
    response = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.command} - {self.executed_at}"
