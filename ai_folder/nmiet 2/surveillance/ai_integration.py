from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from ai_surveillance.models import (
    Detection, Alert, FacialRecognition, ThreatAssessment, 
    Drone, SurveillanceSession
)
import json
import random
import base64
from datetime import datetime, timedelta

@csrf_exempt
def detect_objects(request):
    """Advanced AI object detection endpoint"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            detection_mode = data.get('mode', 'standard')
            sensitivity = data.get('sensitivity', 7)
            target_classes = data.get('target_classes', ['person', 'vehicle'])
            image_data = data.get('image_data', None)
            
            # Simulate advanced AI processing
            detections = simulate_advanced_detection(detection_mode, sensitivity, target_classes)
            
            # Process facial recognition for person detections
            facial_results = []
            for detection in detections:
                if detection['object_type'] == 'person':
                    facial_result = process_facial_recognition(detection)
                    if facial_result:
                        facial_results.append(facial_result)
            
            # Perform threat assessment
            threat_assessments = []
            for detection in detections:
                threat_assessment = analyze_threat_level(detection)
                if threat_assessment:
                    threat_assessments.append(threat_assessment)
            
            # Generate alerts for high-risk detections
            alerts_generated = []
            for assessment in threat_assessments:
                if assessment['risk_score'] > 70:
                    alert = create_security_alert(assessment)
                    alerts_generated.append(alert)
            
            # Calculate overall analysis
            analysis = {
                'total_objects': len(detections),
                'high_confidence_count': len([d for d in detections if d['confidence'] > 80]),
                'threat_level': calculate_overall_threat(threat_assessments),
                'facial_recognitions': len(facial_results),
                'alerts_generated': len(alerts_generated),
                'processing_time': random.uniform(0.5, 2.0),
                'summary': generate_detection_summary(detections, threat_assessments)
            }
            
            return JsonResponse({
                'success': True,
                'detections': detections,
                'facial_results': facial_results,
                'threat_assessments': threat_assessments,
                'alerts': alerts_generated,
                'analysis': analysis
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

def simulate_advanced_detection(mode, sensitivity, target_classes):
    """Simulate advanced AI object detection based on parameters"""
    detections = []
    
    # Adjust detection probability based on sensitivity
    base_probability = 0.3 + (sensitivity / 10) * 0.4
    
    # Detection types with different probabilities based on mode
    if mode == 'standard':
        detection_pool = {
            'person': 0.4, 'vehicle': 0.3, 'animal': 0.2, 'drone': 0.1
        }
    elif mode == 'enhanced':
        detection_pool = {
            'person': 0.35, 'vehicle': 0.25, 'weapon': 0.15, 'animal': 0.15, 'drone': 0.1
        }
    elif mode == 'thermal':
        detection_pool = {
            'person': 0.5, 'vehicle': 0.3, 'animal': 0.2
        }
    elif mode == 'night':
        detection_pool = {
            'person': 0.3, 'vehicle': 0.4, 'animal': 0.2, 'unknown': 0.1
        }
    else:
        detection_pool = {
            'person': 0.4, 'vehicle': 0.3, 'animal': 0.2, 'unknown': 0.1
        }
    
    # Filter by target classes
    filtered_pool = {k: v for k, v in detection_pool.items() if k in target_classes or k == 'unknown'}
    
    # Generate detections
    num_detections = random.randint(1, 6)
    for i in range(num_detections):
        if random.random() < base_probability:
            object_type = random.choices(
                list(filtered_pool.keys()), 
                weights=list(filtered_pool.values())
            )[0]
            
            # Confidence varies by mode and sensitivity
            base_confidence = 60 + (sensitivity * 3)
            confidence = random.uniform(base_confidence, min(99, base_confidence + 25))
            
            # Enhanced mode provides higher confidence
            if mode == 'enhanced':
                confidence = min(99, confidence + 10)
            
            # Create detection record in database
            detection_record = Detection.objects.create(
                object_type=object_type,
                confidence=confidence,
                location_lat=28.6139 + random.uniform(-0.01, 0.01),
                location_lng=77.2090 + random.uniform(-0.01, 0.01),
                drone=random.choice(Drone.objects.all()) if random.random() > 0.4 else None
            )
            
            detection = {
                'id': detection_record.id,
                'object_type': object_type,
                'confidence': round(confidence, 1),
                'location': {
                    'lat': detection_record.location_lat,
                    'lng': detection_record.location_lng
                },
                'bounding_box': {
                    'x': random.randint(50, 300),
                    'y': random.randint(50, 200),
                    'width': random.randint(80, 150),
                    'height': random.randint(100, 200)
                },
                'timestamp': detection_record.timestamp.isoformat(),
                'detection_mode': mode,
                'features': generate_object_features(object_type)
            }
            
            detections.append(detection)
    
    return detections

def process_facial_recognition(detection):
    """Simulate facial recognition processing"""
    if detection['confidence'] < 70:
        return None
    
    # Simulate facial recognition database lookup
    recognition_confidence = random.uniform(60, 95)
    
    # Simulate different recognition statuses
    statuses = ['identified', 'unknown', 'watchlist', 'vip']
    weights = [0.2, 0.6, 0.15, 0.05]
    status = random.choices(statuses, weights=weights)[0]
    
    # Generate person details based on status
    if status == 'identified':
        names = ['John Smith', 'Sarah Johnson', 'Mike Wilson', 'Lisa Brown', 'David Lee']
        person_name = random.choice(names)
        person_id = f"ID{random.randint(1000, 9999)}"
    elif status == 'watchlist':
        names = ['Unknown Subject A', 'Suspect B', 'Person of Interest C']
        person_name = random.choice(names)
        person_id = f"WL{random.randint(100, 999)}"
    elif status == 'vip':
        names = ['VIP Guest', 'Authorized Personnel', 'Security Chief']
        person_name = random.choice(names)
        person_id = f"VIP{random.randint(10, 99)}"
    else:
        person_name = ''
        person_id = ''
    
    # Create facial recognition record
    detection_obj = Detection.objects.get(id=detection['id'])
    facial_record = FacialRecognition.objects.create(
        detection=detection_obj,
        person_id=person_id,
        name=person_name,
        status=status,
        confidence=recognition_confidence,
        facial_features={
            'age_estimate': random.randint(20, 60),
            'gender': random.choice(['male', 'female']),
            'emotion': random.choice(['neutral', 'alert', 'suspicious', 'calm']),
            'facial_hair': random.choice([True, False]),
            'glasses': random.choice([True, False])
        }
    )
    
    return {
        'id': facial_record.id,
        'detection_id': detection['id'],
        'person_id': person_id,
        'name': person_name,
        'status': status,
        'confidence': round(recognition_confidence, 1),
        'features': facial_record.facial_features,
        'timestamp': facial_record.timestamp.isoformat()
    }

def analyze_threat_level(detection):
    """Analyze threat level for a detection"""
    object_type = detection['object_type']
    confidence = detection['confidence']
    
    # Base risk scores by object type
    risk_scores = {
        'weapon': random.uniform(80, 95),
        'person': random.uniform(20, 60),
        'vehicle': random.uniform(15, 45),
        'drone': random.uniform(40, 70),
        'animal': random.uniform(5, 25),
        'unknown': random.uniform(30, 60)
    }
    
    base_risk = risk_scores.get(object_type, 30)
    
    # Adjust risk based on confidence
    confidence_multiplier = confidence / 100
    final_risk = base_risk * confidence_multiplier
    
    # Add random factors for realism
    final_risk += random.uniform(-10, 10)
    final_risk = max(0, min(100, final_risk))
    
    # Determine threat type and recommended action
    if object_type == 'weapon':
        threat_type = 'weapon'
        recommended_action = "Immediate security response required"
    elif object_type == 'person' and final_risk > 50:
        threat_type = 'suspicious_behavior'
        recommended_action = "Monitor closely and assess behavior"
    elif object_type == 'vehicle' and final_risk > 40:
        threat_type = 'vehicle_anomaly'
        recommended_action = "Verify vehicle authorization"
    elif object_type == 'drone':
        threat_type = 'unauthorized_access'
        recommended_action = "Identify drone operator and intent"
    else:
        threat_type = 'suspicious_behavior'
        recommended_action = "Continue monitoring"
    
    # Create threat assessment record
    detection_obj = Detection.objects.get(id=detection['id'])
    threat_record = ThreatAssessment.objects.create(
        detection=detection_obj,
        threat_type=threat_type,
        risk_score=final_risk,
        description=f"{object_type.title()} detected with {confidence:.1f}% confidence",
        recommended_action=recommended_action,
        automated_response=final_risk > 70
    )
    
    return {
        'id': threat_record.id,
        'detection_id': detection['id'],
        'threat_type': threat_type,
        'risk_score': round(final_risk, 1),
        'description': threat_record.description,
        'recommended_action': recommended_action,
        'automated_response': final_risk > 70,
        'timestamp': threat_record.timestamp.isoformat()
    }

def create_security_alert(threat_assessment):
    """Create security alert for high-risk threats"""
    risk_score = threat_assessment['risk_score']
    threat_type = threat_assessment['threat_type']
    
    # Determine alert severity
    if risk_score >= 90:
        severity = 'critical'
        title = f"CRITICAL THREAT DETECTED"
    elif risk_score >= 70:
        severity = 'high'
        title = f"HIGH-RISK {threat_type.replace('_', ' ').upper()}"
    else:
        severity = 'medium'
        title = f"Security Alert: {threat_type.replace('_', ' ').title()}"
    
    # Create alert record
    alert = Alert.objects.create(
        title=title,
        description=f"{threat_assessment['description']} - Risk Score: {risk_score:.1f}%",
        severity=severity,
        status='new'
    )
    
    return {
        'id': alert.id,
        'title': title,
        'description': alert.description,
        'severity': severity,
        'risk_score': risk_score,
        'timestamp': alert.created_at.isoformat()
    }

def calculate_overall_threat(threat_assessments):
    """Calculate overall threat level from all assessments"""
    if not threat_assessments:
        return 'low'
    
    max_risk = max(assessment['risk_score'] for assessment in threat_assessments)
    avg_risk = sum(assessment['risk_score'] for assessment in threat_assessments) / len(threat_assessments)
    
    if max_risk >= 90 or avg_risk >= 70:
        return 'critical'
    elif max_risk >= 70 or avg_risk >= 50:
        return 'high'
    elif max_risk >= 50 or avg_risk >= 30:
        return 'medium'
    else:
        return 'low'

def generate_detection_summary(detections, threat_assessments):
    """Generate human-readable summary of detection results"""
    if not detections:
        return "No objects detected in current scan."
    
    object_counts = {}
    for detection in detections:
        obj_type = detection['object_type']
        object_counts[obj_type] = object_counts.get(obj_type, 0) + 1
    
    summary_parts = []
    for obj_type, count in object_counts.items():
        if count == 1:
            summary_parts.append(f"1 {obj_type}")
        else:
            summary_parts.append(f"{count} {obj_type}s")
    
    objects_summary = ", ".join(summary_parts)
    
    high_risk_count = len([a for a in threat_assessments if a['risk_score'] > 70])
    
    if high_risk_count > 0:
        return f"Detected {objects_summary}. {high_risk_count} high-risk threat(s) identified."
    else:
        return f"Detected {objects_summary}. No immediate threats identified."

def generate_object_features(object_type):
    """Generate realistic features for detected objects"""
    features = {}
    
    if object_type == 'person':
        features = {
            'height_estimate': random.randint(150, 190),
            'clothing_color': random.choice(['dark', 'light', 'red', 'blue', 'green', 'black']),
            'movement_speed': random.choice(['stationary', 'walking', 'running']),
            'posture': random.choice(['standing', 'sitting', 'crouching', 'lying'])
        }
    elif object_type == 'vehicle':
        features = {
            'vehicle_type': random.choice(['car', 'truck', 'motorcycle', 'van']),
            'color': random.choice(['white', 'black', 'silver', 'red', 'blue']),
            'size': random.choice(['small', 'medium', 'large']),
            'movement': random.choice(['parked', 'moving', 'idling'])
        }
    elif object_type == 'weapon':
        features = {
            'weapon_type': random.choice(['handgun', 'rifle', 'knife', 'unknown']),
            'size': random.choice(['small', 'medium', 'large']),
            'visibility': random.choice(['clearly_visible', 'partially_concealed', 'concealed'])
        }
    elif object_type == 'drone':
        features = {
            'size': random.choice(['small', 'medium', 'large']),
            'altitude': random.randint(10, 100),
            'movement_pattern': random.choice(['hovering', 'circling', 'linear', 'erratic'])
        }
    
    return features

@csrf_exempt
def facial_recognition_search(request):
    """Search facial recognition database"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            search_query = data.get('query', '')
            search_type = data.get('type', 'name')  # name, id, status
            
            # Simulate database search
            results = []
            
            if search_type == 'status':
                # Search by status (watchlist, vip, etc.)
                facial_records = FacialRecognition.objects.filter(status=search_query)[:20]
            elif search_type == 'id':
                # Search by person ID
                facial_records = FacialRecognition.objects.filter(person_id__icontains=search_query)[:20]
            else:
                # Search by name
                facial_records = FacialRecognition.objects.filter(name__icontains=search_query)[:20]
            
            for record in facial_records:
                results.append({
                    'id': record.id,
                    'person_id': record.person_id,
                    'name': record.name,
                    'status': record.status,
                    'confidence': record.confidence,
                    'last_seen': record.timestamp.isoformat(),
                    'detection_location': {
                        'lat': record.detection.location_lat,
                        'lng': record.detection.location_lng
                    } if record.detection.location_lat else None
                })
            
            return JsonResponse({
                'success': True,
                'results': results,
                'total_count': len(results),
                'search_query': search_query,
                'search_type': search_type
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def behavioral_analysis(request):
    """Analyze behavioral patterns from detection history"""
    if request.method == 'GET':
        try:
            # Analyze recent detection patterns
            recent_detections = Detection.objects.filter(
                timestamp__gte=timezone.now() - timedelta(hours=24)
            )
            
            # Pattern analysis
            patterns = {
                'peak_activity_hours': analyze_peak_hours(recent_detections),
                'common_locations': analyze_common_locations(recent_detections),
                'object_frequency': analyze_object_frequency(recent_detections),
                'anomaly_score': calculate_anomaly_score(recent_detections)
            }
            
            # Behavioral insights
            insights = generate_behavioral_insights(patterns)
            
            return JsonResponse({
                'success': True,
                'patterns': patterns,
                'insights': insights,
                'analysis_period': '24 hours',
                'total_detections': recent_detections.count()
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

def analyze_peak_hours(detections):
    """Analyze peak activity hours"""
    hour_counts = {}
    for detection in detections:
        hour = detection.timestamp.hour
        hour_counts[hour] = hour_counts.get(hour, 0) + 1
    
    if not hour_counts:
        return []
    
    # Find top 3 peak hours
    sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
    return [{'hour': hour, 'count': count} for hour, count in sorted_hours[:3]]

def analyze_common_locations(detections):
    """Analyze common detection locations"""
    # Simplified location clustering
    locations = []
    for detection in detections:
        if detection.location_lat and detection.location_lng:
            locations.append({
                'lat': round(detection.location_lat, 4),
                'lng': round(detection.location_lng, 4),
                'count': 1
            })
    
    # Simple clustering by rounding coordinates
    location_counts = {}
    for loc in locations:
        key = f"{loc['lat']},{loc['lng']}"
        if key in location_counts:
            location_counts[key]['count'] += 1
        else:
            location_counts[key] = loc
    
    # Return top 5 locations
    sorted_locations = sorted(location_counts.values(), key=lambda x: x['count'], reverse=True)
    return sorted_locations[:5]

def analyze_object_frequency(detections):
    """Analyze object type frequency"""
    object_counts = {}
    for detection in detections:
        obj_type = detection.object_type
        object_counts[obj_type] = object_counts.get(obj_type, 0) + 1
    
    return [{'type': obj_type, 'count': count} for obj_type, count in object_counts.items()]

def calculate_anomaly_score(detections):
    """Calculate anomaly score based on detection patterns"""
    if not detections:
        return 0
    
    # Simple anomaly calculation based on various factors
    total_detections = len(detections)
    weapon_detections = len([d for d in detections if d.object_type == 'weapon'])
    high_confidence_detections = len([d for d in detections if d.confidence > 90])
    
    # Normalize scores
    weapon_score = (weapon_detections / total_detections) * 100 if total_detections > 0 else 0
    confidence_score = (high_confidence_detections / total_detections) * 50 if total_detections > 0 else 0
    volume_score = min(total_detections / 10, 1) * 30  # Max 30 points for volume
    
    anomaly_score = weapon_score + confidence_score + volume_score
    return min(100, anomaly_score)

def generate_behavioral_insights(patterns):
    """Generate human-readable behavioral insights"""
    insights = []
    
    # Peak hours insights
    if patterns['peak_activity_hours']:
        peak_hour = patterns['peak_activity_hours'][0]['hour']
        insights.append(f"Peak activity occurs around {peak_hour:02d}:00 hours")
    
    # Location insights
    if patterns['common_locations']:
        insights.append(f"Most activity concentrated in {len(patterns['common_locations'])} key areas")
    
    # Object frequency insights
    if patterns['object_frequency']:
        most_common = max(patterns['object_frequency'], key=lambda x: x['count'])
        insights.append(f"Most frequently detected: {most_common['type']} ({most_common['count']} times)")
    
    # Anomaly insights
    anomaly_score = patterns['anomaly_score']
    if anomaly_score > 70:
        insights.append("High anomaly score detected - increased vigilance recommended")
    elif anomaly_score > 40:
        insights.append("Moderate anomaly score - monitor for unusual patterns")
    else:
        insights.append("Normal activity patterns observed")
    
    return insights
