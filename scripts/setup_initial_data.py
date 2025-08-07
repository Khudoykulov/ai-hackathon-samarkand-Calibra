#!/usr/bin/env python
"""
Script to set up initial data for the AI irrigation system
Run this after migrations: python manage.py shell < scripts/setup_initial_data.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from sensor.models import SensorType, Sensor
from plant.models import PlantType, PlantProfile
from controller.models import IrrigationSystem
from ai_engine.models import AIModel
from datetime import date

def create_sensor_types():
    """Create sensor types"""
    sensor_types = [
        {'name': 'Tuproq Namligi', 'unit': '%', 'description': 'Tuproq namligini o\'lchash'},
        {'name': 'Tuproq Harorati', 'unit': '°C', 'description': 'Tuproq haroratini o\'lchash'},
        {'name': 'Havo Namligi', 'unit': '%', 'description': 'Havo namligini o\'lchash'},
        {'name': 'Havo Harorati', 'unit': '°C', 'description': 'Havo haroratini o\'lchash'},
        {'name': 'pH Darajasi', 'unit': 'pH', 'description': 'Tuproq pH darajasini o\'lchash'},
        {'name': 'Elektr O\'tkazuvchanlik', 'unit': 'mS/cm', 'description': 'Tuproq o\'tkazuvchanligini o\'lchash'},
        {'name': 'Yorug\'lik Intensivligi', 'unit': 'W/m²', 'description': 'Quyosh radiatsiyasini o\'lchash'},
        {'name': 'Yomg\'ir', 'unit': 'mm', 'description': 'Yomg\'ir miqdorini o\'lchash'},
    ]
    
    for sensor_type_data in sensor_types:
        sensor_type, created = SensorType.objects.get_or_create(
            name=sensor_type_data['name'],
            defaults=sensor_type_data
        )
        if created:
            print(f"Created sensor type: {sensor_type.name}")

def create_sensors():
    """Create sensors"""
    sensors_data = [
        {'name': 'Tuproq Namligi Datchigi #1', 'type': 'Tuproq Namligi', 'location': 'A sektori, 2-qator'},
        {'name': 'Tuproq Namligi Datchigi #2', 'type': 'Tuproq Namligi', 'location': 'B sektori, 1-qator'},
        {'name': 'Tuproq Harorati #1', 'type': 'Tuproq Harorati', 'location': 'A sektori, chuqurlik 15cm'},
        {'name': 'Havo Namligi Datchigi', 'type': 'Havo Namligi', 'location': 'Markaziy meteo stantsiya'},
        {'name': 'Havo Harorati', 'type': 'Havo Harorati', 'location': 'Markaziy meteo stantsiya'},
        {'name': 'pH Datchigi', 'type': 'pH Darajasi', 'location': 'A sektori, chuqurlik 20cm'},
        {'name': 'O\'tkazuvchanlik', 'type': 'Elektr O\'tkazuvchanlik', 'location': 'A sektori, chuqurlik 20cm'},
        {'name': 'Yorug\'lik Datchigi', 'type': 'Yorug\'lik Intensivligi', 'location': 'Markaziy meteo stantsiya'},
        {'name': 'Yomg\'ir Datchigi', 'type': 'Yomg\'ir', 'location': 'Markaziy meteo stantsiya'},
    ]
    
    for sensor_data in sensors_data:
        sensor_type = SensorType.objects.get(name=sensor_data['type'])
        sensor, created = Sensor.objects.get_or_create(
            name=sensor_data['name'],
            defaults={
                'sensor_type': sensor_type,
                'location': sensor_data['location'],
                'is_active': True
            }
        )
        if created:
            print(f"Created sensor: {sensor.name}")

def create_plant_types():
    """Create plant types"""
    plant_types = [
        {
            'name': 'Pomidor',
            'scientific_name': 'Solanum lycopersicum',
            'description': 'Pomidor o\'simligi',
            'optimal_soil_moisture_min': 65,
            'optimal_soil_moisture_max': 75,
            'optimal_temperature_min': 20,
            'optimal_temperature_max': 30,
            'irrigation_frequency_hours': 12,
            'irrigation_duration_minutes': 20
        },
        {
            'name': 'Bodring',
            'scientific_name': 'Cucumis sativus',
            'description': 'Bodring o\'simligi',
            'optimal_soil_moisture_min': 70,
            'optimal_soil_moisture_max': 80,
            'optimal_temperature_min': 18,
            'optimal_temperature_max': 28,
            'irrigation_frequency_hours': 8,
            'irrigation_duration_minutes': 15
        }
    ]
    
    for plant_data in plant_types:
        plant_type, created = PlantType.objects.get_or_create(
            name=plant_data['name'],
            defaults=plant_data
        )
        if created:
            print(f"Created plant type: {plant_type.name}")

def create_irrigation_system():
    """Create irrigation system"""
    system, created = IrrigationSystem.objects.get_or_create(
        name='Asosiy Sug\'orish Tizimi',
        defaults={
            'location': 'Markaziy boshqaruv',
            'is_active': True,
            'is_automatic': True
        }
    )
    if created:
        print(f"Created irrigation system: {system.name}")

def create_ai_model():
    """Create AI model"""
    model, created = AIModel.objects.get_or_create(
        name='Gemini AI Irrigation Model',
        defaults={
            'version': '1.0',
            'description': 'AI model for irrigation decision making using Gemini API',
            'accuracy_percentage': 87,
            'training_data_count': 15847,
            'is_active': True
        }
    )
    if created:
        print(f"Created AI model: {model.name}")

def main():
    """Run all setup functions"""
    print("Setting up initial data for AI Irrigation System...")
    
    create_sensor_types()
    create_sensors()
    create_plant_types()
    create_irrigation_system()
    create_ai_model()
    
    print("Initial data setup completed!")

if __name__ == '__main__':
    main()
