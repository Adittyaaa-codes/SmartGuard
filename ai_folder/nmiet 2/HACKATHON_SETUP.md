# 🚁 AI Surveillance & Drone Monitoring System - Hackathon Setup Guide

## 🎯 Quick Start (5 Minutes Setup)

### Prerequisites
- Python 3.8+ installed
- Git (optional)
- Modern web browser

### 1. Setup Virtual Environment
```bash
# Create virtual environment
python -m venv surveillance_env

# Activate virtual environment
# On Windows:
surveillance_env\Scripts\activate
# On macOS/Linux:
source surveillance_env/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Database
```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 4. Load Demo Data (Optional)
```bash
# Load sample drones and surveillance data
python manage.py shell
```

Then run this in the Django shell:
```python
from ai_surveillance.models import *
from django.contrib.auth.models import User

# Create sample drones
Drone.objects.create(name="Recon-Alpha", drone_type="recon", status="deployed", battery_level=87, signal_strength=4)
Drone.objects.create(name="Patrol-Beta", drone_type="patrol", status="standby", battery_level=100, signal_strength=5)
Drone.objects.create(name="Surv-Delta", drone_type="surveillance", status="scanning", battery_level=65, signal_strength=3)

# Create sample alerts
Alert.objects.create(title="Perimeter Breach", description="Unauthorized access detected", severity="high", status="new")
Alert.objects.create(title="Weapon Detection", description="Potential weapon identified", severity="critical", status="new")

print("Demo data loaded successfully!")
exit()
```

### 5. Run the Server
```bash
python manage.py runserver
```

### 6. Access the System
Open your browser and go to: **http://localhost:8000**

---

## 🎨 Features Showcase

### ✨ Visual Features
- **Military-themed UI** with animated background
- **Real-time particle effects** and matrix-style animations
- **Glitch effects** on hover interactions
- **Pulsing alerts** and scanning animations
- **Responsive design** for all screen sizes

### 🤖 AI Features
- **Object Detection Simulation** with confidence scores
- **Facial Recognition** capabilities
- **Threat Assessment** algorithms
- **Automated Alert System**
- **Pattern Recognition** and behavioral analysis

### 🚁 Drone Management
- **Real-time drone tracking** on interactive map
- **Battery and signal monitoring**
- **Automated patrol routes**
- **Deploy/Recall/Scan operations**
- **Live status updates**

### 📊 Analytics Dashboard
- **Real-time metrics** and system performance
- **Detection frequency charts**
- **Threat level monitoring**
- **Historical data analysis**
- **Export capabilities**

---

## 🏆 Hackathon Demo Script

### 1. System Overview (2 minutes)
- Show the main dashboard with military theme
- Highlight real-time clock and system status
- Demonstrate particle animations and visual effects

### 2. Drone Operations (3 minutes)
- Show drone fleet on the map
- Demonstrate deploy/recall operations
- Show battery levels and signal strength
- Simulate drone movement and patrol

### 3. AI Object Detection (3 minutes)
- Run object detection simulation
- Show confidence scores and object types
- Demonstrate threat assessment
- Show automated alert generation

### 4. Real-time Monitoring (2 minutes)
- Show live alerts and system logs
- Demonstrate critical alert popup
- Show system metrics and analytics
- Highlight real-time updates

---

## 🔧 Customization for Your Hackathon

### Change Theme Colors
Edit `static/css/style.css` and modify the CSS variables:
```css
:root {
    --military-dark: #your-color;
    --military-green: #your-color;
    --military-highlight: #your-color;
}
```

### Add Your Team Logo
Replace the header in `surveillance/templates/surveillance/index.html`:
```html
<h1 class="text-light">
    <i class="fas fa-satellite"></i> YOUR TEAM NAME - SURVEILLANCE SYSTEM
</h1>
```

### Modify Detection Classes
Edit `ai_surveillance/object_detection.py` to add your specific object types:
```python
OBJECT_CLASSES = ['person', 'vehicle', 'weapon', 'your-custom-object']
```

---

## 📱 Mobile Responsive

The system is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Large displays/projectors

---

## 🚀 Production Deployment (Optional)

### For Heroku:
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn surveillance_project.wsgi" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### For Local Network Demo:
```bash
# Run on all interfaces
python manage.py runserver 0.0.0.0:8000
```

Then access from other devices using your computer's IP address.

---

## 🎯 Hackathon Judging Points

### Technical Innovation
- ✅ Real-time AI object detection simulation
- ✅ Advanced drone fleet management
- ✅ Sophisticated threat assessment algorithms
- ✅ Real-time data processing and visualization

### User Experience
- ✅ Intuitive military-themed interface
- ✅ Smooth animations and visual effects
- ✅ Responsive design for all devices
- ✅ Real-time notifications and alerts

### Practical Application
- ✅ Realistic surveillance scenarios
- ✅ Scalable architecture
- ✅ Integration-ready APIs
- ✅ Comprehensive logging and analytics

### Code Quality
- ✅ Clean, well-documented code
- ✅ Modular Django architecture
- ✅ RESTful API design
- ✅ Database optimization

---

## 🆘 Troubleshooting

### Common Issues:

**Port already in use:**
```bash
python manage.py runserver 8001
```

**Database errors:**
```bash
rm surveillance_db.sqlite3
python manage.py migrate
```

**Static files not loading:**
```bash
python manage.py collectstatic
```

**Module not found:**
```bash
pip install -r requirements.txt
```

---

## 📞 Support

If you encounter any issues during the hackathon:
1. Check the console for error messages
2. Ensure all dependencies are installed
3. Verify Python version (3.8+)
4. Check that the virtual environment is activated

---

## 🏅 Good Luck!

Your AI Surveillance System is now ready for the hackathon! The system includes:
- ✅ Professional military-themed UI
- ✅ Real-time animations and effects
- ✅ Comprehensive drone management
- ✅ AI-powered object detection
- ✅ Advanced analytics dashboard
- ✅ Mobile-responsive design

**Remember to highlight the real-time features, AI capabilities, and impressive visual design during your presentation!**

---

*Built with Django, Bootstrap, and lots of hackathon spirit! 🚀*
