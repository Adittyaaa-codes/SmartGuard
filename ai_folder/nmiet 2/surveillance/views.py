from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count, Q
from ai_surveillance.models import (
    Drone, Detection, Alert, SurveillanceSession, 
    FacialRecognition, ThreatAssessment, SystemMetrics,
    PatrolRoute, WeatherCondition
)
from ai_surveillance.object_detection import ObjectDetector, process_image_for_detection
import json
import random
from datetime import datetime, timedelta

def index(request):
    """Main view for the surveillance dashboard"""
    # Get dashboard data
    context = {
        'active_drones': Drone.objects.filter(status__in=['deployed', 'patrolling', 'scanning']).count(),
        'total_drones': Drone.objects.count(),
        'recent_alerts': Alert.objects.filter(status='new')[:5],
        'threat_level': get_current_threat_level(),
        'system_status': 'operational',
    }
    return render(request, 'surveillance/index.html', context)

def get_current_threat_level():
    """Calculate current threat level based on recent alerts"""
    recent_alerts = Alert.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=1)
    )
    
    if recent_alerts.filter(severity='critical').exists():
        return 'critical'
    elif recent_alerts.filter(severity='high').exists():
        return 'high'
    elif recent_alerts.filter(severity='medium').exists():
        return 'medium'
    else:
        return 'low'

@csrf_exempt
def api_drone_status(request):
    """API endpoint for drone status"""
    if request.method == 'GET':
        drones = Drone.objects.all()
        drone_data = []
        
        for drone in drones:
            drone_data.append({
                'id': drone.id,
                'name': drone.name,
                'type': drone.drone_type,
                'status': drone.status,
                'battery_level': drone.battery_level,
                'signal_strength': drone.signal_strength,
                'location': {
                    'lat': drone.last_location_lat,
                    'lng': drone.last_location_lng
                },
                'last_active': drone.last_active.isoformat() if drone.last_active else None
            })
        
        return JsonResponse({
            'success': True,
            'drones': drone_data,
            'total_count': len(drone_data),
            'active_count': len([d for d in drone_data if d['status'] in ['deployed', 'patrolling', 'scanning']])
        })
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def api_drone_control(request):
    """API endpoint for drone control operations"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            drone_id = data.get('drone_id')
            action = data.get('action')
            
            drone = Drone.objects.get(id=drone_id)
            
            if action == 'deploy':
                result = drone.deploy()
                message = f"{drone.name} deployed successfully"
            elif action == 'recall':
                result = drone.recall()
                message = f"{drone.name} recalled to base"
            elif action == 'scan':
                result = drone.scan_area()
                message = f"{drone.name} performing area scan"
            else:
                return JsonResponse({'success': False, 'error': 'Invalid action'})
            
            if result:
                return JsonResponse({
                    'success': True,
                    'message': message,
                    'drone_status': drone.status
                })
            else:
                return JsonResponse({'success': False, 'error': 'Operation failed'})
                
        except Drone.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Drone not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def api_object_detection(request):
    """API endpoint for object detection"""
    if request.method == 'POST':
        try:
            # Simulate object detection process
            detector = ObjectDetector()
            detections = detector.detect_objects()
            analysis = detector.analyze_detections(detections)
            
            # Store detection results
            for detection_data in detections:
                Detection.objects.create(
                    object_type=detection_data['class'],
                    confidence=detection_data['confidence'] * 100,
                    timestamp=timezone.now()
                )
            
            # Create alert if high-risk objects detected
            if analysis['threat_level'] in ['high', 'critical']:
                Alert.objects.create(
                    title=f"High-Risk Detection Alert",
                    description=analysis['summary'],
                    severity=analysis['threat_level'],
                    status='new'
                )
            
            return JsonResponse({
                'success': True,
                'detections': detections,
                'analysis': analysis,
                'total_objects': analysis['total_objects']
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def api_alerts(request):
    """API endpoint for alerts management"""
    if request.method == 'GET':
        alerts = Alert.objects.all()[:20]  # Get latest 20 alerts
        alert_data = []
        
        for alert in alerts:
            alert_data.append({
                'id': alert.id,
                'title': alert.title,
                'description': alert.description,
                'severity': alert.severity,
                'status': alert.status,
                'created_at': alert.created_at.isoformat(),
                'updated_at': alert.updated_at.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'alerts': alert_data,
            'total_count': Alert.objects.count(),
            'new_count': Alert.objects.filter(status='new').count()
        })
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            alert_id = data.get('alert_id')
            action = data.get('action')
            
            alert = Alert.objects.get(id=alert_id)
            
            if action == 'acknowledge':
                alert.status = 'acknowledged'
                alert.save()
                message = "Alert acknowledged"
            elif action == 'resolve':
                alert.status = 'resolved'
                alert.save()
                message = "Alert resolved"
            else:
                return JsonResponse({'success': False, 'error': 'Invalid action'})
            
            return JsonResponse({
                'success': True,
                'message': message,
                'alert_status': alert.status
            })
            
        except Alert.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Alert not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def api_system_metrics(request):
    """API endpoint for system metrics"""
    if request.method == 'GET':
        # Generate simulated system metrics
        current_metrics = {
            'timestamp': timezone.now().isoformat(),
            'cpu_usage': random.uniform(20, 80),
            'memory_usage': random.uniform(30, 70),
            'disk_usage': random.uniform(40, 60),
            'network_latency': random.uniform(10, 50),
            'active_drones': Drone.objects.filter(status__in=['deployed', 'patrolling', 'scanning']).count(),
            'detections_per_hour': Detection.objects.filter(
                timestamp__gte=timezone.now() - timedelta(hours=1)
            ).count(),
            'system_uptime': random.uniform(100, 500),
            'threat_level': get_current_threat_level(),
            'total_alerts': Alert.objects.count(),
            'new_alerts': Alert.objects.filter(status='new').count()
        }
        
        # Store metrics
        SystemMetrics.objects.create(**{
            k: v for k, v in current_metrics.items() 
            if k not in ['timestamp', 'threat_level']
        })
        
        return JsonResponse({
            'success': True,
            'metrics': current_metrics
        })
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def api_analytics_data(request):
    """API endpoint for analytics charts data"""
    if request.method == 'GET':
        # Detection frequency data (last 24 hours)
        now = timezone.now()
        hours = []
        detection_counts = []
        
        for i in range(24):
            hour_start = now - timedelta(hours=i+1)
            hour_end = now - timedelta(hours=i)
            count = Detection.objects.filter(
                timestamp__gte=hour_start,
                timestamp__lt=hour_end
            ).count()
            
            hours.append(hour_start.strftime('%H:00'))
            detection_counts.append(count)
        
        hours.reverse()
        detection_counts.reverse()
        
        # Object type distribution
        object_types = Detection.objects.values('object_type').annotate(
            count=Count('object_type')
        ).order_by('-count')
        
        # Threat level distribution
        threat_levels = Alert.objects.values('severity').annotate(
            count=Count('severity')
        ).order_by('-count')
        
        return JsonResponse({
            'success': True,
            'detection_frequency': {
                'labels': hours,
                'data': detection_counts
            },
            'object_distribution': {
                'labels': [obj['object_type'] for obj in object_types],
                'data': [obj['count'] for obj in object_types]
            },
            'threat_distribution': {
                'labels': [threat['severity'] for threat in threat_levels],
                'data': [threat['count'] for threat in threat_levels]
            }
        })
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def api_live_feed(request):
    """API endpoint for live feed simulation"""
    if request.method == 'GET':
        # Simulate live feed data
        feed_data = {
            'status': 'active',
            'timestamp': timezone.now().isoformat(),
            'resolution': '1920x1080',
            'fps': 30,
            'quality': 'HD',
            'zoom_level': 1.0,
            'night_vision': False,
            'thermal_imaging': False,
            'motion_detected': random.choice([True, False]),
            'recording': True
        }
        
        return JsonResponse({
            'success': True,
            'feed_data': feed_data
        })
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

def simulate_real_time_data(request):
    """Generate simulated real-time data for demo purposes"""
    # This would typically be called by a background task or WebSocket
    
    # Simulate drone battery updates
    for drone in Drone.objects.filter(status__in=['deployed', 'patrolling']):
        if random.random() < 0.3:  # 30% chance to update battery
            new_battery = max(0, drone.battery_level - random.randint(1, 5))
            drone.update_battery(new_battery)
    
    # Simulate random detections
    if random.random() < 0.4:  # 40% chance of detection
        detector = ObjectDetector()
        detections = detector.detect_objects()
        
        for detection_data in detections:
            Detection.objects.create(
                object_type=detection_data['class'],
                confidence=detection_data['confidence'] * 100,
                timestamp=timezone.now()
            )
    
    # Simulate alerts
    if random.random() < 0.1:  # 10% chance of alert
        alert_types = [
            ("Perimeter Breach", "Unauthorized access detected in Sector 7", "medium"),
            ("Suspicious Activity", "Unusual movement pattern detected", "low"),
            ("Weapon Detection", "Potential weapon identified", "high"),
            ("System Anomaly", "Drone communication interrupted", "medium"),
        ]
        
        title, desc, severity = random.choice(alert_types)
        Alert.objects.create(
            title=title,
            description=desc,
            severity=severity,
            status='new'
        )
    
    return JsonResponse({'success': True, 'message': 'Simulation updated'})
