from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard-home'),
    path('weather.html', views.weather_page, name='weather-page'),
    path('sensors.html', views.sensors_page, name='sensors-page'),
    path('ai.html', views.ai_page, name='ai-page'),
    path('settings.html', views.settings_page, name='settings-page'),
    path('api/overview/', views.get_dashboard_overview, name='dashboard-overview'),
    path('api/realtime/', views.get_realtime_data, name='realtime-data'),
    path('api/statistics/', views.get_statistics_data, name='statistics-data'),
    path('api/system-health/', views.get_system_health, name='system-health'),
    path('api/weather-forecast/', views.get_weather_forecast, name='weather-forecast'),
    path('api/irrigation-schedule/', views.get_irrigation_schedule, name='irrigation-schedule'),
    path('api/settings/', views.update_dashboard_settings, name='update-settings'),
]