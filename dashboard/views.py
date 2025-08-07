from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import json


def index(request):
    """Serve the main dashboard HTML"""
    return render(request, 'dashboard.html')


@api_view(['GET'])
def dashboard_data(request):
    """API endpoint for dashboard data"""
    try:
        from sensor.views import DashboardViewSet
        from controller.views import SystemStatusViewSet

        # Get dashboard overview
        dashboard_viewset = DashboardViewSet()
        dashboard_response = dashboard_viewset.overview(request)

        # Get system status
        status_viewset = SystemStatusViewSet()
        status_response = status_viewset.current_status(request)

        return Response({
            'dashboard': dashboard_response.data,
            'system_status': status_response.data,
            'timestamp': timezone.now()
        })

    except Exception as e:
        return Response({
            'error': 'Failed to get dashboard data',
            'details': str(e)
        }, status=500)


@api_view(['POST'])
def update_sensor_data(request):
    """Update sensor data (for testing)"""
    try:
        from sensor.views import SensorViewSet

        sensor_viewset = SensorViewSet()
        response = sensor_viewset.generate_test_data(request)

        return response

    except Exception as e:
        return Response({
            'error': 'Failed to update sensor data',
            'details': str(e)
        }, status=500)
