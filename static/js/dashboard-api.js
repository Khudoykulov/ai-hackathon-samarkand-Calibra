// Enhanced API integration for Django backend
class DashboardAPI {
    constructor() {
        this.baseURL = '/api';
        this.updateInterval = 30000; // 30 seconds
        this.isLoading = false;
        this.retryCount = 0;
        this.maxRetries = 3;
        this.init();
    }

    init() {
        this.loadDashboardData();
        this.startLiveUpdates();
        this.bindEvents();
        this.setupErrorHandling();
    }

    setupErrorHandling() {
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            this.showNotification('Kutilmagan xatolik yuz berdi', 'error');
        });
    }

    async makeRequest(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken(),
            },
            credentials: 'same-origin'
        };

        const finalOptions = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, finalOptions);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            if (this.retryCount < this.maxRetries) {
                this.retryCount++;
                await this.delay(1000 * this.retryCount);
                return this.makeRequest(url, options);
            }
            
            this.retryCount = 0;
            throw error;
        }
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    getCSRFToken() {
        // Try to get CSRF token from various sources
        const token = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                     document.querySelector('meta[name=csrf-token]')?.content ||
                     this.getCookie('csrftoken');
        return token || '';
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    async loadDashboardData() {
        if (this.isLoading) return;
        this.isLoading = true;

        try {
            const data = await this.makeRequest(`${this.baseURL}/dashboard-data/`);
            this.updateDashboard(data);
            this.retryCount = 0; // Reset retry count on success
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showNotification('Dashboard ma\'lumotlari yuklanmadi', 'error');
        } finally {
            this.isLoading = false;
        }
    }

    async loadSensorData() {
        try {
            // Load current sensor status
            const currentStatus = await this.makeRequest(`${this.baseURL}/sensor/sensors/current_status/`);
            this.updateSensorCards(currentStatus);

            // Load sensor statistics
            const statistics = await this.makeRequest(`${this.baseURL}/sensor/readings/statistics/`);
            this.updateSensorStatistics(statistics);

            // Generate new random data for demo
            await this.makeRequest(`${this.baseURL}/sensor/sensors/generate_random_data/`, {
                method: 'GET'
            });

        } catch (error) {
            console.error('Error loading sensor data:', error);
            this.showNotification('Sensor ma\'lumotlari yuklanmadi', 'error');
        }
    }

    async loadWeatherData() {
        try {
            // Load current weather
            const current = await this.makeRequest(`${this.baseURL}/sensor/weather/current/`);
            this.updateWeatherCards(current);

            // Load forecast
            const forecast = await this.makeRequest(`${this.baseURL}/sensor/weather/forecast/`);
            this.updateWeatherForecast(forecast);

        } catch (error) {
            console.error('Error loading weather data:', error);
            this.showNotification('Ob-havo ma\'lumotlari yuklanmadi', 'error');
        }
    }

    async loadAIAnalysis() {
        try {
            // Trigger AI analysis
            const analysis = await this.makeRequest(`${this.baseURL}/ai/analysis/analyze_current_conditions/`, {
                method: 'POST'
            });
            this.updateAIAnalysis(analysis);

            // Load current AI model info
            const modelInfo = await this.makeRequest(`${this.baseURL}/ai/models/current_model/`);
            this.updateAIModelInfo(modelInfo);

            // Load recent decisions
            const recentDecisions = await this.makeRequest(`${this.baseURL}/ai/analysis/recent_decisions/`);
            this.updateAITimeline(recentDecisions);

            // Load performance metrics
            const performance = await this.makeRequest(`${this.baseURL}/ai/analysis/performance_metrics/`);
            this.updateAIPerformance(performance);

        } catch (error) {
            console.error('Error loading AI analysis:', error);
            this.showNotification('AI tahlil ma\'lumotlari yuklanmadi', 'error');
        }
    }

    async loadLiveFeed() {
        try {
            const data = await this.makeRequest(`${this.baseURL}/live-feed/`);
            this.updateLiveFeed(data);
        } catch (error) {
            console.error('Error loading live feed:', error);
        }
    }

    async loadStatistics() {
        try {
            // Load irrigation statistics
            const irrigationStats = await this.makeRequest(`${this.baseURL}/controller/events/statistics/`);
            
            // Load AI performance metrics
            const aiMetrics = await this.makeRequest(`${this.baseURL}/ai/analysis/performance_metrics/`);
            
            // Load sensor statistics
            const sensorStats = await this.makeRequest(`${this.baseURL}/sensor/readings/statistics/`);

            this.updateStatistics({
                irrigation: irrigationStats,
                ai: aiMetrics,
                sensors: sensorStats
            });

        } catch (error) {
            console.error('Error loading statistics:', error);
            this.showNotification('Statistika ma\'lumotlari yuklanmadi', 'error');
        }
    }

    async loadSystemControl() {
        try {
            const systemStatus = await this.makeRequest(`${this.baseURL}/controller/systems/status/`);
            this.updateSystemControl(systemStatus);
        } catch (error) {
            console.error('Error loading system control:', error);
        }
    }

    // Update methods
    updateDashboard(data) {
        if (data.system_status) this.updateSystemStatus(data.system_status);
        if (data.sensors) this.updateDashboardSensors(data.sensors);
        if (data.weather) this.updateDashboardWeather(data.weather);
        if (data.ai_analysis) this.updateDashboardAI(data.ai_analysis);
        if (data.statistics) this.updateDashboardStatistics(data.statistics);
    }

    updateSystemStatus(status) {
        // Update system status cards
        this.updateStatusCard('systemStatus', {
            value: status.system_active ? 'FAOL' : 'NOFAOL',
            class: status.system_active ? '' : 'warning'
        });

        this.updateStatusCard('irrigationStatus', {
            value: status.irrigation_running ? 'SUGH.' : 'KUTISH',
            class: status.irrigation_running ? 'danger' : ''
        });

        this.updateStatusCard('waterLevel', {
            value: status.critical_sensors?.length > 0 ? 'KRITIK' : 'NORMAL',
            class: status.critical_sensors?.length > 0 ? 'danger' : ''
        });
    }

    updateStatusCard(cardId, { value, class: className }) {
        const card = document.getElementById(cardId);
        if (card) {
            const valueElement = card.querySelector('.status-value');
            if (valueElement) valueElement.textContent = value;
            
            card.className = `status-card ${className}`;
        }
    }

    updateDashboardSensors(sensors) {
        // Update soil moisture
        const soilSensor = sensors.find(s => 
            s.type.toLowerCase().includes('namlik') || 
            s.name.toLowerCase().includes('namlik')
        );
        
        if (soilSensor) {
            this.updateProgressBar('soilMoistureFill', soilSensor.value, {
                valueElement: 'soilMoistureValue',
                unit: '%',
                statusClass: soilSensor.status
            });
        }

        // Update pH
        const phSensor = sensors.find(s => 
            s.type.toLowerCase().includes('ph') || 
            s.name.toLowerCase().includes('ph')
        );
        
        if (phSensor) {
            this.updateProgressBar('phFill', (phSensor.value / 14) * 100, {
                valueElement: 'phValue',
                value: phSensor.value,
                unit: '',
                statusClass: 'normal'
            });
        }

        // Update soil temperature
        const soilTempSensor = sensors.find(s => 
            s.type.toLowerCase().includes('tuproq') && 
            s.type.toLowerCase().includes('harorat')
        );
        
        if (soilTempSensor) {
            this.updateProgressBar('soilTempFill', (soilTempSensor.value / 50) * 100, {
                valueElement: 'soilTempValue',
                value: soilTempSensor.value,
                unit: '°C',
                statusClass: 'normal'
            });
        }
    }

    updateProgressBar(fillId, percentage, options = {}) {
        const fillElement = document.getElementById(fillId);
        if (fillElement) {
            fillElement.style.width = `${Math.min(100, Math.max(0, percentage))}%`;
            
            if (options.statusClass) {
                fillElement.className = `progress-fill ${options.statusClass === 'critical' ? 'critical' : options.statusClass === 'warning' ? 'warning' : ''}`;
            }
        }

        if (options.valueElement) {
            const valueElement = document.getElementById(options.valueElement);
            if (valueElement) {
                const displayValue = options.value !== undefined ? options.value : percentage;
                valueElement.textContent = `${Math.round(displayValue * 100) / 100}${options.unit || ''}`;
            }
        }
    }

    updateDashboardWeather(weather) {
        const updates = {
            currentTemp: `${Math.round(weather.temperature)}°C`,
            currentHumidity: `${Math.round(weather.humidity)}%`,
            currentRainfall: `${weather.rainfall}mm`
        };

        Object.entries(updates).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) element.textContent = value;
        });
    }

    updateDashboardAI(analysis) {
        // Update AI decision display
        const decisionElement = document.getElementById('aiDecision');
        if (decisionElement) {
            decisionElement.textContent = this.getDecisionText(analysis.decision);
        }

        // Update reasoning
        const reasoningElement = document.getElementById('aiReasoning');
        if (reasoningElement) {
            reasoningElement.textContent = analysis.reasoning || 'Tahlil davom etmoqda...';
        }

        // Update confidence
        this.updateProgressBar('aiConfidenceFill', analysis.confidence_percentage, {
            valueElement: 'aiConfidenceValue',
            value: analysis.confidence_percentage,
            unit: '%'
        });

        // Update recommendations
        const recommendationsList = document.getElementById('aiRecommendationsList');
        if (recommendationsList && analysis.recommendations) {
            recommendationsList.innerHTML = analysis.recommendations
                .map(rec => `<li>${rec}</li>`)
                .join('');
        }
    }

    updateLiveFeed(feedData) {
        const liveFeed = document.getElementById('liveFeed');
        if (!liveFeed) return;

        // Clear existing content
        liveFeed.innerHTML = '';

        // Add new entries with animation
        feedData.forEach((entry, index) => {
            const entryElement = document.createElement('div');
            entryElement.className = `data-entry ${entry.status_class}`;
            entryElement.innerHTML = `
                <span class="timestamp">[${entry.timestamp}]</span>
                ${entry.message}
            `;
            
            // Add animation delay
            entryElement.style.animationDelay = `${index * 0.1}s`;
            liveFeed.appendChild(entryElement);
        });
    }

    updateSensorCards(sensors) {
        const sensorsGrid = document.getElementById('sensorsGrid');
        if (!sensorsGrid) return;

        sensorsGrid.innerHTML = '';

        sensors.forEach(sensor => {
            const sensorCard = document.createElement('div');
            sensorCard.className = `sensor-card ${sensor.status}`;
            sensorCard.setAttribute('data-sensor-id', sensor.id);
            
            sensorCard.innerHTML = `
                <div class="sensor-name">${this.getSensorIcon(sensor.type)} ${sensor.name}</div>
                <div class="sensor-value">${sensor.value}${sensor.unit}</div>
                <div class="sensor-status">${this.getStatusText(sensor.status)}</div>
                <div style="margin-top: 10px; font-size: 0.8rem; opacity: 0.6;">
                    Joylashuv: ${sensor.location}<br>
                    Oxirgi yangilanish: ${this.getTimeAgo(sensor.timestamp)}
                </div>
            `;
            
            sensorsGrid.appendChild(sensorCard);
        });
    }

    updateSensorStatistics(stats) {
        const tableBody = document.getElementById('sensorsTableBody');
        if (!tableBody) return;

        tableBody.innerHTML = '';

        stats.forEach(stat => {
            const row = document.createElement('tr');
            const statusColor = this.getValueColor(stat.sensor_type, stat.current_value);
            
            row.innerHTML = `
                <td>${this.getSensorIcon(stat.sensor_type)} ${stat.sensor_name}</td>
                <td style="color: ${statusColor}; font-weight: bold;">${stat.current_value}${stat.unit}</td>
                <td>${stat.min_value}${stat.unit}</td>
                <td>${stat.max_value}${stat.unit}</td>
                <td>${stat.avg_value}${stat.unit}</td>
                <td style="color: ${statusColor};">${this.getStatusFromValue(stat.sensor_type, stat.current_value)}</td>
            `;
            
            tableBody.appendChild(row);
        });
    }

    updateWeatherCards(weather) {
        const weatherUpdates = {
            weatherTemp: `${Math.round(weather.temperature)}°C`,
            weatherHumidity: `${Math.round(weather.humidity)}%`,
            weatherRainfall: `${weather.rainfall}mm`,
            weatherWind: `${Math.round(weather.wind_speed)} km/h`,
            weatherSolar: `${Math.round(weather.solar_radiation)} W/m²`,
            weatherPressure: `${Math.round(weather.pressure)}`,
            windDirection: weather.wind_direction || '--',
            humidityStatus: weather.humidity < 50 ? 'Quruq havo' : 'Normal',
            solarStatus: weather.solar_radiation > 800 ? 'Yuqori daraja' : 'O\'rtacha'
        };

        Object.entries(weatherUpdates).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) element.textContent = value;
        });
    }

    updateWeatherForecast(forecast) {
        // Update forecast chart if forecast data is available
        if (!forecast || !Array.isArray(forecast)) return;

        const forecastChart = document.getElementById('forecastChart');
        const forecastDays = document.getElementById('forecastDays');
        const forecastIcons = document.getElementById('forecastIcons');

        if (forecastChart) {
            const bars = forecastChart.children;
            forecast.slice(0, 7).forEach((day, index) => {
                if (bars[index]) {
                    const height = Math.min(90, Math.max(20, (day.temperature / 35) * 100));
                    bars[index].style.height = `${height}%`;
                    bars[index].title = `${day.temperature}°C`;
                }
            });
        }

        if (forecastDays) {
            forecastDays.innerHTML = forecast.slice(0, 7)
                .map(day => `<span>${day.day_name?.substring(0, 3) || 'N/A'}</span>`)
                .join('');
        }

        if (forecastIcons) {
            forecastIcons.innerHTML = forecast.slice(0, 7)
                .map(day => `<span>${this.getWeatherIcon(day.condition)}</span>`)
                .join('');
        }
    }

    // Control actions
    async handleControlAction(button) {
        const action = button.getAttribute('data-action');
        if (!action) return;

        // Visual feedback
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = '';
        }, 150);

        try {
            let result;

            switch (action) {
                case 'start_irrigation':
                    result = await this.makeRequest(`${this.baseURL}/controller/systems/1/start_irrigation/`, {
                        method: 'POST',
                        body: JSON.stringify({ duration_minutes: 15 })
                    });
                    break;

                case 'stop_irrigation':
                    result = await this.makeRequest(`${this.baseURL}/controller/systems/1/stop_irrigation/`, {
                        method: 'POST'
                    });
                    break;

                case 'auto_mode':
                case 'manual_mode':
                    // Handle mode switching
                    document.querySelectorAll('[data-action="auto_mode"], [data-action="manual_mode"]')
                        .forEach(btn => btn.classList.remove('active'));
                    button.classList.add('active');
                    this.showNotification(`${action === 'auto_mode' ? 'Avtomatik' : 'Qo\'lda'} rejim yoqildi`, 'success');
                    return;

                default:
                    // Handle other control commands
                    result = await this.makeRequest(`${this.baseURL}/controller/controls/execute_command/`, {
                        method: 'POST',
                        body: JSON.stringify({
                            command: action,
                            parameters: {}
                        })
                    });
                    break;
            }

            if (result && result.success !== false) {
                this.showNotification('Buyruq muvaffaqiyatli bajarildi', 'success');
                // Refresh dashboard data
                setTimeout(() => this.loadDashboardData(), 1000);
            } else {
                this.showNotification(result?.error || 'Xatolik yuz berdi', 'error');
            }

        } catch (error) {
            console.error('Control action error:', error);
            this.showNotification('Aloqa xatosi yuz berdi', 'error');
        }
    }

    // Event binding
    bindEvents() {
        // Control button events
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('control-btn') || e.target.closest('.control-btn')) {
                const button = e.target.classList.contains('control-btn') ? e.target : e.target.closest('.control-btn');
                this.handleControlAction(button);
            }
        });

        // Navigation events
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('nav-link')) {
                const page = e.target.getAttribute('data-page');
                if (page) {
                    setTimeout(() => this.loadPageData(page), 100);
                }
            }
        });

        // Refresh buttons
        document.addEventListener('click', (e) => {
            if (e.target.dataset.action === 'refresh') {
                const activePage = document.querySelector('.page.active');
                if (activePage) {
                    this.loadPageData(activePage.id);
                }
            }
        });
    }

    loadPageData(page) {
        switch (page) {
            case 'dashboard':
                this.loadDashboardData();
                break;
            case 'sensors':
                this.loadSensorData();
                break;
            case 'weather':
                this.loadWeatherData();
                break;
            case 'ai':
                this.loadAIAnalysis();
                break;
            case 'statistics':
                this.loadStatistics();
                break;
            case 'control':
                this.loadSystemControl();
                break;
        }
    }

    startLiveUpdates() {
        // Live feed updates - more frequent
        setInterval(() => {
            this.loadLiveFeed();
        }, 15000);

        // Main data updates - less frequent
        setInterval(() => {
            const activePage = document.querySelector('.page.active');
            if (activePage) {
                this.loadPageData(activePage.id);
            }
        }, this.updateInterval);

        // Generate random sensor data for demo
        setInterval(async () => {
            try {
                await this.makeRequest(`${this.baseURL}/sensor/sensors/generate_random_data/`);
            } catch (error) {
                // Silently fail for demo data generation
            }
        }, 45000);
    }

    // Utility methods
    getSensorIcon(sensorType) {
        const type = sensorType.toLowerCase();
        if (type.includes('namlik')) return '🌍';
        if (type.includes('harorat')) return '🌡️';
        if (type.includes('ph')) return '⚡';
        if (type.includes('havo')) return '💨';
        if (type.includes('yorug')) return '☀️';
        if (type.includes('yomg')) return '🌧️';
        if (type.includes('o\'tkazuvchan')) return '🔌';
        return '📊';
    }

    getStatusText(status) {
        const statusMap = {
            'critical': 'Kritik - Darhol harakat kerak',
            'warning': 'Ogohlantirish - Kuzatish kerak',
            'normal': 'Normal - Optimal daraja'
        };
        return statusMap[status] || 'Noma\'lum';
    }

    getDecisionText(decision) {
        const decisionMap = {
            'urgent_irrigation': 'Darhol sug\'orish kerak!',
            'irrigation_needed': 'Sug\'orish tavsiya etiladi',
            'no_action': 'Harakat kerak emas',
            'stop_irrigation': 'Sug\'orishni to\'xtatish',
            'adjust_schedule': 'Jadvalni o\'zgartirish'
        };
        return decisionMap[decision] || decision;
    }

    getValueColor(sensorType, value) {
        if (sensorType.toLowerCase().includes('namlik')) {
            if (value < 25) return '#ff416c';
            if (value < 40) return '#ff9a00';
            return '#00ff87';
        }
        if (sensorType.toLowerCase().includes('harorat')) {
            if (value > 35 || value < 10) return '#ff9a00';
            return '#00ff87';
        }
        return '#00ff87';
    }

    getStatusFromValue(sensorType, value) {
        if (sensorType.toLowerCase().includes('namlik')) {
            if (value < 25) return 'Kritik';
            if (value < 40) return 'Past';
            return 'Normal';
        }
        if (sensorType.toLowerCase().includes('harorat')) {
            if (value > 35) return 'Yuqori';
            if (value < 10) return 'Past';
            return 'Normal';
        }
        return 'Normal';
    }

    getWeatherIcon(condition) {
        const iconMap = {
            'sunny': '☀️',
            'cloudy': '☁️',
            'partly_cloudy': '⛅',
            'rainy': '🌧️',
            'stormy': '⛈️'
        };
        return iconMap[condition] || '🌤️';
    }

    getTimeAgo(timestamp) {
        const now = new Date();
        const time = new Date(timestamp);
        const diffMs = now - time;
        const diffMins = Math.floor(diffMs / 60000);
        
        if (diffMins < 1) return 'Hozir';
        if (diffMins < 60) return `${diffMins} daqiqa oldin`;
        
        const diffHours = Math.floor(diffMins / 60);
        if (diffHours < 24) return `${diffHours} soat oldin`;
        
        const diffDays = Math.floor(diffHours / 24);
        return `${diffDays} kun oldin`;
    }

    showNotification(message, type = 'info') {
        // Remove existing notifications
        document.querySelectorAll('.notification').forEach(n => n.remove());

        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;

        // Add click to dismiss
        notification.addEventListener('click', () => notification.remove());

        document.body.appendChild(notification);

        // Auto remove after 4 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 4000);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeDashboard);
} else {
    initializeDashboard();
}

function initializeDashboard() {
    window.dashboardAPI = new DashboardAPI();
    
    // Add global error handler
    window.addEventListener('error', (e) => {
        console.error('Global error:', e.error);
    });
    
    // Add visibility change handler to pause/resume updates
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            // Pause updates when tab is not visible
            console.log('Tab hidden - pausing updates');
        } else {
            // Resume updates when tab becomes visible
            console.log('Tab visible - resuming updates');
            if (window.dashboardAPI) {
                window.dashboardAPI.loadDashboardData();
            }
        }
    });
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DashboardAPI;
}
