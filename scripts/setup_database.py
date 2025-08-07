#!/usr/bin/env python
"""
Database setup script for AI Irrigation System
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.management import execute_from_command_line
from sensor.models import Sensor, SensorReading, WeatherData
from plant.models import PlantType, Plant
from controller.models import IrrigationZone, IrrigationController
from ai_engine.models import AIModel
import random
from datetime import datetime, timedelta
from django.utils import timezone


def create_initial_data():
    """Create initial data for the system"""

    print("Creating initial sensors...")

    # Create sensors
    sensors_data = [
        {'name': 'Tuproq Namligi #1', 'type': 'soil_moisture', 'location': 'A sektori, 2-qator'},
        {'name': 'Tuproq Namligi #2', 'type': 'soil_moisture', 'location': 'B sektori, 1-qator'},
        {'name': 'Tuproq Harorati #1', 'type': 'soil_temperature', 'location': 'A sektori, chuqurlik 15cm'},
        {'name': 'Havo Namligi Datchigi', 'type': 'air_humidity', 'location': 'Markaziy meteo stantsiya'},
        {'name': 'Havo Harorati', 'type': 'air_temperature', 'location': 'Markaziy meteo stantsiya'},
        {'name': 'pH Datchigi', 'type': 'ph_level', 'location': 'A sektori, chuqurlik 20cm'},
        {'name': "O'tkazuvchanlik", 'type': 'conductivity', 'location': 'A sektori, chuqurlik 20cm'},
        {'name': "Yorug'lik Datchigi", 'type': 'light_intensity', 'location': 'Markaziy meteo stantsiya'},
    ]

    for sensor_data in sensors_data:
        sensor, created = Sensor.objects.get_or_create(
            name=sensor_data['name'],
            defaults={
                'sensor_type': sensor_data['type'],
                'location': sensor_data['location'],
                'status': 'active'
            }
        )
        if created:
            print(f"Created sensor: {sensor.name}")

    print("Creating plant types...")

    # Create plant types
    plant_types_data = [
        {
            'name': 'Pomidor',
            'scientific_name': 'Solanum lycopersicum',
            'optimal_soil_moisture_min': 60.0,
            'optimal_soil_moisture_max': 70.0,
            'water_requirement_medium': 35.0
        },
        {
            'name': 'Bodring',
            'scientific_name': 'Cucumis sativus',
            'optimal_soil_moisture_min': 65.0,
            'optimal_soil_moisture_max': 75.0,
            'water_requirement_medium': 40.0
        }
    ]

    for plant_type_data in plant_types_data:
        plant_type, created = PlantType.objects.get_or_create(
            name=plant_type_data['name'],
            defaults=plant_type_data
        )
        if created:
            print(f"Created plant type: {plant_type.name}")

    print("Creating irrigation zones...")

    # Create irrigation zones
    zones_data = [
        {
            'name': 'A Sektori',
            'location': 'Shimoliy maydon',
            'area_square_meters': 100.0,
            'flow_rate_liters_per_minute': 15.0
        },
        {
            'name': 'B Sektori',
            'location': 'Janubiy maydon',
            'area_square_meters': 80.0,
            'flow_rate_liters_per_minute': 12.0
        }
    ]

    for zone_data in zones_data:
        zone, created = IrrigationZone.objects.get_or_create(
            name=zone_data['name'],
            defaults=zone_data
        )
        if created:
            print(f"Created irrigation zone: {zone.name}")

    print("Creating controllers...")

    # Create controllers
    controller, created = IrrigationController.objects.get_or_create(
        name='ESP32 Asosiy Kontroller',
        defaults={
            'controller_type': 'esp32',
            'ip_address': '192.168.1.100',
            'is_online': True,
            'last_heartbeat': timezone.now()
        }
    )
    if created:
        print(f"Created controller: {controller.name}")
        # Assign zones to controller
        controller.zones.set(IrrigationZone.objects.all())

    print("Creating AI models...")

    # Create AI models
    ai_models_data = [
        {
            'name': 'Irrigation Predictor',
            'model_type': 'irrigation_predictor',
            'accuracy': 94.0,
            'precision': 92.0,
            'recall': 96.0,
            'f1_score': 94.0
        },
        {
            'name': 'Weather Analyzer',
            'model_type': 'weather_analyzer',
            'accuracy': 88.0,
            'precision': 85.0,
            'recall': 90.0,
            'f1_score': 87.5
        }
    ]

    for model_data in ai_models_data:
        model, created = AIModel.objects.get_or_create(
            name=model_data['name'],
            model_type=model_data['model_type'],
            defaults=model_data
        )
        if created:
            print(f"Created AI model: {model.name}")

    print("Creating sample plants...")

    # Create sample plants
    tomato_type = PlantType.objects.get(name='Pomidor')
    plant, created = Plant.objects.get_or_create(
        name='Pomidor A1',
        defaults={
            'plant_type': tomato_type,
            'location': 'A sektori, 1-qator',
            'planted_date': timezone.now().date() - timedelta(days=30),
            'growth_stage': 'vegetative'
        }
    )
    if created:
        print(f"Created plant: {plant.name}")

    print("Initial data creation completed!")


def generate_sample_data():
    """Generate sample sensor readings and weather data"""

    print("Generating sample sensor readings...")

    sensors = Sensor.objects.all()

    # Generate readings for the last 24 hours
    for i in range(24):
        timestamp = timezone.now() - timedelta(hours=i)

        for sensor in sensors:
            if sensor.sensor_type == 'soil_moisture':
                value = random.uniform(20, 60)
                unit = '%'
            elif sensor.sensor_type == 'soil_temperature':
                value = random.uniform(15, 25)
                unit = '°C'
            elif sensor.sensor_type == 'air_temperature':
                value = random.uniform(18, 32)
                unit = '°C'
            elif sensor.sensor_type == 'air_humidity':
                value = random.uniform(40, 70)
                unit = '%'
            elif sensor.sensor_type == 'ph_level':
                value = random.uniform(6.0, 7.5)
                unit = 'pH'
            elif sensor.sensor_type == 'conductivity':
                value = random.uniform(0.8, 1.8)
                unit = 'mS/cm'
            elif sensor.sensor_type == 'light_intensity':
                value = random.uniform(200, 1000)
                unit = 'W/m²'
            else:
                value = random.uniform(0, 100)
                unit = ''

            SensorReading.objects.create(
                sensor=sensor,
                value=round(value, 2),
                unit=unit,
                timestamp=timestamp,
                is_anomaly=value < 25 if sensor.sensor_type == 'soil_moisture' else False
            )

    print("Generating sample weather data...")

    # Generate weather data for the last 7 days
    for i in range(7):
        timestamp = timezone.now() - timedelta(days=i)

        WeatherData.objects.create(
            temperature=round(random.uniform(18, 32), 1),
            humidity=round(random.uniform(40, 70), 1),
            pressure=round(random.uniform(1010, 1020), 1),
            wind_speed=round(random.uniform(5, 20), 1),
            wind_direction=random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
            rainfall=round(random.uniform(0, 5), 1),
            solar_radiation=round(random.uniform(200, 1000), 1),
            uv_index=round(random.uniform(1, 10), 1),
            visibility=round(random.uniform(5, 15), 1),
            cloud_cover=random.randint(0, 100),
            weather_condition=random.choice(['clear sky', 'few clouds', 'scattered clouds', 'overcast']),
            timestamp=timestamp
        )

    print("Sample data generation completed!")


if __name__ == '__main__':
    print("Setting up AI Irrigation System database...")

    # Run migrations
    print("Running database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])

    # Create initial data
    create_initial_data()

    # Generate sample data
    generate_sample_data()

    print("Database setup completed successfully!")
    print("\nYou can now start the development server with:")
    print("python manage.py runserver")
