# AI Surveillance and Drone Monitoring System

A comprehensive military-themed surveillance system with drone monitoring and AI-powered object detection capabilities.

## Features

- Real-time surveillance feed monitoring
- Drone fleet management and control
- AI-powered object detection
- Military-themed UI with animations
- Alert management system
- Analytics dashboard

## Project Structure

```
nmiet 2/
├── ai_surveillance/
│   ├── __init__.py
│   ├── models.py           # Database models for drones, detections, etc.
│   └── object_detection.py # AI object detection functionality
├── static/
│   ├── css/
│   │   └── style.css       # Military-themed styles and animations
│   ├── images/
│   │   ├── detections/     # Detected object images
│   │   └── drones/         # Drone images
│   └── js/
│       ├── main.js         # Main JavaScript functionality
│       ├── drone-control.js # Drone control functionality
│       ├── object-detection.js # Object detection functionality
│       └── analytics.js    # Analytics functionality
├── surveillance/
│   ├── __init__.py
│   ├── api.py              # API endpoints for the system
│   ├── ai_integration.py   # AI integration with the API
│   ├── templates/
│   │   └── surveillance/
│   │       └── index.html  # Main dashboard template
│   ├── urls.py             # URL configuration
│   └── views.py            # View functions
└── project_config.py       # Project configuration
```

## Setup Instructions

1. Ensure you have Django installed
2. Copy all files to your Django project
3. Add 'ai_surveillance' and 'surveillance' to your INSTALLED_APPS in settings.py
4. Add the URLs to your main urls.py file
5. Run migrations: `python manage.py makemigrations` and `python manage.py migrate`
6. Start the server: `python manage.py runserver`

## Technologies Used

- Django (Backend)
- HTML, CSS, JavaScript (Frontend)
- Bootstrap (UI Framework)
- Custom CSS animations for military theme

## Credits

Created for AI-powered surveillance and drone monitoring hackathon project.