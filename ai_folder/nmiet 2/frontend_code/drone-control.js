// Enhanced Drone Control System
class DroneController {
    constructor() {
        this.selectedDroneId = 1;
        this.drones = new Map();
        this.isRealTimeActive = false;
        this.updateInterval = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadDroneData();
        this.startRealTimeUpdates();
        this.initDroneMap();
    }

    setupEventListeners() {
        // Drone selector
        const droneSelector = document.getElementById('drone-selector');
        if (droneSelector) {
            droneSelector.addEventListener('change', (e) => {
                this.selectedDroneId = parseInt(e.target.value);
                this.updateSelectedDroneInfo();
            });
        }

        // Control buttons
        const deployBtn = document.getElementById('deploy-drone');
        const recallBtn = document.getElementById('recall-drone');
        const scanBtn = document.getElementById('scan-area');

        if (deployBtn) {
            deployBtn.addEventListener('click', () => this.deployDrone());
        }
        if (recallBtn) {
            recallBtn.addEventListener('click', () => this.recallDrone());
        }
        if (scanBtn) {
            scanBtn.addEventListener('click', () => this.scanArea());
        }

        // Drone map interactions
        this.setupMapInteractions();
    }

    setupMapInteractions() {
        const droneElements = document.querySelectorAll('.drone');
        droneElements.forEach(drone => {
            drone.addEventListener('click', (e) => {
                const droneId = parseInt(e.currentTarget.dataset.droneId);
                this.selectDrone(droneId);
            });

            // Add hover effects
            drone.addEventListener('mouseenter', (e) => {
                this.showDroneTooltip(e.currentTarget);
            });

            drone.addEventListener('mouseleave', (e) => {
                this.hideDroneTooltip();
            });
        });
    }

    async loadDroneData() {
        try {
            const response = await fetch('/api/drones/');
            const data = await response.json();
            
            if (data.success) {
                this.updateDroneData(data.drones);
                this.updateDroneSelector(data.drones);
                this.updateDroneMap(data.drones);
            }
        } catch (error) {
            console.error('Error loading drone data:', error);
            this.showNotification('Failed to load drone data', 'error');
        }
    }

    updateDroneData(drones) {
        drones.forEach(drone => {
            this.drones.set(drone.id, drone);
        });
    }

    updateDroneSelector(drones) {
        const selector = document.getElementById('drone-selector');
        if (!selector) return;

        selector.innerHTML = '';
        drones.forEach(drone => {
            const option = document.createElement('option');
            option.value = drone.id;
            option.textContent = `${drone.name} - ${drone.type} (${drone.status})`;
            selector.appendChild(option);
        });
    }

    updateDroneMap(drones) {
        drones.forEach(drone => {
            const droneElement = document.querySelector(`[data-drone-id="${drone.id}"]`);
            if (droneElement) {
                // Update position if drone is moving
                if (drone.status === 'patrolling' || drone.status === 'scanning') {
                    this.animateDroneMovement(droneElement, drone);
                }

                // Update status class
                droneElement.className = `drone drone-${drone.id} status-${drone.status}`;
                
                // Update drone icon color based on status
                const droneIcon = droneElement.querySelector('.drone-icon');
                if (droneIcon) {
                    this.updateDroneIconStatus(droneIcon, drone.status, drone.battery_level);
                }
            }
        });
    }

    updateDroneIconStatus(iconElement, status, batteryLevel) {
        // Remove existing status classes
        iconElement.classList.remove('status-deployed', 'status-patrolling', 'status-scanning', 'status-standby', 'status-low-battery');
        
        // Add current status class
        iconElement.classList.add(`status-${status}`);
        
        // Add low battery warning
        if (batteryLevel < 20) {
            iconElement.classList.add('status-low-battery');
        }
    }

    animateDroneMovement(droneElement, droneData) {
        // Simulate realistic drone movement patterns
        const currentLeft = parseFloat(droneElement.style.left) || 20;
        const currentTop = parseFloat(droneElement.style.top) || 30;
        
        let newLeft, newTop;
        
        if (droneData.status === 'patrolling') {
            // Patrol pattern - move in a circuit
            const time = Date.now() / 1000;
            const patrolRadius = 15;
            const centerX = 50;
            const centerY = 50;
            
            newLeft = centerX + Math.cos(time * 0.1 + droneData.id) * patrolRadius;
            newTop = centerY + Math.sin(time * 0.1 + droneData.id) * patrolRadius;
        } else if (droneData.status === 'scanning') {
            // Scanning pattern - systematic grid movement
            const scanSpeed = 0.5;
            newLeft = currentLeft + (Math.random() - 0.5) * scanSpeed;
            newTop = currentTop + (Math.random() - 0.5) * scanSpeed;
        } else {
            // Small random movement for other statuses
            newLeft = currentLeft + (Math.random() - 0.5) * 2;
            newTop = currentTop + (Math.random() - 0.5) * 2;
        }
        
        // Keep within bounds
        newLeft = Math.max(5, Math.min(95, newLeft));
        newTop = Math.max(5, Math.min(95, newTop));
        
        // Smooth animation
        droneElement.style.transition = 'left 2s ease-in-out, top 2s ease-in-out';
        droneElement.style.left = newLeft + '%';
        droneElement.style.top = newTop + '%';
    }

    selectDrone(droneId) {
        this.selectedDroneId = droneId;
        
        // Update selector
        const selector = document.getElementById('drone-selector');
        if (selector) {
            selector.value = droneId;
        }
        
        // Update drone info
        this.updateSelectedDroneInfo();
        
        // Highlight selected drone on map
        this.highlightSelectedDrone(droneId);
    }

    highlightSelectedDrone(droneId) {
        // Remove previous highlights
        document.querySelectorAll('.drone').forEach(drone => {
            drone.classList.remove('selected');
        });
        
        // Add highlight to selected drone
        const selectedDrone = document.querySelector(`[data-drone-id="${droneId}"]`);
        if (selectedDrone) {
            selectedDrone.classList.add('selected');
        }
    }

    updateSelectedDroneInfo() {
        const drone = this.drones.get(this.selectedDroneId);
        if (!drone) return;

        // Update battery display
        const batteryProgress = document.querySelector('.progress-bar');
        if (batteryProgress) {
            batteryProgress.style.width = drone.battery_level + '%';
            batteryProgress.textContent = drone.battery_level + '%';
            
            // Update battery color based on level
            batteryProgress.classList.remove('bg-success', 'bg-warning', 'bg-danger');
            if (drone.battery_level > 50) {
                batteryProgress.classList.add('bg-success');
            } else if (drone.battery_level > 20) {
                batteryProgress.classList.add('bg-warning');
            } else {
                batteryProgress.classList.add('bg-danger');
            }
        }

        // Update signal strength
        const signalBars = document.querySelectorAll('.signal-strength .bar');
        signalBars.forEach((bar, index) => {
            if (index < drone.signal_strength) {
                bar.classList.add('active');
            } else {
                bar.classList.remove('active');
            }
        });

        // Update status
        const statusElement = document.querySelector('.drone-status .status-value:last-child');
        if (statusElement) {
            statusElement.textContent = drone.status.charAt(0).toUpperCase() + drone.status.slice(1);
            statusElement.className = `status-value ${this.getStatusClass(drone.status)}`;
        }
    }

    getStatusClass(status) {
        const statusClasses = {
            'deployed': 'operational',
            'patrolling': 'operational',
            'scanning': 'operational',
            'standby': 'low',
            'returning': 'medium',
            'maintenance': 'warning',
            'offline': 'danger'
        };
        return statusClasses[status] || 'low';
    }

    async deployDrone() {
        try {
            this.showNotification('Deploying drone...', 'info');
            
            const response = await fetch(`/api/drones/${this.selectedDroneId}/deploy/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showNotification(data.message, 'success');
                this.loadDroneData(); // Refresh data
                this.logDroneActivity('deploy', data.message);
            } else {
                this.showNotification(data.error, 'error');
            }
        } catch (error) {
            console.error('Error deploying drone:', error);
            this.showNotification('Failed to deploy drone', 'error');
        }
    }

    async recallDrone() {
        try {
            this.showNotification('Recalling drone...', 'info');
            
            const response = await fetch(`/api/drones/${this.selectedDroneId}/recall/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showNotification(data.message, 'success');
                this.loadDroneData(); // Refresh data
                this.logDroneActivity('recall', data.message);
            } else {
                this.showNotification(data.error, 'error');
            }
        } catch (error) {
            console.error('Error recalling drone:', error);
            this.showNotification('Failed to recall drone', 'error');
        }
    }

    async scanArea() {
        try {
            this.showNotification('Initiating area scan...', 'info');
            
            const response = await fetch(`/api/drones/${this.selectedDroneId}/scan/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showNotification(data.message, 'success');
                this.loadDroneData(); // Refresh data
                this.logDroneActivity('scan', data.message);
                
                // Simulate scan results after delay
                setTimeout(() => {
                    this.simulateScanResults();
                }, 3000);
            } else {
                this.showNotification(data.error, 'error');
            }
        } catch (error) {
            console.error('Error scanning area:', error);
            this.showNotification('Failed to initiate scan', 'error');
        }
    }

    async simulateScanResults() {
        try {
            const response = await fetch('/api/simulate-detection/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                const detectionCount = data.detections.length;
                this.showNotification(`Scan complete: ${detectionCount} objects detected`, 'success');
                
                // Update detection display if available
                if (typeof updateDetectionResults === 'function') {
                    updateDetectionResults(data.detections);
                }
            }
        } catch (error) {
            console.error('Error getting scan results:', error);
        }
    }

    logDroneActivity(action, message) {
        // Add to activity log
        if (typeof addLogEntry === 'function') {
            addLogEntry(message);
        }
    }

    showDroneTooltip(droneElement) {
        const droneId = parseInt(droneElement.dataset.droneId);
        const drone = this.drones.get(droneId);
        
        if (!drone) return;
        
        // Create tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'drone-tooltip';
        tooltip.innerHTML = `
            <div class="tooltip-header">${drone.name}</div>
            <div class="tooltip-content">
                <div>Status: ${drone.status}</div>
                <div>Battery: ${drone.battery_level}%</div>
                <div>Signal: ${drone.signal_strength}/5</div>
            </div>
        `;
        
        // Position tooltip
        const rect = droneElement.getBoundingClientRect();
        tooltip.style.position = 'absolute';
        tooltip.style.left = (rect.left + rect.width / 2) + 'px';
        tooltip.style.top = (rect.top - 10) + 'px';
        tooltip.style.transform = 'translateX(-50%) translateY(-100%)';
        
        document.body.appendChild(tooltip);
        
        // Store reference for cleanup
        this.currentTooltip = tooltip;
    }

    hideDroneTooltip() {
        if (this.currentTooltip) {
            this.currentTooltip.remove();
            this.currentTooltip = null;
        }
    }

    startRealTimeUpdates() {
        if (this.isRealTimeActive) return;
        
        this.isRealTimeActive = true;
        this.updateInterval = setInterval(() => {
            this.loadDroneData();
        }, 5000); // Update every 5 seconds
    }

    stopRealTimeUpdates() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
        this.isRealTimeActive = false;
    }

    initDroneMap() {
        // Add grid overlay for better visualization
        const mapContainer = document.getElementById('drone-map-container');
        if (mapContainer) {
            this.addMapOverlay(mapContainer);
        }
    }

    addMapOverlay(container) {
        // Add coordinate system
        const overlay = document.createElement('div');
        overlay.className = 'map-overlay';
        overlay.innerHTML = `
            <div class="coordinate-system">
                <div class="axis-labels">
                    <div class="x-axis">
                        <span>0</span><span>25</span><span>50</span><span>75</span><span>100</span>
                    </div>
                    <div class="y-axis">
                        <span>0</span><span>25</span><span>50</span><span>75</span><span>100</span>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(overlay);
    }

    showNotification(message, type = 'info') {
        // Use the global notification system
        if (typeof showNotification === 'function') {
            showNotification(message, type);
        } else {
            console.log(`${type.toUpperCase()}: ${message}`);
        }
    }

    // Advanced drone control methods
    async setPatrolRoute(routePoints) {
        try {
            const response = await fetch(`/api/drones/${this.selectedDroneId}/set-route/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    route_points: routePoints
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showNotification('Patrol route set successfully', 'success');
            } else {
                this.showNotification(data.error, 'error');
            }
        } catch (error) {
            console.error('Error setting patrol route:', error);
            this.showNotification('Failed to set patrol route', 'error');
        }
    }

    async emergencyRecallAll() {
        try {
            this.showNotification('Emergency recall initiated...', 'warning');
            
            const activeDrones = Array.from(this.drones.values()).filter(
                drone => ['deployed', 'patrolling', 'scanning'].includes(drone.status)
            );
            
            const recallPromises = activeDrones.map(drone => 
                fetch(`/api/drones/${drone.id}/recall/`, { method: 'POST' })
            );
            
            await Promise.all(recallPromises);
            
            this.showNotification(`Emergency recall complete: ${activeDrones.length} drones recalled`, 'success');
            this.loadDroneData();
        } catch (error) {
            console.error('Error during emergency recall:', error);
            this.showNotification('Emergency recall failed', 'error');
        }
    }

    getDroneStatistics() {
        const stats = {
            total: this.drones.size,
            active: 0,
            standby: 0,
            maintenance: 0,
            offline: 0,
            averageBattery: 0
        };
        
        let totalBattery = 0;
        
        this.drones.forEach(drone => {
            if (['deployed', 'patrolling', 'scanning'].includes(drone.status)) {
                stats.active++;
            } else if (drone.status === 'standby') {
                stats.standby++;
            } else if (drone.status === 'maintenance') {
                stats.maintenance++;
            } else if (drone.status === 'offline') {
                stats.offline++;
            }
            
            totalBattery += drone.battery_level;
        });
        
        stats.averageBattery = this.drones.size > 0 ? totalBattery / this.drones.size : 0;
        
        return stats;
    }
}

// CSS for drone control enhancements
const droneControlStyles = `
    .drone.selected {
        box-shadow: 0 0 20px var(--military-highlight);
        z-index: 10;
    }
    
    .drone-tooltip {
        background: var(--military-green);
        border: 1px solid var(--military-highlight);
        border-radius: 5px;
        padding: 0.5rem;
        font-size: 0.8rem;
        z-index: 1000;
        pointer-events: none;
    }
    
    .tooltip-header {
        font-weight: bold;
        color: var(--military-highlight);
        margin-bottom: 0.25rem;
    }
    
    .tooltip-content div {
        margin-bottom: 0.1rem;
    }
    
    .status-deployed .drone-icon {
        background-color: var(--military-success);
    }
    
    .status-patrolling .drone-icon {
        background-color: var(--military-highlight);
        animation: patrol-pulse 2s infinite;
    }
    
    .status-scanning .drone-icon {
        background-color: var(--military-warning);
        animation: scan-rotate 3s linear infinite;
    }
    
    .status-standby .drone-icon {
        background-color: var(--military-text);
        opacity: 0.6;
    }
    
    .status-low-battery .drone-icon {
        animation: battery-warning 1s infinite;
    }
    
    @keyframes patrol-pulse {
        0%, 100% { transform: scale(1) rotate(180deg); }
        50% { transform: scale(1.1) rotate(180deg); }
    }
    
    @keyframes scan-rotate {
        0% { transform: rotate(180deg); }
        100% { transform: rotate(540deg); }
    }
    
    @keyframes battery-warning {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    .map-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }
    
    .coordinate-system .x-axis {
        position: absolute;
        bottom: 5px;
        left: 0;
        right: 0;
        display: flex;
        justify-content: space-between;
        font-size: 0.7rem;
        color: var(--military-text);
        opacity: 0.5;
    }
    
    .coordinate-system .y-axis {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 5px;
        display: flex;
        flex-direction: column-reverse;
        justify-content: space-between;
        font-size: 0.7rem;
        color: var(--military-text);
        opacity: 0.5;
    }
`;

// Inject styles
const droneStyleSheet = document.createElement('style');
droneStyleSheet.textContent = droneControlStyles;
document.head.appendChild(droneStyleSheet);

// Initialize drone controller when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.droneController = new DroneController();
});
