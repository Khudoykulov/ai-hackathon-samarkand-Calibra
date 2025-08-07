import random
import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Sensor, SensorReading, WeatherData, SensorType
from .serializers import SensorSerializer, SensorReadingSerializer, WeatherDataSerializer

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    @action(detail=False, methods=['get'])
    def generate_random_data(self, request):
        """Generate random sensor data for testing"""
        sensors = Sensor.objects.filter(is_active=True)

        for sensor in sensors:
            # Generate random values based on sensor type
            if 'namlik' in sensor.sensor_type.name.lower() or 'moisture' in sensor.sensor_type.name.lower():
                value = random.uniform(20, 80)  # Soil moisture 20-80%
            elif 'harorat' in sensor.sensor_type.name.lower() or 'temperature' in sensor.sensor_type.name.lower():
                value = random.uniform(15, 35)  # Temperature 15-35°C
            elif 'ph' in sensor.sensor_type.name.lower():
                value = random.uniform(6.0, 8.0)  # pH 6.0-8.0
            elif 'conductivity' in sensor.sensor_type.name.lower():
                value = random.uniform(0.5, 2.0)  # Conductivity 0.5-2.0 mS/cm
            else:
                value = random.uniform(0, 100)

            SensorReading.objects.create(
                sensor=sensor,
                value=round(value, 2)
            )

        return Response({'message': 'Random sensor data generated successfully'})

    @action(detail=False, methods=['get'])
    def current_status(self, request):
        """Get current status of all sensors"""
        sensors = Sensor.objects.filter(is_active=True)
        data = []

        for sensor in sensors:
            latest_reading = sensor.readings.first()
            if latest_reading:
                # Determine status based on sensor type and value
                status_info = self._get_sensor_status(sensor, latest_reading.value)

                data.append({
                    'id': sensor.id,
                    'name': sensor.name,
                    'type': sensor.sensor_type.name,
                    'location': sensor.location,
                    'current_value': latest_reading.value,
                    'unit': sensor.sensor_type.unit,
                    'status': status_info['status'],
                    'status_color': status_info['color'],
                    'last_updated': latest_reading.timestamp,
                })

        return Response(data)

    def _get_sensor_status(self, sensor, value):
        """Determine sensor status based on value and type"""
        sensor_name = sensor.sensor_type.name.lower()

        if 'namlik' in sensor_name or 'moisture' in sensor_name:
            if value < settings.IRRIGATION_SETTINGS['CRITICAL_SOIL_MOISTURE']:
                return {'status': 'Kritik', 'color': 'critical'}
            elif value < settings.IRRIGATION_SETTINGS['WARNING_SOIL_MOISTURE']:
                return {'status': 'Ogohlantirish', 'color': 'warning'}
            else:
                return {'status': 'Normal', 'color': 'normal'}
        elif 'harorat' in sensor_name or 'temperature' in sensor_name:
            if value > settings.IRRIGATION_SETTINGS['CRITICAL_TEMP_MAX']:
                return {'status': 'Yuqori', 'color': 'warning'}
            elif value < 10:
                return {'status': 'Past', 'color': 'warning'}
            else:
                return {'status': 'Normal', 'color': 'normal'}
        elif 'ph' in sensor_name:
            if (settings.IRRIGATION_SETTINGS['OPTIMAL_PH_MIN'] <= value <=
                settings.IRRIGATION_SETTINGS['OPTIMAL_PH_MAX']):
                return {'status': 'Optimal', 'color': 'normal'}
            else:
                return {'status': 'Moslash kerak', 'color': 'warning'}
        else:
            return {'status': 'Normal', 'color': 'normal'}

class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get sensor statistics for the last 24 hours"""
        end_time = timezone.now()
        start_time = end_time - timedelta(hours=24)

        sensors = Sensor.objects.filter(is_active=True)
        stats = []

        for sensor in sensors:
            readings = SensorReading.objects.filter(
                sensor=sensor,
                timestamp__gte=start_time,
                timestamp__lte=end_time
            )

            if readings.exists():
                values = [r.value for r in readings]
                current_reading = sensor.readings.first()

                stats.append({
                    'sensor_name': sensor.name,
                    'sensor_type': sensor.sensor_type.name,
                    'current_value': current_reading.value if current_reading else 0,
                    'min_value': min(values),
                    'max_value': max(values),
                    'avg_value': round(sum(values) / len(values), 2),
                    'unit': sensor.sensor_type.unit,
                    'readings_count': len(values)
                })

        return Response(stats)

class WeatherViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current weather data"""
        # Try to get from API first, then fallback to latest DB record
        weather_data = self._fetch_weather_from_api()

        if not weather_data:
            # Fallback to latest DB record or generate random data
            latest = WeatherData.objects.first()
            if latest:
                weather_data = WeatherDataSerializer(latest).data
            else:
                weather_data = self._generate_random_weather()

        return Response(weather_data)

    @action(detail=False, methods=['get'])
    def forecast(self, request):
        """Get 7-day weather forecast"""
        forecast_data = []

        # Generate mock 7-day forecast
        for i in range(7):
            date = timezone.now().date() + timedelta(days=i)
            forecast_data.append({
                'date': date,
                'day_name': date.strftime('%A'),
                'temperature': random.randint(18, 30),
                'humidity': random.randint(40, 80),
                'rainfall': random.uniform(0, 10) if random.random() > 0.7 else 0,
                'condition': random.choice(['sunny', 'cloudy', 'rainy', 'partly_cloudy'])
            })

        return Response(forecast_data)

    def _fetch_weather_from_api(self):
        """Fetch weather data from OpenWeatherMap API"""
        try:
            api_key = settings.WEATHER_API_KEY
            if not api_key or api_key == 'your-openweathermap-api-key':
                return None

            # Tashkent coordinates
            lat, lon = 41.2995, 69.2401
            url = f"{settings.WEATHER_API_URL}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': api_key,
                'units': 'metric'
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()

                weather_data = {
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': data['wind']['speed'] * 3.6,  # Convert m/s to km/h
                    'wind_direction': self._get_wind_direction(data['wind']['deg']),
                    'rainfall': data.get('rain', {}).get('1h', 0),
                    'solar_radiation': random.uniform(200, 1000),  # Mock solar radiation
                    'timestamp': timezone.now()
                }

                # Save to database
                WeatherData.objects.create(**weather_data)

                return weather_data
        except Exception as e:
            print(f"Weather API error: {e}")
            return None

    def _generate_random_weather(self):
        """Generate random weather data for testing"""
        return {
            'temperature': random.uniform(18, 32),
            'humidity': random.uniform(30, 80),
            'pressure': random.uniform(1000, 1020),
            'wind_speed': random.uniform(5, 25),
            'wind_direction': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
            'rainfall': random.uniform(0, 5) if random.random() > 0.8 else 0,
            'solar_radiation': random.uniform(200, 1000),
            'timestamp': timezone.now()
        }

    def _get_wind_direction(self, degrees):
        """Convert wind degrees to direction"""
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        index = round(degrees / 45) % 8
        return directions[index]
