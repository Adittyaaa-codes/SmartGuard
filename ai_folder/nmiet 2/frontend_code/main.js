// Enhanced Main JavaScript for AI Surveillance System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initClock();
    initFeedControls();
    initAlertLog();
    initParticleSystem();
    initRealTimeUpdates();
    initNotificationSystem();
    simulateSystemActivity();
    
    // Initialize enhanced animations
    initEnhancedAnimations();
    
    // Initialize API connections
    initAPIConnections();
});

// Create floating particles for enhanced background
function initParticleSystem() {
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles';
    document.body.appendChild(particlesContainer);
    
    // Create 50 particles
    for (let i = 0; i < 50; i++) {
        createParticle(particlesContainer);
    }
    
    // Continuously create new particles
    setInterval(() => {
        if (particlesContainer.children.length < 50) {
            createParticle(particlesContainer);
        }
    }, 2000);
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    // Random starting position
    particle.style.left = Math.random() * 100 + '%';
    particle.style.animationDelay = Math.random() * 15 + 's';
    
    container.appendChild(particle);
    
    // Remove particle after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
        }
    }, 25000);
}

// Enhanced animations for military theme
function initEnhancedAnimations() {
    // Add glitch effect to headers
    const headers = document.querySelectorAll('h1, h2, h3');
    headers.forEach(header => {
        header.addEventListener('mouseenter', function() {
            this.style.animation = 'glitch 0.3s ease-in-out';
            setTimeout(() => {
                this.style.animation = '';
            }, 300);
        });
    });
    
    // Add pulse effect to buttons
    const buttons = document.querySelectorAll('.btn-military');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.style.animation = 'buttonPulse 0.3s ease-in-out';
            setTimeout(() => {
                this.style.animation = '';
            }, 300);
        });
    });
    
    // Add scanning line to cards
    const cards = document.querySelectorAll('.military-card');
    cards.forEach(card => {
        const scanLine = document.createElement('div');
        scanLine.className = 'card-scan-line';
        card.appendChild(scanLine);
    });
}

// Real-time updates system
function initRealTimeUpdates() {
    // Update system metrics every 5 seconds
    setInterval(updateSystemMetrics, 5000);
    
    // Update drone status every 10 seconds
    setInterval(updateDroneStatus, 10000);
    
    // Check for new alerts every 3 seconds
    setInterval(checkForAlerts, 3000);
    
    // Update analytics charts every 30 seconds
    setInterval(updateAnalyticsCharts, 30000);
}

// API connections for real-time data
function initAPIConnections() {
    // Initial data load
    loadDashboardData();
    loadDroneData();
    loadAlertData();
}

async function updateSystemMetrics() {
    try {
        const response = await fetch('/api/system-metrics/');
        const data = await response.json();
        
        if (data.success) {
            updateMetricsDisplay(data.metrics);
        }
    } catch (error) {
        console.error('Error updating system metrics:', error);
    }
}

async function updateDroneStatus() {
    try {
        const response = await fetch('/api/drone-status/');
        const data = await response.json();
        
        if (data.success) {
            updateDroneDisplay(data.drones);
            updateDroneCount(data.active_count, data.total_count);
        }
    } catch (error) {
        console.error('Error updating drone status:', error);
    }
}

async function checkForAlerts() {
    try {
        const response = await fetch('/api/alerts/');
        const data = await response.json();
        
        if (data.success) {
            updateAlertsDisplay(data.alerts);
            
            // Check for new critical alerts
            const criticalAlerts = data.alerts.filter(alert => 
                alert.severity === 'critical' && alert.status === 'new'
            );
            
            criticalAlerts.forEach(alert => {
                showCriticalAlert(alert);
            });
        }
    } catch (error) {
        console.error('Error checking alerts:', error);
    }
}

function updateMetricsDisplay(metrics) {
    // Update threat level
    const threatElement = document.querySelector('.status-value.low, .status-value.medium, .status-value.high, .status-value.critical');
    if (threatElement) {
        threatElement.className = `status-value ${metrics.threat_level}`;
        threatElement.textContent = metrics.threat_level.charAt(0).toUpperCase() + metrics.threat_level.slice(1);
    }
    
    // Update system uptime
    const uptimeElement = document.querySelector('#system-uptime');
    if (uptimeElement) {
        uptimeElement.textContent = `${metrics.system_uptime.toFixed(1)}h`;
    }
    
    // Update detection count
    const detectionElement = document.querySelector('#detections-count');
    if (detectionElement) {
        detectionElement.textContent = metrics.detections_per_hour;
    }
}

function updateDroneDisplay(drones) {
    drones.forEach(drone => {
        const droneElement = document.querySelector(`[data-drone-id="${drone.id}"]`);
        if (droneElement) {
            // Update drone position (simulate movement)
            if (drone.status === 'patrolling') {
                const currentLeft = parseFloat(droneElement.style.left) || 20;
                const currentTop = parseFloat(droneElement.style.top) || 30;
                
                // Small random movement
                const newLeft = Math.max(10, Math.min(90, currentLeft + (Math.random() - 0.5) * 10));
                const newTop = Math.max(10, Math.min(90, currentTop + (Math.random() - 0.5) * 10));
                
                droneElement.style.left = newLeft + '%';
                droneElement.style.top = newTop + '%';
            }
            
            // Update drone status indicator
            droneElement.className = `drone drone-${drone.id} status-${drone.status}`;
        }
    });
}

function updateDroneCount(active, total) {
    const droneCountElement = document.getElementById('active-drones-count');
    if (droneCountElement) {
        droneCountElement.textContent = `${active}/${total}`;
    }
}

function updateAlertsDisplay(alerts) {
    const alertContainer = document.getElementById('alert-log-entries');
    if (!alertContainer) return;
    
    // Clear existing alerts
    alertContainer.innerHTML = '';
    
    // Add new alerts (limit to 10)
    alerts.slice(0, 10).forEach(alert => {
        const alertElement = document.createElement('div');
        alertElement.className = `log-entry ${alert.severity}`;
        
        const time = new Date(alert.created_at).toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit'
        });
        
        alertElement.innerHTML = `
            <span class="log-time">${time}</span>
            <span class="log-message">${alert.title}</span>
        `;
        
        alertContainer.appendChild(alertElement);
    });
}

function showCriticalAlert(alert) {
    // Create critical alert overlay
    const overlay = document.createElement('div');
    overlay.className = 'critical-alert-overlay';
    overlay.innerHTML = `
        <div class="critical-alert">
            <div class="alert-header">
                <i class="fas fa-exclamation-triangle"></i>
                CRITICAL ALERT
            </div>
            <div class="alert-content">
                <h3>${alert.title}</h3>
                <p>${alert.description}</p>
                <div class="alert-actions">
                    <button class="btn btn-military" onclick="acknowledgeAlert(${alert.id})">
                        <i class="fas fa-check"></i> Acknowledge
                    </button>
                    <button class="btn btn-military" onclick="dismissAlert()">
                        <i class="fas fa-times"></i> Dismiss
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    // Auto-dismiss after 10 seconds
    setTimeout(() => {
        if (overlay.parentNode) {
            overlay.parentNode.removeChild(overlay);
        }
    }, 10000);
}

async function acknowledgeAlert(alertId) {
    try {
        const response = await fetch('/api/alerts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                alert_id: alertId,
                action: 'acknowledge'
            })
        });
        
        const data = await response.json();
        if (data.success) {
            showNotification('Alert acknowledged', 'success');
            dismissAlert();
        }
    } catch (error) {
        console.error('Error acknowledging alert:', error);
        showNotification('Failed to acknowledge alert', 'error');
    }
}

function dismissAlert() {
    const overlay = document.querySelector('.critical-alert-overlay');
    if (overlay) {
        overlay.parentNode.removeChild(overlay);
    }
}

// Enhanced notification system
function initNotificationSystem() {
    // Create notification container
    const container = document.createElement('div');
    container.className = 'notification-container';
    container.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        max-width: 400px;
    `;
    document.body.appendChild(container);
}

// Load initial dashboard data
async function loadDashboardData() {
    try {
        const response = await fetch('/api/dashboard-data/');
        const data = await response.json();
        
        // Update dashboard with initial data
        updateDashboardStats(data);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

async function loadDroneData() {
    try {
        const response = await fetch('/api/drones/');
        const data = await response.json();
        
        if (data.drones) {
            updateDroneDisplay(data.drones);
        }
    } catch (error) {
        console.error('Error loading drone data:', error);
    }
}

async function loadAlertData() {
    try {
        const response = await fetch('/api/alerts/');
        const data = await response.json();
        
        if (data.alerts) {
            updateAlertsDisplay(data.alerts);
        }
    } catch (error) {
        console.error('Error loading alert data:', error);
    }
}

function updateDashboardStats(data) {
    // Update various dashboard statistics
    if (data.drone_status) {
        const activeCount = Object.values(data.drone_status).reduce((a, b) => a + b, 0);
        updateDroneCount(data.drone_status.deployed + data.drone_status.patrolling, activeCount);
    }
    
    if (data.total_detections) {
        const detectionElement = document.querySelector('#total-detections');
        if (detectionElement) {
            detectionElement.textContent = data.total_detections;
        }
    }
}

// Add CSS for new animations
const additionalStyles = `
    @keyframes glitch {
        0% { transform: translate(0); }
        20% { transform: translate(-2px, 2px); }
        40% { transform: translate(-2px, -2px); }
        60% { transform: translate(2px, 2px); }
        80% { transform: translate(2px, -2px); }
        100% { transform: translate(0); }
    }
    
    @keyframes buttonPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .card-scan-line {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--military-highlight), transparent);
        animation: cardScan 3s linear infinite;
        opacity: 0.7;
    }
    
    @keyframes cardScan {
        0% { transform: translateY(0); opacity: 0; }
        50% { opacity: 0.7; }
        100% { transform: translateY(300px); opacity: 0; }
    }
    
    .critical-alert-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease-in-out;
    }
    
    .critical-alert {
        background: var(--military-green);
        border: 2px solid var(--military-danger);
        border-radius: 10px;
        padding: 2rem;
        max-width: 500px;
        text-align: center;
        animation: alertPulse 1s ease-in-out infinite;
    }
    
    .alert-header {
        color: var(--military-danger);
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }
    
    .alert-actions {
        margin-top: 1.5rem;
        display: flex;
        gap: 1rem;
        justify-content: center;
    }
    
    @keyframes alertPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(217, 83, 79, 0.5); }
        50% { box-shadow: 0 0 40px rgba(217, 83, 79, 0.8); }
    }
    
    .status-patrolling .drone-icon {
        animation: droneMove 2s ease-in-out infinite;
    }
    
    @keyframes droneMove {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(5deg); }
        75% { transform: rotate(-5deg); }
    }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// Digital Clock
function initClock() {
    function updateClock() {
        const now = new Date();
        document.getElementById('hours').textContent = String(now.getHours()).padStart(2, '0');
        document.getElementById('minutes').textContent = String(now.getMinutes()).padStart(2, '0');
        document.getElementById('seconds').textContent = String(now.getSeconds()).padStart(2, '0');
    }
    
    // Update clock immediately and then every second
    updateClock();
    setInterval(updateClock, 1000);
}

// Feed Controls
function initFeedControls() {
    const toggleFeedBtn = document.getElementById('toggle-feed');
    const captureBtn = document.getElementById('capture-image');
    const detectBtn = document.getElementById('detect-objects');
    const zoomInBtn = document.getElementById('zoom-in');
    const zoomOutBtn = document.getElementById('zoom-out');
    
    let feedActive = false;
    let zoomLevel = 1;
    
    // Toggle feed button
    if (toggleFeedBtn) {
        toggleFeedBtn.addEventListener('click', function() {
            feedActive = !feedActive;
            if (feedActive) {
                this.innerHTML = '<i class="fas fa-stop"></i> Stop Feed';
                this.classList.add('active');
                // Simulate live feed by changing the opacity of the feed
                document.querySelector('.live-feed').classList.add('active');
            } else {
                this.innerHTML = '<i class="fas fa-play"></i> Start Feed';
                this.classList.remove('active');
                document.querySelector('.live-feed').classList.remove('active');
            }
        });
    }
    
    // Capture image button
    if (captureBtn) {
        captureBtn.addEventListener('click', function() {
            if (!feedActive) {
                showNotification('Feed must be active to capture images', 'warning');
                return;
            }
            
            // Simulate capture with flash effect
            const feed = document.querySelector('.live-feed');
            feed.classList.add('capturing');
            
            setTimeout(() => {
                feed.classList.remove('capturing');
                showNotification('Image captured successfully', 'success');
                
                // Add to log
                addLogEntry('Image captured from surveillance feed');
            }, 300);
        });
    }
    
    // Detect objects button
    if (detectBtn) {
        detectBtn.addEventListener('click', function() {
            if (!feedActive) {
                showNotification('Feed must be active to detect objects', 'warning');
                return;
            }
            
            showNotification('Running object detection...', 'info');
            
            // Simulate processing delay
            setTimeout(() => {
                // Redirect to detection section
                document.getElementById('detection-section').scrollIntoView({ behavior: 'smooth' });
                
                // Add to log
                addLogEntry('Object detection initiated on current feed');
                
                // Trigger the detection process in the detection.js file
                if (typeof runObjectDetection === 'function') {
                    runObjectDetection();
                }
            }, 1000);
        });
    }
    
    // Zoom controls
    if (zoomInBtn) {
        zoomInBtn.addEventListener('click', function() {
            if (zoomLevel < 3) {
                zoomLevel += 0.25;
                updateZoom();
            }
        });
    }
    
    if (zoomOutBtn) {
        zoomOutBtn.addEventListener('click', function() {
            if (zoomLevel > 1) {
                zoomLevel -= 0.25;
                updateZoom();
            }
        });
    }
    
    function updateZoom() {
        const feedContent = document.getElementById('surveillance-feed');
        if (feedContent) {
            feedContent.style.transform = `scale(${zoomLevel})`;
            showNotification(`Zoom level: ${Math.round(zoomLevel * 100)}%`, 'info');
        }
    }
}

// Alert Log
function initAlertLog() {
    // Initial log entries are already in HTML
    // This function will be used to add new entries
}

// Add log entry
function addLogEntry(message, type = '') {
    const logEntries = document.getElementById('alert-log-entries');
    if (!logEntries) return;
    
    const now = new Date();
    const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    
    const entry = document.createElement('div');
    entry.className = 'log-entry' + (type ? ` ${type}` : '');
    
    entry.innerHTML = `
        <span class="log-time">${timeStr}</span>
        <span class="log-message">${message}</span>
    `;
    
    // Add new entry at the top
    logEntries.insertBefore(entry, logEntries.firstChild);
    
    // Limit to 10 entries
    if (logEntries.children.length > 10) {
        logEntries.removeChild(logEntries.lastChild);
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element if it doesn't exist
    let notificationContainer = document.querySelector('.notification-container');
    
    if (!notificationContainer) {
        notificationContainer = document.createElement('div');
        notificationContainer.className = 'notification-container';
        document.body.appendChild(notificationContainer);
    }
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${getIconForType(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Add to container
    notificationContainer.appendChild(notification);
    
    // Remove after delay
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
    
    function getIconForType(type) {
        switch(type) {
            case 'success': return 'fa-check-circle';
            case 'warning': return 'fa-exclamation-triangle';
            case 'error': return 'fa-times-circle';
            case 'info':
            default: return 'fa-info-circle';
        }
    }
}

// Simulate system activity
function simulateSystemActivity() {
    const activities = [
        'Perimeter scan completed - All clear',
        'Drone battery level check - All optimal',
        'System diagnostics completed successfully',
        'Automatic calibration of sensors completed',
        'Weather conditions updated - Visibility optimal',
        'Network connectivity check - All systems online',
        'Scheduled system backup completed',
        'Unidentified movement detected - Sector 3',
        'Suspicious activity flagged - Reviewing footage',
        'Object of interest tracked - ID #4872'
    ];
    
    const activityTypes = ['', '', '', '', '', '', '', 'warning', 'warning', 'warning'];
    
    // Add random activity every 20-40 seconds
    setInterval(() => {
        const index = Math.floor(Math.random() * activities.length);
        addLogEntry(activities[index], activityTypes[index]);
        
        // Update threat level occasionally
        if (Math.random() < 0.3) {
            updateThreatLevel();
        }
        
        // Update drone count occasionally
        if (Math.random() < 0.2) {
            updateDroneCount();
        }
    }, Math.random() * 20000 + 20000);
}

// Update threat level
function updateThreatLevel() {
    const threatLevelElement = document.querySelector('.status-item .status-value:nth-child(2)');
    if (!threatLevelElement) return;
    
    const levels = [
        { text: 'Low', class: 'low' },
        { text: 'Medium', class: 'medium' },
        { text: 'High', class: 'high' }
    ];
    
    // Weighted random selection (more likely to be low)
    const weights = [0.7, 0.2, 0.1];
    const random = Math.random();
    let index = 0;
    
    let sum = weights[0];
    while (random > sum && index < weights.length - 1) {
        index++;
        sum += weights[index];
    }
    
    const selected = levels[index];
    
    // Remove all classes and add the new one
    threatLevelElement.className = 'status-value ' + selected.class;
    threatLevelElement.textContent = selected.text;
    
    // Log if changed to medium or high
    if (selected.class !== 'low') {
        addLogEntry(`Threat level changed to ${selected.text}`, selected.class === 'high' ? 'warning' : '');
    }
}

// Update drone count
function updateDroneCount() {
    const droneCountElement = document.getElementById('active-drones-count');
    if (!droneCountElement) return;
    
    const currentCount = droneCountElement.textContent.split('/')[0];
    let newCount = Math.floor(Math.random() * 6); // 0-5 drones
    
    // Ensure some change
    while (newCount === parseInt(currentCount)) {
        newCount = Math.floor(Math.random() * 6);
    }
    
    droneCountElement.textContent = `${newCount}/5`;
    
    // Log if drones were deployed or recalled
    if (newCount > parseInt(currentCount)) {
        addLogEntry(`Drone #${newCount} deployed for patrol`);
    } else if (newCount < parseInt(currentCount)) {
        addLogEntry(`Drone #${parseInt(currentCount)} recalled to base`);
    }
}
