from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class Drone(models.Model):
    """Model for drone information"""
    DRONE_TYPES = (
        ('recon', 'Reconnaissance'),
        ('surveillance', 'Surveillance'),
        ('patrol', 'Patrol'),
    )
    
    STATUS_CHOICES = (
        ('standby', 'Standby'),
        ('deployed', 'Deployed'),
        ('patrolling', 'Patrolling'),
        ('scanning', 'Scanning'),
        ('returning', 'Returning'),
        ('maintenance', 'Maintenance'),
        ('offline', 'Offline'),
    )
    
    name = models.CharField(max_length=100)
    drone_type = models.CharField(max_length=20, choices=DRONE_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='standby')
    battery_level = models.IntegerField(default=100)  # Percentage
    signal_strength = models.IntegerField(default=5)  # 1-5 scale
    last_location_lat = models.FloatField(null=True, blank=True)
    last_location_lng = models.FloatField(null=True, blank=True)
    last_active = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_drone_type_display()})"
    
    def deploy(self):
        """Deploy the drone"""
        self.status = 'deployed'
        self.last_active = timezone.now()
        self.save()
        
        # Create a drone activity log
        DroneActivity.objects.create(
            drone=self,
            activity_type='deploy',
            description=f"{self.name} deployed for mission"
        )
        
        return True
    
    def recall(self):
        """Recall the drone to base"""
        self.status = 'returning'
        self.save()
        
        # Create a drone activity log
        DroneActivity.objects.create(
            drone=self,
            activity_type='recall',
            description=f"{self.name} recalled to base"
        )
        
        return True
    
    def scan_area(self):
        """Perform area scan with the drone"""
        self.status = 'scanning'
        self.save()
        
        # Create a drone activity log
        DroneActivity.objects.create(
            drone=self,
            activity_type='scan',
            description=f"{self.name} performing area scan"
        )
        
        return True
    
    def update_battery(self, level):
        """Update drone battery level"""
        self.battery_level = level
        self.save()
        
        # Log if battery is low
        if level < 20:
            DroneActivity.objects.create(
                drone=self,
                activity_type='warning',
                description=f"{self.name} battery level critical: {level}%"
            )
        
        return True


class DroneActivity(models.Model):
    """Model for tracking drone activities"""
    ACTIVITY_TYPES = (
        ('deploy', 'Deployment'),
        ('recall', 'Recall'),
        ('scan', 'Area Scan'),
        ('detection', 'Object Detection'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('status', 'Status Change'),
    )
    
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Drone Activities'
    
    def __str__(self):
        return f"{self.drone.name} - {self.get_activity_type_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class Detection(models.Model):
    """Model for object detection results"""
    OBJECT_TYPES = (
        ('person', 'Person'),
        ('vehicle', 'Vehicle'),
        ('weapon', 'Weapon'),
        ('animal', 'Animal'),
        ('drone', 'Drone'),
        ('unknown', 'Unknown'),
    )
    
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, related_name='detections', null=True, blank=True)
    object_type = models.CharField(max_length=20, choices=OBJECT_TYPES)
    confidence = models.FloatField()  # Detection confidence (0-100)
    location_lat = models.FloatField(null=True, blank=True)
    location_lng = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='detections/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_object_type_display()} - {self.confidence}% - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class SurveillanceZone(models.Model):
    """Model for defining surveillance zones"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    coordinates = models.TextField()  # JSON string of polygon coordinates
    priority = models.IntegerField(default=0)  # Higher number = higher priority
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Alert(models.Model):
    """Model for security alerts"""
    SEVERITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )
    
    STATUS_CHOICES = (
        ('new', 'New'),
        ('acknowledged', 'Acknowledged'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('false_alarm', 'False Alarm'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new')
    zone = models.ForeignKey(SurveillanceZone, on_delete=models.SET_NULL, null=True, blank=True)
    detection = models.ForeignKey(Detection, on_delete=models.SET_NULL, null=True, blank=True)
    acknowledged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_severity_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class SurveillanceSession(models.Model):
    """Model to track surveillance sessions"""
    SESSION_STATUS = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('error', 'Error'),
    ]
    
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=SESSION_STATUS, default='active')
    location = models.CharField(max_length=200, blank=True)
    operator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    notes = models.TextField(blank=True)
    total_detections = models.IntegerField(default=0)
    threat_level = models.CharField(max_length=20, default='low')
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class FacialRecognition(models.Model):
    """Model for facial recognition results"""
    RECOGNITION_STATUS = [
        ('identified', 'Identified'),
        ('unknown', 'Unknown'),
        ('watchlist', 'On Watchlist'),
        ('vip', 'VIP'),
    ]
    
    detection = models.OneToOneField(Detection, on_delete=models.CASCADE, related_name='facial_recognition')
    person_id = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=RECOGNITION_STATUS, default='unknown')
    confidence = models.FloatField(default=0.0)
    facial_features = models.JSONField(default=dict)  # Store facial feature vectors
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Face Recognition - {self.name or 'Unknown'} - {self.confidence}%"


class ThreatAssessment(models.Model):
    """Model for AI threat assessment"""
    THREAT_TYPES = [
        ('weapon', 'Weapon Detection'),
        ('suspicious_behavior', 'Suspicious Behavior'),
        ('unauthorized_access', 'Unauthorized Access'),
        ('crowd_formation', 'Crowd Formation'),
        ('vehicle_anomaly', 'Vehicle Anomaly'),
    ]
    
    detection = models.ForeignKey(Detection, on_delete=models.CASCADE, related_name='threat_assessments')
    threat_type = models.CharField(max_length=30, choices=THREAT_TYPES)
    risk_score = models.FloatField()  # 0-100 scale
    description = models.TextField()
    recommended_action = models.TextField()
    automated_response = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-risk_score', '-timestamp']
    
    def __str__(self):
        return f"{self.get_threat_type_display()} - Risk: {self.risk_score}%"


class SystemMetrics(models.Model):
    """Model for system performance metrics"""
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_usage = models.FloatField(default=0.0)
    memory_usage = models.FloatField(default=0.0)
    disk_usage = models.FloatField(default=0.0)
    network_latency = models.FloatField(default=0.0)
    active_drones = models.IntegerField(default=0)
    detections_per_hour = models.IntegerField(default=0)
    system_uptime = models.FloatField(default=0.0)  # Hours
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"System Metrics - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class PatrolRoute(models.Model):
    """Model for drone patrol routes"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    waypoints = models.JSONField()  # List of lat/lng coordinates
    estimated_duration = models.IntegerField()  # Minutes
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    assigned_drone = models.ForeignKey(Drone, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Route: {self.name}"


class WeatherCondition(models.Model):
    """Model for weather conditions affecting surveillance"""
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()  # Celsius
    humidity = models.FloatField()  # Percentage
    wind_speed = models.FloatField()  # km/h
    visibility = models.FloatField()  # km
    weather_condition = models.CharField(max_length=50)  # Clear, Cloudy, Rain, etc.
    impact_on_surveillance = models.CharField(max_length=20, choices=[
        ('optimal', 'Optimal'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ], default='optimal')
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Weather - {self.weather_condition} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
