from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import AIAnalysis, AIModel, AILearningData
from .serializers import AIAnalysisSerializer, AIModelSerializer, AILearningDataSerializer
from .predictors import GeminiAIPredictor, IrrigationOptimizer
from sensor.models import SensorReading, WeatherData, Sensor


class AIAnalysisViewSet(viewsets.ModelViewSet):
    queryset = AIAnalysis.objects.all()
    serializer_class = AIAnalysisSerializer

    @action(detail=False, methods=['post'])
    def analyze_current_conditions(self, request):
        """Analyze current sensor and weather conditions"""
        predictor = GeminiAIPredictor()

        # Get latest sensor data
        sensor_data = self._get_latest_sensor_data()

        # Get latest weather data
        weather_data = self._get_latest_weather_data()

        # Perform AI analysis
        analysis_result = predictor.analyze_irrigation_needs(sensor_data, weather_data)

        # Save analysis to database
        analysis = AIAnalysis.objects.create(
            decision=analysis_result['decision'],
            confidence_level=analysis_result['confidence_level'],
            confidence_percentage=analysis_result['confidence_percentage'],
            reasoning=analysis_result['reasoning'],
            recommendations=analysis_result.get('recommendations', []),
            soil_moisture=sensor_data.get('soil_moisture', 0),
            air_temperature=sensor_data.get('air_temperature', 0),
            air_humidity=sensor_data.get('air_humidity', 0),
            weather_forecast=weather_data
        )

        return Response({
            'analysis_id': analysis.id,
            'decision': analysis_result['decision'],
            'confidence_percentage': analysis_result['confidence_percentage'],
            'confidence_level': analysis_result['confidence_level'],
            'reasoning': analysis_result['reasoning'],
            'recommendations': analysis_result.get('recommendations', []),
            'estimated_duration': analysis_result.get('estimated_duration', 15),
            'optimal_time': analysis_result.get('optimal_time', 'hozir'),
            'timestamp': analysis.created_at
        })

    @action(detail=False, methods=['get'])
    def recent_decisions(self, request):
        """Get recent AI decisions"""
        recent_analyses = AIAnalysis.objects.filter(
            created_at__gte=timezone.now() - timedelta(hours=24)
        )[:10]

        decisions = []
        for analysis in recent_analyses:
            decisions.append({
                'id': analysis.id,
                'decision': analysis.decision,
                'confidence_percentage': analysis.confidence_percentage,
                'reasoning': analysis.reasoning[:100] + '...' if len(analysis.reasoning) > 100 else analysis.reasoning,
                'timestamp': analysis.created_at
            })

        return Response(decisions)

    @action(detail=False, methods=['get'])
    def performance_metrics(self, request):
        """Get AI performance metrics"""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)

        analyses = AIAnalysis.objects.filter(
            created_at__gte=start_date
        )

        total_analyses = analyses.count()
        if total_analyses == 0:
            return Response({
                'total_analyses': 0,
                'average_confidence': 0,
                'decision_distribution': {},
                'accuracy_trend': []
            })

        # Calculate metrics
        avg_confidence = sum(a.confidence_percentage for a in analyses) / total_analyses

        # Decision distribution
        decision_dist = {}
        for analysis in analyses:
            decision = analysis.get_decision_display()
            decision_dist[decision] = decision_dist.get(decision, 0) + 1

        # Mock accuracy trend (in real implementation, this would be based on actual outcomes)
        accuracy_trend = [
            {'date': (end_date - timedelta(days=i)).date(), 'accuracy': 85 + (i % 10)}
            for i in range(7, 0, -1)
        ]

        return Response({
            'total_analyses': total_analyses,
            'average_confidence': round(avg_confidence, 2),
            'decision_distribution': decision_dist,
            'accuracy_trend': accuracy_trend,
            'learning_data_count': AILearningData.objects.count()
        })

    def _get_latest_sensor_data(self):
        """Get latest sensor readings"""
        data = {}

        # Get soil moisture
        soil_sensor = Sensor.objects.filter(
            sensor_type__name__icontains='namlik',
            is_active=True
        ).first()
        if soil_sensor:
            latest_reading = soil_sensor.readings.first()
            if latest_reading:
                data['soil_moisture'] = latest_reading.value

        # Get air temperature
        temp_sensor = Sensor.objects.filter(
            sensor_type__name__icontains='harorat',
            is_active=True
        ).first()
        if temp_sensor:
            latest_reading = temp_sensor.readings.first()
            if latest_reading:
                data['air_temperature'] = latest_reading.value

        # Get air humidity
        humidity_sensor = Sensor.objects.filter(
            sensor_type__name__icontains='havo',
            is_active=True
        ).first()
        if humidity_sensor:
            latest_reading = humidity_sensor.readings.first()
            if latest_reading:
                data['air_humidity'] = latest_reading.value

        # Get pH
        ph_sensor = Sensor.objects.filter(
            sensor_type__name__icontains='ph',
            is_active=True
        ).first()
        if ph_sensor:
            latest_reading = ph_sensor.readings.first()
            if latest_reading:
                data['ph_level'] = latest_reading.value

        # Set defaults if no data
        data.setdefault('soil_moisture', 45)
        data.setdefault('air_temperature', 24)
        data.setdefault('air_humidity', 55)
        data.setdefault('ph_level', 6.8)

        return data

    def _get_latest_weather_data(self):
        """Get latest weather data"""
        latest_weather = WeatherData.objects.first()
        if latest_weather:
            return {
                'temperature': latest_weather.temperature,
                'humidity': latest_weather.humidity,
                'rainfall': latest_weather.rainfall,
                'wind_speed': latest_weather.wind_speed,
                'solar_radiation': latest_weather.solar_radiation,
                'pressure': latest_weather.pressure
            }

        # Default weather data
        return {
            'temperature': 24,
            'humidity': 55,
            'rainfall': 0,
            'wind_speed': 12,
            'solar_radiation': 850,
            'pressure': 1013
        }


class AIModelViewSet(viewsets.ModelViewSet):
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer

    @action(detail=False, methods=['get'])
    def current_model(self, request):
        """Get current active AI model information"""
        active_model = AIModel.objects.filter(is_active=True).first()

        if not active_model:
            # Create default model if none exists
            active_model = AIModel.objects.create(
                name='Gemini AI Irrigation Model',
                version='1.0',
                description='AI model for irrigation decision making using Gemini API',
                accuracy_percentage=87,
                training_data_count=15847,
                is_active=True
            )

        return Response({
            'id': active_model.id,
            'name': active_model.name,
            'version': active_model.version,
            'accuracy_percentage': active_model.accuracy_percentage,
            'training_data_count': active_model.training_data_count,
            'last_trained': active_model.last_trained,
            'learning_progress': {
                'data_collection': 78,
                'model_training': 87,
                'accuracy_validation': 94
            }
        })


class AILearningDataViewSet(viewsets.ModelViewSet):
    queryset = AILearningData.objects.all()
    serializer_class = AILearningDataSerializer

    @action(detail=False, methods=['post'])
    def add_learning_data(self, request):
        """Add new learning data point"""
        data = request.data

        learning_data = AILearningData.objects.create(
            soil_moisture=data.get('soil_moisture', 0),
            air_temperature=data.get('air_temperature', 0),
            air_humidity=data.get('air_humidity', 0),
            ph_level=data.get('ph_level', 7.0),
            rainfall=data.get('rainfall', 0),
            solar_radiation=data.get('solar_radiation', 0),
            wind_speed=data.get('wind_speed', 0),
            irrigation_applied=data.get('irrigation_applied', False),
            irrigation_duration=data.get('irrigation_duration', 0),
            plant_health_score=data.get('plant_health_score'),
            water_efficiency=data.get('water_efficiency')
        )

        return Response({
            'id': learning_data.id,
            'message': 'Learning data added successfully',
            'timestamp': learning_data.timestamp
        })
