import google.generativeai as genai
from django.conf import settings
import json
import random
from datetime import datetime


class GeminiAIPredictor:
    def __init__(self):
        if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY != 'your-gemini-api-key':
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            self.api_available = True
        else:
            self.api_available = False

    def analyze_irrigation_needs(self, sensor_data, weather_data):
        """Analyze sensor and weather data to determine irrigation needs"""

        if self.api_available:
            return self._analyze_with_gemini(sensor_data, weather_data)
        else:
            return self._analyze_with_mock_ai(sensor_data, weather_data)

    def _analyze_with_gemini(self, sensor_data, weather_data):
        """Use Gemini AI for analysis"""
        try:
            prompt = self._create_analysis_prompt(sensor_data, weather_data)
            response = self.model.generate_content(prompt)

            # Parse the AI response
            return self._parse_ai_response(response.text, sensor_data, weather_data)

        except Exception as e:
            print(f"Gemini AI error: {e}")
            return self._analyze_with_mock_ai(sensor_data, weather_data)

    def _analyze_with_mock_ai(self, sensor_data, weather_data):
        """Mock AI analysis for testing when API is not available"""
        soil_moisture = sensor_data.get('soil_moisture', 50)
        air_temp = sensor_data.get('air_temperature', 25)
        air_humidity = sensor_data.get('air_humidity', 60)
        rainfall = weather_data.get('rainfall', 0)

        # Simple rule-based decision making
        if soil_moisture < 25:
            decision = 'urgent_irrigation'
            confidence = 94
            reasoning = f"Tuproq namligi kritik darajada ({soil_moisture}%). Darhol sug'orish zarur."
            recommendations = [
                "Darhol 18-20 daqiqa sug'orish",
                "Keyingi 6 soat davomida namligi kuzatish",
                "Mulch (qoplama) qo'llash"
            ]
        elif soil_moisture < 40:
            decision = 'irrigation_needed'
            confidence = 87
            reasoning = f"Tuproq namligi past ({soil_moisture}%). Sug'orish tavsiya etiladi."
            recommendations = [
                "12-15 daqiqa sug'orish",
                "Ertalab yoki kechqurun sug'orish",
                "Havo namligini kuzatish"
            ]
        elif rainfall > 5:
            decision = 'no_action'
            confidence = 91
            reasoning = f"Yaqinda yomg'ir yog'gan ({rainfall}mm). Sug'orish kerak emas."
            recommendations = [
                "24 soat kutish",
                "Tuproq namligini kuzatish",
                "Drenaj tizimini tekshirish"
            ]
        else:
            decision = 'no_action'
            confidence = 78
            reasoning = "Barcha ko'rsatkichlar normal oraliqda. Hozircha harakat kerak emas."
            recommendations = [
                "Muntazam kuzatishni davom ettirish",
                "Ob-havo prognozini tekshirish"
            ]

        return {
            'decision': decision,
            'confidence_percentage': confidence,
            'confidence_level': self._get_confidence_level(confidence),
            'reasoning': reasoning,
            'recommendations': recommendations,
            'analysis_details': {
                'soil_moisture_status': 'critical' if soil_moisture < 25 else 'warning' if soil_moisture < 40 else 'normal',
                'temperature_status': 'high' if air_temp > 30 else 'normal',
                'humidity_status': 'low' if air_humidity < 50 else 'normal',
                'weather_impact': 'positive' if rainfall > 0 else 'neutral'
            }
        }

    def _create_analysis_prompt(self, sensor_data, weather_data):
        """Create prompt for Gemini AI"""
        return f"""
        Siz professional qishloq xo'jaligi va sug'orish tizimi mutaxassisisiz. 
        Quyidagi ma'lumotlarni tahlil qilib, sug'orish bo'yicha qaror qabul qiling:

        DATCHILAR MA'LUMOTLARI:
        - Tuproq namligi: {sensor_data.get('soil_moisture', 0)}%
        - Havo harorati: {sensor_data.get('air_temperature', 0)}°C
        - Havo namligi: {sensor_data.get('air_humidity', 0)}%
        - pH darajasi: {sensor_data.get('ph_level', 7.0)}

        OB-HAVO MA'LUMOTLARI:
        - Yomg'ir: {weather_data.get('rainfall', 0)}mm
        - Shamol tezligi: {weather_data.get('wind_speed', 0)} km/h
        - Quyosh radiatsiyasi: {weather_data.get('solar_radiation', 0)} W/m²

        OPTIMAL QIYMATLAR:
        - Tuproq namligi: 60-70%
        - pH: 6.5-7.2
        - Havo harorati: 18-28°C

        Javobingizni quyidagi JSON formatida bering:
        {{
            "decision": "no_action/irrigation_needed/urgent_irrigation/stop_irrigation",
            "confidence_percentage": 85,
            "reasoning": "Batafsil tahlil va sabab",
            "recommendations": ["Tavsiya 1", "Tavsiya 2", "Tavsiya 3"],
            "estimated_duration": 15,
            "optimal_time": "ertalab/kechqurun/hozir"
        }}
        """

    def _parse_ai_response(self, response_text, sensor_data, weather_data):
        """Parse Gemini AI response"""
        try:
            # Try to extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                ai_response = json.loads(json_str)

                return {
                    'decision': ai_response.get('decision', 'no_action'),
                    'confidence_percentage': ai_response.get('confidence_percentage', 75),
                    'confidence_level': self._get_confidence_level(ai_response.get('confidence_percentage', 75)),
                    'reasoning': ai_response.get('reasoning', 'AI tahlil yakunlandi'),
                    'recommendations': ai_response.get('recommendations', []),
                    'estimated_duration': ai_response.get('estimated_duration', 15),
                    'optimal_time': ai_response.get('optimal_time', 'hozir')
                }
            else:
                raise ValueError("JSON not found in response")

        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return self._analyze_with_mock_ai(sensor_data, weather_data)

    def _get_confidence_level(self, percentage):
        """Convert confidence percentage to level"""
        if percentage >= 95:
            return 'very_high'
        elif percentage >= 85:
            return 'high'
        elif percentage >= 70:
            return 'medium'
        else:
            return 'low'


class IrrigationOptimizer:
    """Optimize irrigation schedules based on historical data"""

    def __init__(self):
        self.predictor = GeminiAIPredictor()

    def optimize_schedule(self, plant_profile, historical_data):
        """Optimize irrigation schedule for a plant profile"""
        # Analyze historical patterns
        patterns = self._analyze_patterns(historical_data)

        # Generate optimized schedule
        schedule = {
            'morning_time': '06:30',
            'evening_time': '18:30',
            'frequency_hours': 24,
            'duration_minutes': 15,
            'adjustments': patterns.get('adjustments', [])
        }

        return schedule

    def _analyze_patterns(self, historical_data):
        """Analyze historical irrigation patterns"""
        # Mock pattern analysis
        return {
            'best_times': ['06:00-08:00', '18:00-20:00'],
            'optimal_duration': 15,
            'water_efficiency': 0.85,
            'adjustments': [
                'Yozda ertalab sug\'orish samaraliroq',
                'Shamolda sug\'orish vaqtini uzaytirish',
                'Yomg\'irdan keyin 24 soat kutish'
            ]
        }
