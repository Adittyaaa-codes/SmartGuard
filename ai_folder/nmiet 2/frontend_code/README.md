# AI Surveillance & Drone Monitoring Frontend

This is a complete frontend implementation for an AI-powered surveillance and drone monitoring system. The frontend features a military-themed design with advanced animations, real-time updates, and comprehensive functionality.

## Features

### 🎯 Core Functionality
- **Live Surveillance Feed**: Real-time video feed with crosshair and scanning animations
- **Drone Fleet Management**: Control and monitor multiple drones with real-time positioning
- **AI Object Detection**: Advanced object detection with multiple modes (standard, enhanced, thermal, night vision)
- **Analytics Dashboard**: Comprehensive analytics with charts and real-time metrics
- **Alert System**: Real-time alerts and notifications

### 🎨 Design Features
- **Military Theme**: Authentic military-style interface with tactical colors
- **Animated Background**: Matrix-style falling code and radar animations
- **Particle Effects**: Floating particles for enhanced visual appeal
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Theme**: Optimized for low-light surveillance environments

### ⚡ Interactive Elements
- **Real-time Clock**: Digital clock with military precision
- **Status Indicators**: Live system status with animated dots
- **Progress Bars**: Battery levels, signal strength, and system metrics
- **Interactive Maps**: Drone positioning with patrol patterns
- **Chart Animations**: Dynamic charts using Chart.js

## File Structure

```
frontend_code/
├── index.html          # Main HTML file
├── style.css           # Complete CSS with military theme
├── main.js            # Core JavaScript functionality
├── drone-control.js   # Drone management system
├── object-detection.js # AI object detection interface
├── analytics.js       # Analytics and charting system
├── placeholder-feed.jpg # Placeholder image (replace with actual feed)
└── README.md          # This file
```

## Setup Instructions

1. **Copy Files**: Copy all files from this `frontend_code/` folder to your Django project's static files directory.

2. **Update Paths**: If needed, update the paths in `index.html` to match your Django static file configuration.

3. **Add Images**: Replace `placeholder-feed.jpg` with actual surveillance feed images.

4. **Django Integration**: Make sure your Django settings include proper static file serving.

## Dependencies

The frontend uses the following external libraries:
- **Bootstrap 5.3.0**: For responsive layout and components
- **Chart.js**: For analytics charts and visualizations
- **Font Awesome 6.0.0**: For icons and military-themed symbols

All dependencies are loaded via CDN for easy deployment.

## Key Components

### 1. Military Header
- Radar animation background
- Real-time status indicator
- Digital clock with military precision

### 2. Surveillance Feed
- Crosshair targeting system
- Scanning line animation
- Corner brackets for tactical display
- Zoom controls and capture functionality

### 3. Drone Control Panel
- Interactive map with drone positioning
- Real-time battery and signal monitoring
- Patrol route visualization
- Emergency recall functionality

### 4. Object Detection
- Multiple detection modes
- Sensitivity controls
- Target class selection
- Facial recognition and threat assessment
- Detection result visualization

### 5. Analytics Dashboard
- Real-time metrics and KPIs
- Interactive charts (line, doughnut, bar, radar)
- Trend analysis and anomaly detection
- Export functionality

## Customization

### Colors
The design uses CSS custom properties (variables) for easy theming:
```css
:root {
    --military-dark: #0a0e14;
    --military-green: #1a3518;
    --military-highlight: #4a8;
    --military-accent: #8b0000;
    /* ... more variables */
}
```

### Animations
- **Radar Scan**: Continuous rotating radar sweep
- **Matrix Rain**: Falling code effect background
- **Particle Float**: Ambient floating particles
- **Drone Pulse**: Animated drone indicators
- **Scan Lines**: Moving scan effects

### API Integration
The frontend expects the following API endpoints:
- `/api/system-metrics/` - System performance data
- `/api/drone-status/` - Drone fleet status
- `/api/alerts/` - Alert management
- `/api/detect-objects/` - Object detection processing
- `/api/analytics-data/` - Analytics and reporting

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance

- Optimized animations using CSS transforms
- Efficient DOM manipulation
- Lazy loading of heavy components
- Real-time updates with configurable intervals

## Security Features

- No sensitive data stored in frontend
- Secure API communication
- Input validation and sanitization
- XSS protection through proper escaping

## License

This frontend is designed for educational and demonstration purposes in hackathons and surveillance system development.
