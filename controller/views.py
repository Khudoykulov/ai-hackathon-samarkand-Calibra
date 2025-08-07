from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import IrrigationSystem, IrrigationEvent, SystemControl
from .serializers import IrrigationSystemSerializer, IrrigationEventSerializer, SystemControlSerializer

class IrrigationSystemViewSet(viewsets.ModelViewSet):
    queryset = IrrigationSystem.objects.all()
    serializer_class = IrrigationSystemSerializer
    
    @action(detail=True, methods=['post'])
    def start_irrigation(self, request, pk=None):
        """Start irrigation manually"""
        system = self.get_object()
        duration = request.data.get('duration_minutes', 15)
        
        # Check if there's already a running irrigation
        running_event = IrrigationEvent.objects.filter(
            system=system,
            status='running'
        ).first()
        
        if running_event:
            return Response(
                {'error': 'Irrigation is already running'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create new irrigation event
        event = IrrigationEvent.objects.create(
            system=system,
            status='running',
            trigger_type='manual',
            scheduled_start=timezone.now(),
            actual_start=timezone.now(),
            duration_minutes=duration
        )
        
        # Log control command
        SystemControl.objects.create(
            command='start_irrigation',
            parameters={'system_id': system.id, 'duration': duration},
            success=True,
            response=f'Irrigation started for {duration} minutes'
        )
        
        return Response({
            'message': 'Irrigation started successfully',
            'event_id': event.id,
            'duration_minutes': duration
        })
    
    @action(detail=True, methods=['post'])
    def stop_irrigation(self, request, pk=None):
        """Stop irrigation manually"""
        system = self.get_object()
        
        # Find running irrigation
        running_event = IrrigationEvent.objects.filter(
            system=system,
            status='running'
        ).first()
        
        if not running_event:
            return Response(
                {'error': 'No running irrigation found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Stop irrigation
        running_event.status = 'completed'
        running_event.actual_end = timezone.now()
        running_event.save()
        
        # Log control command
        SystemControl.objects.create(
            command='stop_irrigation',
            parameters={'system_id': system.id, 'event_id': running_event.id},
            success=True,
            response='Irrigation stopped manually'
        )
        
        return Response({
            'message': 'Irrigation stopped successfully',
            'event_id': running_event.id
        })
    
    @action(detail=False, methods=['get'])
    def status(self, request):
        """Get current system status"""
        systems = IrrigationSystem.objects.filter(is_active=True)
        status_data = []
        
        for system in systems:
            running_event = IrrigationEvent.objects.filter(
                system=system,
                status='running'
            ).first()
            
            recent_events = IrrigationEvent.objects.filter(
                system=system,
                created_at__gte=timezone.now() - timedelta(days=7)
            ).count()
            
            status_data.append({
                'id': system.id,
                'name': system.name,
                'location': system.location,
                'is_active': system.is_active,
                'is_automatic': system.is_automatic,
                'is_running': bool(running_event),
                'current_event': running_event.id if running_event else None,
                'recent_events_count': recent_events
            })
        
        return Response(status_data)

class IrrigationEventViewSet(viewsets.ModelViewSet):
    queryset = IrrigationEvent.objects.all()
    serializer_class = IrrigationEventSerializer
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get irrigation statistics"""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        events = IrrigationEvent.objects.filter(
            created_at__gte=start_date,
            status='completed'
        )
        
        total_events = events.count()
        total_water = sum(e.water_amount_liters or 0 for e in events)
        avg_duration = sum(e.duration_minutes for e in events) / total_events if total_events > 0 else 0
        
        # Events by trigger type
        trigger_stats = {}
        for event in events:
            trigger = event.trigger_type
            trigger_stats[trigger] = trigger_stats.get(trigger, 0) + 1
        
        return Response({
            'period_days': 30,
            'total_events': total_events,
            'total_water_liters': round(total_water, 2),
            'average_duration_minutes': round(avg_duration, 2),
            'trigger_statistics': trigger_stats
        })

class SystemControlViewSet(viewsets.ModelViewSet):
    queryset = SystemControl.objects.all()
    serializer_class = SystemControlSerializer
    
    @action(detail=False, methods=['post'])
    def execute_command(self, request):
        """Execute system command"""
        command = request.data.get('command')
        parameters = request.data.get('parameters', {})
        
        if not command:
            return Response(
                {'error': 'Command is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Simulate command execution
        success = True
        response_message = f"Command '{command}' executed successfully"
        
        # Log the command
        control = SystemControl.objects.create(
            command=command,
            parameters=parameters,
            success=success,
            response=response_message
        )
        
        return Response({
            'id': control.id,
            'command': command,
            'success': success,
            'response': response_message,
            'executed_at': control.executed_at
        })
