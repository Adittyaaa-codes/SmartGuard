"""
AI Surveillance and Drone Monitoring System Configuration
--------------------------------------------------------
This file contains the main configuration for the project.
"""

# Project settings
PROJECT_NAME = "AI Surveillance & Drone Monitoring"
VERSION = "1.0.0"

# AI Detection settings
DETECTION_CONFIDENCE_THRESHOLD = 0.6
ENABLE_REAL_TIME_DETECTION = True
DETECTION_INTERVAL = 2  # seconds

# Drone settings
MAX_DRONES = 10
DRONE_BATTERY_WARNING = 20  # percentage
DRONE_SIGNAL_WARNING = 2  # out of 5

# Surveillance zones
DEFAULT_ZONES = [
    {
        'name': 'Perimeter Zone',
        'priority': 1,
        'active': True
    },
    {
        'name': 'Entry Zone',
        'priority': 2,
        'active': True
    },
    {
        'name': 'Restricted Zone',
        'priority': 3,
        'active': True
    }
]

# Alert settings
ALERT_LEVELS = {
    'low': {
        'color': '#3498db',
        'notification': False
    },
    'medium': {
        'color': '#f39c12',
        'notification': True
    },
    'high': {
        'color': '#e74c3c',
        'notification': True
    },
    'critical': {
        'color': '#c0392b',
        'notification': True
    }
}

# System settings
LOG_LEVEL = 'INFO'
ENABLE_ANALYTICS = True