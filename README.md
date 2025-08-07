# AI Sug'orish Tizimi (AI Irrigation System)

Professional AI-powered irrigation system with Django backend and modern frontend.

## Features

- 🤖 **AI Analysis**: Gemini AI integration for intelligent irrigation decisions
- 📊 **Real-time Monitoring**: Live sensor data and weather information
- 🌡️ **Multi-sensor Support**: Soil moisture, temperature, pH, humidity sensors
- 🌤️ **Weather Integration**: OpenWeatherMap API integration
- 💧 **Smart Irrigation**: Automated irrigation based on AI recommendations
- 📱 **Responsive Dashboard**: Modern, mobile-friendly interface
- 📈 **Statistics & Analytics**: Comprehensive system performance metrics

## Project Structure

\`\`\`
project/
├── manage.py
├── project/                 # Django project settings
├── ai_engine/              # AI analysis and decision making
├── controller/             # Irrigation system control
├── dashboard/              # Web dashboard views
├── plant/                  # Plant profiles and settings
├── sensor/                 # Sensor data management
├── scripts/                # Setup and utility scripts
├── static/                 # Static files (CSS, JS)
├── templates/              # HTML templates
└── requirements.txt
\`\`\`

## Quick Setup

1. **Clone and setup**:
\`\`\`bash
git clone <repository-url>
cd ai-irrigation-system
\`\`\`

2. **Install dependencies**:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Configure environment**:
\`\`\`bash
cp .env.example .env
# Edit .env with your API keys
\`\`\`

4. **Run setup script**:
\`\`\`bash
chmod +x scripts/run_setup.sh
./scripts/run_setup.sh
\`\`\`

5. **Start the server**:
\`\`\`bash
python manage.py runserver
\`\`\`

6. **Access the system**:
- Dashboard: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin (admin/admin123)

## API Endpoints

### Sensor Data
- `GET /api/sensor/sensors/` - List all sensors
- `GET /api/sensor/sensors/current_status/` - Current sensor status
- `GET /api/sensor/readings/statistics/` - Sensor statistics
- `GET /api/sensor/weather/current/` - Current weather data

### AI Analysis
- `POST /api/ai/analysis/analyze_current_conditions/` - Get AI analysis
- `GET /api/ai/analysis/recent_decisions/` - Recent AI decisions
- `GET /api/ai/models/current_model/` - Current AI model info

### Irrigation Control
- `GET /api/controller/systems/status/` - System status
- `POST /api/controller/systems/{id}/start_irrigation/` - Start irrigation
- `POST /api/controller/systems/{id}/stop_irrigation/` - Stop irrigation

### Dashboard
- `GET /api/dashboard-data/` - Complete dashboard data
- `GET /api/live-feed/` - Live data feed

## Configuration

### Weather API Setup
1. Get API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Add to `.env`: `WEATHER_API_KEY=your-key-here`

### Gemini AI Setup
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env`: `GEMINI_API_KEY=your-key-here`

### Irrigation Settings
Adjust thresholds in `settings.py`:
```python
IRRIGATION_SETTINGS = {
    'CRITICAL_SOIL_MOISTURE': 25,
    'WARNING_SOIL_MOISTURE': 40,
    'OPTIMAL_SOIL_MOISTURE_MIN': 60,
    'OPTIMAL_SOIL_MOISTURE_MAX': 70,
}
