from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count, Q
from ai_surveillance.models import (
    Drone, Detection, Alert, SurveillanceSession, 
    FacialRecognition, ThreatAssessment, SystemMetrics,
    PatrolRoute, WeatherCondition, DroneActivity, SurveillanceZone
)
import json
import random
from datetime import datetime, timedelta

@csrf_exempt
def drone_list(request):
    """API endpoint for drone list and status"""
    if request.method == 'GET':
        drones = Drone.objects.all()
        drone_data = []
        
        for drone in drones:
            # Simulate real-time battery drain for active drones
            if drone.status in ['deployed', 'patrolling', 'scanning']:
                if random.random() < 0.3:  # 30% chance to update
                    new_battery = max(10, drone.battery_level - random.randint(1, 3))
                    drone.update_battery(new_battery)
            
            drone_data.append({
                'id': drone.id,
                'name': drone.name,
                'type': drone.drone_type,
                'status': drone.status,
                'battery_level': drone.battery_level,
                'signal_strength': drone.signal_strength,
                'location': {
                    'lat': drone.last_location_lat or (28.6139 + random.uniform(-0.01, 0.01)),
                    'lng': drone.last_location_lng or (77.2090 + random.uniform(-0.01, 0.01))
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
def drone_action(request, drone_id, action):
    """API endpoint for drone control actions"""
    if request.method == 'POST':
        try:
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
            elif action == 'patrol':
                drone.status = 'patrolling'
                drone.save()
                DroneActivity.objects.create(
                    drone=drone,
                    activity_type='status',
                    description=f"{drone.name} started patrolling"
                )
                result = True
                message = f"{drone.name} started patrolling"
            else:
                return JsonResponse({'success': False, 'error': 'Invalid action'})
            
            if result:
                return JsonResponse({
                    'success': True,
                    'message': message,
                    'drone_status': drone.status,
                    'drone_id': drone.id
                })
            else:
                return JsonResponse({'success': False, 'error': 'Operation failed'})
                
        except Drone.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Drone not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def drone_activities(request):
    """API endpoint for drone activities log"""
    if request.method == 'GET':
        activities = DroneActivity.objects.all()[:50]  # Latest 50 activities
        activity_data = []
        
        for activity in activities:
            activity_data.append({
                'id': activity.id,
                'drone_name': activity.drone.name,
                'activity_type': activity.activity_type,
                'description': activity.description,
                'timestamp': activity.timestamp.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'activities': activity_data,
            'total_count': DroneActivity.objects.count()
        })
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def detection_list(request):
    """API endpoint for detection results"""
    if request.method == 'GET':
        detections = Detection.objects.all()[:100]  # Latest 100 detections
        detection_data = []
        
        for detection in detections:
            detection_data.append({
                'id': detection.id,
                'object_type': detection.object_type,
                'confidence': detection.confidence,
                'location': {
                    'lat': detection.location_lat,
                    'lng': detection.location_lng
                },
                'drone_name': detection.drone.name if detection.drone else 'System',
                'timestamp': detection.timestamp.isoformat(),
                'image_url': detection.image.url if detection.image else None
            })
        
        # Get detection statistics
        stats = {
            'total_detections': Detection.objects.count(),
            'today_detections': Detection.objects.filter(
                timestamp__date=timezone.now().date()
            ).count(),
            'high_confidence': Detection.objects.filter(confidence__gte=80).count(),
            'object_types': list(Detection.objects.values('object_type').annotate(
                count=Count('object_type')
            ).order_by('-count'))
        }
        
        return JsonResponse({
            'success': True,
            'detections': detection_data,
            'statistics': stats
        })
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def alert_list(request):
    """API endpoint for alerts management"""
    if request.method == 'GET':
        alerts = Alert.objects.all()[:50]  # Latest 50 alerts
        alert_data = []
        
        for alert in alerts:
            alert_data.append({
                'id': alert.id,
                'title': alert.title,
                'description': alert.description,
                'severity': alert.severity,
                'status': alert.status,
                'zone_name': alert.zone.name if alert.zone else None,
                'created_at': alert.created_at.isoformat(),
                'updated_at': alert.updated_at.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'alerts': alert_data,
            'total_count': Alert.objects.count(),
            'new_count': Alert.objects.filter(status='new').count(),
            'critical_count': Alert.objects.filter(severity='critical', status='new').count()
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
            elif action == 'investigate':
                alert.status = 'investigating'
                alert.save()
                message = "Alert under investigation"
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
def surveillance_zones(request):
    """API endpoint for surveillance zones"""
    if request.method == 'GET':
        zones = SurveillanceZone.objects.filter(active=True)
        zone_data = []
        
        for zone in zones:
            zone_data.append({
                'id': zone.id,
                'name': zone.name,
                'description': zone.description,
                'coordinates': json.loads(zone.coordinates) if zone.coordinates else [],
                'priority': zone.priority,
                'active': zone.active,
                'alert_count': Alert.objects.filter(zone=zone, status='new').count()
            })
        
        return JsonResponse({
            'success': True,
            'zones': zone_data,
            'total_count': len(zone_data)
        })
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def simulate_detection(request):
    """API endpoint to simulate object detection"""
    if request.method == 'POST':
        try:
            # Simulate detection process
            detection_types = ['person', 'vehicle', 'weapon', 'animal', 'drone']
            weights = [0.4, 0.3, 0.1, 0.15, 0.05]  # Probability weights
            
            # Generate 1-5 random detections
            num_detections = random.randint(1, 5)
            detections = []
            
            for _ in range(num_detections):
                object_type = random.choices(detection_types, weights=weights)[0]
                confidence = random.uniform(60, 99)
                
                # Create detection record
                detection = Detection.objects.create(
                    object_type=object_type,
                    confidence=confidence,
                    location_lat=28.6139 + random.uniform(-0.01, 0.01),
                    location_lng=77.2090 + random.uniform(-0.01, 0.01),
                    drone=random.choice(Drone.objects.all()) if random.random() > 0.3 else None
                )
                
                detections.append({
                    'id': detection.id,
                    'object_type': object_type,
                    'confidence': confidence,
                    'location': {
                        'lat': detection.location_lat,
                        'lng': detection.location_lng
                    },
                    'timestamp': detection.timestamp.isoformat()
                })
                
                # Create threat assessment for weapons
                if object_type == 'weapon' and confidence > 80:
                    ThreatAssessment.objects.create(
                        detection=detection,
                        threat_type='weapon',
                        risk_score=random.uniform(70, 95),
                        description=f"High-confidence weapon detection ({confidence:.1f}%)",
                        recommended_action="Immediate security response required",
                        automated_response=True
                    )
                    
                    # Create high-priority alert
                    Alert.objects.create(
                        title="WEAPON DETECTED",
                        description=f"Weapon detected with {confidence:.1f}% confidence",
                        severity='critical',
                        status='new',
                        detection=detection
                    )
            
            # Calculate threat level
            weapon_detections = [d for d in detections if d['object_type'] == 'weapon']
            if weapon_detections:
                threat_level = 'critical'
            elif len(detections) > 3:
                threat_level = 'high'
            elif any(d['confidence'] > 90 for d in detections):
                threat_level = 'medium'
            else:
                threat_level = 'low'
            
            return JsonResponse({
                'success': True,
                'detections': detections,
                'analysis': {
                    'total_objects': len(detections),
                    'threat_level': threat_level,
                    'high_confidence_count': len([d for d in detections if d['confidence'] > 80]),
                    'summary': f"Detected {len(detections)} objects with threat level: {threat_level}"
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def dashboard_data(request):
    """API endpoint for dashboard overview data"""
    if request.method == 'GET':
        # Get current statistics
        now = timezone.now()
        today = now.date()
        
        # Drone statistics
        drone_stats = {
            'total': Drone.objects.count(),
            'active': Drone.objects.filter(status__in=['deployed', 'patrolling', 'scanning']).count(),
            'standby': Drone.objects.filter(status='standby').count(),
            'maintenance': Drone.objects.filter(status='maintenance').count(),
            'offline': Drone.objects.filter(status='offline').count()
        }
        
        # Detection statistics
        detection_stats = {
            'total': Detection.objects.count(),
            'today': Detection.objects.filter(timestamp__date=today).count(),
            'last_hour': Detection.objects.filter(timestamp__gte=now - timedelta(hours=1)).count(),
            'high_confidence': Detection.objects.filter(confidence__gte=80).count()
        }
        
        # Alert statistics
        alert_stats = {
            'total': Alert.objects.count(),
            'new': Alert.objects.filter(status='new').count(),
            'critical': Alert.objects.filter(severity='critical', status='new').count(),
            'today': Alert.objects.filter(created_at__date=today).count()
        }
        
        # System metrics
        latest_metrics = SystemMetrics.objects.first()
        system_metrics = {
            'cpu_usage': latest_metrics.cpu_usage if latest_metrics else random.uniform(20, 60),
            'memory_usage': latest_metrics.memory_usage if latest_metrics else random.uniform(30, 70),
            'disk_usage': latest_metrics.disk_usage if latest_metrics else random.uniform(40, 60),
            'network_latency': latest_metrics.network_latency if latest_metrics else random.uniform(10, 50),
            'system_uptime': latest_metrics.system_uptime if latest_metrics else random.uniform(100, 500)
        }
        
        # Recent activities
        recent_activities = []
        for activity in DroneActivity.objects.all()[:10]:
            recent_activities.append({
                'description': activity.description,
                'timestamp': activity.timestamp.isoformat(),
                'type': activity.activity_type
            })
        
        return JsonResponse({
            'success': True,
            'drone_stats': drone_stats,
            'detection_stats': detection_stats,
            'alert_stats': alert_stats,
            'system_metrics': system_metrics,
            'recent_activities': recent_activities,
            'threat_level': get_current_threat_level(),
            'system_status': 'operational'
        })
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

def get_current_threat_level():
    """Calculate current threat level based on recent alerts"""
    recent_alerts = Alert.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=1),
        status='new'
    )
    
    if recent_alerts.filter(severity='critical').exists():
        return 'critical'
    elif recent_alerts.filter(severity='high').exists():
        return 'high'
    elif recent_alerts.filter(severity='medium').exists():
        return 'medium'
    else:
        return 'low'
