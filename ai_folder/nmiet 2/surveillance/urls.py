from django.urls import path
from . import views
from . import api
from . import ai_integration

urlpatterns = [
    # Main view
    path('', views.index, name='index'),
    
    # API endpoints
    path('api/drones/', api.drone_list, name='drone_list'),
    path('api/drones/<int:drone_id>/<str:action>/', api.drone_action, name='drone_action'),
    path('api/drone-activities/', api.drone_activities, name='drone_activities'),
    path('api/detections/', api.detection_list, name='detection_list'),
    path('api/alerts/', api.alert_list, name='alert_list'),
    path('api/zones/', api.surveillance_zones, name='surveillance_zones'),
    path('api/simulate-detection/', api.simulate_detection, name='simulate_detection'),
    path('api/dashboard-data/', api.dashboard_data, name='dashboard_data'),
    
    # AI integration endpoints
    path('api/detect-objects/', ai_integration.detect_objects, name='detect_objects'),
]