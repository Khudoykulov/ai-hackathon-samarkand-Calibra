// UNIVERSAL API CLIENT - Barcha sahifalar uchun
class UniversalAPI {
    constructor() {
        this.retryCount = 0;
        this.maxRetries = 2;
        
        console.log('🚀 UniversalAPI initialized');
    }

    // CSRF Token olish
    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return decodeURIComponent(value);
            }
        }
        return '';
    }

    // Universal API request method
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
            
            const data = await response.json();
            
            // API xatoligi tekshiruvi
            if (data.error) {
                throw new Error(`API Error: ${data.error}`);
            }
            
            return data;
        } catch (error) {
            console.error(`API Request failed: ${url}`, error);
            
            // Network xatoliklari uchun retry
            if (this.retryCount < this.maxRetries && !error.message.includes('API Error')) {
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

    // Notification system
    showNotification(message, type = 'info') {
        document.querySelectorAll('.notification').forEach(n => n.remove());
        
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        
        let icon = '';
        switch(type) {
            case 'error': icon = '❌ '; break;
            case 'warning': icon = '⚠️ '; break;
            case 'success': icon = '✅ '; break;
            case 'info': icon = 'ℹ️ '; break;
        }
        
        notification.innerHTML = `${icon}${message}`;
        notification.addEventListener('click', () => notification.remove());
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 4000);

        console.log(`[${type.toUpperCase()}] ${message}`);
    }

    // Weather API methods
    async getWeatherData() {
        try {
            const data = await this.makeRequest('/api/sensor/weather/');
            return data;
        } catch (error) {
            console.error('Weather API error:', error);
            return this.getEmptyWeatherData();
        }
    }

    async getWeatherForecast() {
        try {
            const data = await this.makeRequest('/api/sensor/weather-forecast/');
            return data;
        } catch (error) {
            console.error('Weather forecast error:', error);
            return { error: true, forecasts: [] };
        }
    }

    // Sensor API methods
    async getSensorData() {
        try {
            const data = await this.makeRequest('/api/realtime/');
            return data;
        } catch (error) {
            console.error('Sensors API error:', error);
            return { error: true, sensors: [] };
        }
    }

    // AI API methods
    async getAIAnalysis() {
        try {
            const data = await this.makeRequest('/api/ai/comprehensive-analysis/', {
                method: 'POST'
            });
            return data;
        } catch (error) {
            console.error('AI API error:', error);
            return { error: true, analysis_result: null };
        }
    }

    // Empty data methods
    getEmptyWeatherData() {
        return {
            location: '-',
            temperature: '-',
            humidity: '-',
            pressure: '-',
            wind_speed: '-',
            wind_direction: '-',
            rainfall: '-',
            weather_condition: 'Ma\'lumot yo\'q',
            icon: '-',
            visibility: '-',
            uv_index: '-',
            air_quality_index: '-',
            feels_like_temperature: '-',
            cloud_coverage: '-',
            dew_point: '-',
            wind_gust: '-',
            solar_radiation: '-',
            error: true
        };
    }

    getEmptyAIData() {
        return {
            decision: 'unavailable',
            reasoning: 'AI ma\'lumotlari yo\'q',
            confidence_percentage: 0,
            recommendations: ['AI ishlamayapti'],
            error: true
        };
    }

    // Utility methods
    formatTime(timestamp) {
        if (!timestamp) return 'Noma\'lum vaqt';
        
        try {
            const date = new Date(timestamp);
            return date.toLocaleTimeString('uz-UZ', { 
                hour: '2-digit', 
                minute: '2-digit',
                second: '2-digit'
            });
        } catch {
            return 'Noma\'lum vaqt';
        }
    }

    formatDate(dateStr) {
        if (!dateStr) return 'Noma\'lum sana';
        
        try {
            const date = new Date(dateStr);
            return date.toLocaleDateString('uz-UZ', {
                weekday: 'short',
                month: 'short',
                day: 'numeric'
            });
        } catch {
            return 'Noma\'lum sana';
        }
    }
}

// Global instance
window.universalAPI = new UniversalAPI();
window.showNotification = window.universalAPI.showNotification.bind(window.universalAPI);

// Legacy compatibility
window.dashboardAPI = window.universalAPI;

console.log('✅ Universal API client loaded successfully');