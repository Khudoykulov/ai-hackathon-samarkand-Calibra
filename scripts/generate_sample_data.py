#!/usr/bin/env python
"""
Script to generate sample sensor data for testing
Run with: python manage.py shell < scripts/generate_sample_data.py
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.utils import timezone
from sensor.models import Sensor, SensorReading, WeatherData

def generate_sensor_readings():
    """Generate random sensor readings for the last 7 days"""
    sensors = Sensor.objects.filter(is_active=True)
    end_time = timezone.now()
    
    for sensor in sensors:
        print(f"Generating data for {sensor.name}...")
        
        # Generate readings for last 7 days, every 30 minutes
        for i in range(7 * 24 * 2):  # 7 days * 24 hours * 2 (every 30 min)
            timestamp = end_time - timedelta(minutes=i * 30)
            
            # Generate realistic values based on sensor type
            if 'namlik' in sensor.sensor_type.name.lower():
                # Soil moisture: simulate daily cycle with some randomness
                base_value = 45 + 20 * abs(random.gauss(0, 0.3))
                daily_variation = 10 * random.sin(i * 3.14159 / 48)  # 24-hour cycle
                value = max(15, min(85, base_value + daily_variation))
            
            elif 'harorat' in sensor.sensor_type.name.lower():
                # Temperature: simulate daily and seasonal cycles
                if 'tuproq' in sensor.sensor_type.name.lower():
                    base_temp = 20
                    daily_variation = 5 * random.sin(i * 3.14159 / 48)
                else:
                    base_temp = 24
                    daily_variation = 8 * random.sin(i * 3.14159 / 48)
                
                value = base_temp + daily_variation + random.gauss(0, 2)
            
            elif 'ph' in sensor.sensor_type.name.lower():
                # pH: relatively stable with small variations
                value = 6.8 + random.gauss(0, 0.2)
                value = max(6.0, min(8.0, value))
            
            elif 'o\'tkazuvchanlik' in sensor.sensor_type.name.lower():
                # Conductivity: stable with small variations
                value = 1.2 + random.gauss(0, 0.1)
                value = max(0.5, min(2.5, value))
            
            elif 'yorug\'lik' in sensor.sensor_type.name.lower():
                # Solar radiation: day/night cycle
                hour_of_day = (timestamp.hour + timestamp.minute / 60) % 24
                if 6 <= hour_of_day <= 18:  # Daytime
                    max_radiation = 1000
                    sun_angle = abs(12 - hour_of_day) / 6  # 0 at noon, 1 at 6am/6pm
                    value = max_radiation * (1 - sun_angle) * random.uniform(0.7, 1.0)
                else:  # Nighttime
                    value = random.uniform(0, 50)
            
            elif 'yomg\'ir' in sensor.sensor_type.name.lower():
                # Rainfall: mostly 0, occasional rain
                if random.random() > 0.95:  # 5% chance of rain
                    value = random.uniform(0.1, 15)
                else:
                    value = 0
            
            else:
                # Default random value
                value = random.uniform(0, 100)
            
            # Create the reading
            SensorReading.objects.create(
                sensor=sensor,
                value=round(value, 2),
                timestamp=timestamp
            )
    
    print(f"Generated sensor readings for {sensors.count()} sensors")

def generate_weather_data():
    """Generate weather data for the last 7 days"""
    end_time = timezone.now()
    
    print("Generating weather data...")
    
    # Generate weather data every hour for last 7 days
    for i in range(7 * 24):  # 7 days * 24 hours
        timestamp = end_time - timedelta(hours=i)
        
        # Generate realistic weather data
        base_temp = 24 + 5 * random.sin(i * 3.14159 / 12)  # Daily cycle
        temperature = base_temp + random.gauss(0, 3)
        
        humidity = max(30, min(90, 60 + random.gauss(0, 15)))
        pressure = 1013 + random.gauss(0, 10)
        wind_speed = max(0, random.gauss(12, 5))
        
        # Rainfall: occasional
        if random.random() > 0.9:  # 10% chance
            rainfall = random.uniform(0.1, 10)
        else:
            rainfall = 0
        
        solar_radiation = max(0, 800 + random.gauss(0, 200))
        
        wind_directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        wind_direction = random.choice(wind_directions)
        
        WeatherData.objects.create(
            temperature=round(temperature, 1),
            humidity=round(humidity, 1),
            pressure=round(pressure, 1),
            wind_speed=round(wind_speed, 1),
            wind_direction=wind_direction,
            rainfall=round(rainfall, 2),
            solar_radiation=round(solar_radiation, 1),
            timestamp=timestamp
        )
    
    print("Generated weather data for 7 days")

def main():
    """Generate all sample data"""
    print("Generating sample data...")
    
    # Clear existing data
    print("Clearing existing readings...")
    SensorReading.objects.all().delete()
    WeatherData.objects.all().delete()
    
    generate_sensor_readings()
    generate_weather_data()
    
    print("Sample data generation completed!")

if __name__ == '__main__':
    main()
