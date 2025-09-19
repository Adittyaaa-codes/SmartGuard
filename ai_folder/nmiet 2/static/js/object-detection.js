// Advanced Object Detection System
class ObjectDetectionSystem {
    constructor() {
        this.isDetectionActive = false;
        this.detectionMode = 'standard';
        this.sensitivity = 7;
        this.targetClasses = ['person', 'vehicle'];
        this.detectionResults = [];
        this.facialRecognitionEnabled = true;
        this.threatAssessmentEnabled = true;
        this.continuousDetectionActive = false;
        this.continuousInterval = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initDetectionDisplay();
        this.loadDetectionHistory();
    }

    setupEventListeners() {
        // Detection mode selector
        const modeSelector = document.getElementById('detection-mode');
        if (modeSelector) {
            modeSelector.addEventListener('change', (e) => {
                this.detectionMode = e.target.value;
                this.updateDetectionSettings();
            });
        }

        // Sensitivity slider
        const sensitivitySlider = document.getElementById('sensitivity-slider');
        if (sensitivitySlider) {
            sensitivitySlider.addEventListener('input', (e) => {
                this.sensitivity = parseInt(e.target.value);
                this.updateSensitivityDisplay();
            });
        }

        // Target class checkboxes
        const classCheckboxes = document.querySelectorAll('.target-classes input[type="checkbox"]');
        classCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                this.updateTargetClasses();
            });
        });

        // Run detection button
        const runDetectionBtn = document.getElementById('run-detection');
        if (runDetectionBtn) {
            runDetectionBtn.addEventListener('click', () => {
                this.runDetection();
            });
        }

        // Advanced detection buttons
        this.setupAdvancedControls();
    }

    setupAdvancedControls() {
        // Add advanced control buttons
        const controlsContainer = document.querySelector('.detection-controls');
        if (controlsContainer) {
            const advancedControls = document.createElement('div');
            advancedControls.className = 'advanced-controls mt-3';
            advancedControls.innerHTML = `
                <h5>Advanced Features</h5>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="facial-recognition" ${this.facialRecognitionEnabled ? 'checked' : ''}>
                    <label class="form-check-label" for="facial-recognition">Facial Recognition</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="threat-assessment" ${this.threatAssessmentEnabled ? 'checked' : ''}>
                    <label class="form-check-label" for="threat-assessment">Threat Assessment</label>
                </div>
                <div class="btn-group mt-2" role="group">
                    <button type="button" class="btn btn-sm btn-military" id="continuous-detection">
                        <i class="fas fa-play"></i> Continuous
                    </button>
                    <button type="button" class="btn btn-sm btn-military" id="batch-detection">
                        <i class="fas fa-layer-group"></i> Batch Process
                    </button>
                    <button type="button" class="btn btn-sm btn-military" id="export-results">
                        <i class="fas fa-download"></i> Export
                    </button>
                </div>
            `;
            controlsContainer.appendChild(advancedControls);

            // Setup advanced control listeners
            this.setupAdvancedListeners();
        }
    }

    setupAdvancedListeners() {
        // Facial recognition toggle
        const facialCheckbox = document.getElementById('facial-recognition');
        if (facialCheckbox) {
            facialCheckbox.addEventListener('change', (e) => {
                this.facialRecognitionEnabled = e.target.checked;
            });
        }

        // Threat assessment toggle
        const threatCheckbox = document.getElementById('threat-assessment');
        if (threatCheckbox) {
            threatCheckbox.addEventListener('change', (e) => {
                this.threatAssessmentEnabled = e.target.checked;
            });
        }

        // Continuous detection
        const continuousBtn = document.getElementById('continuous-detection');
        if (continuousBtn) {
            continuousBtn.addEventListener('click', () => {
                this.toggleContinuousDetection();
            });
        }

        // Batch detection
        const batchBtn = document.getElementById('batch-detection');
        if (batchBtn) {
            batchBtn.addEventListener('click', () => {
                this.runBatchDetection();
            });
        }

        // Export results
        const exportBtn = document.getElementById('export-results');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => {
                this.exportResults();
            });
        }
    }

    updateDetectionSettings() {
        // Update UI based on detection mode
        const modeDescriptions = {
            'standard': 'Standard object detection with basic classification',
            'enhanced': 'Enhanced detection with weapon and threat identification',
            'thermal': 'Thermal imaging mode for heat signature detection',
            'night': 'Night vision mode with infrared enhancement'
        };

        // Show mode description
        this.showNotification(modeDescriptions[this.detectionMode], 'info');
        
        // Update detection display overlay
        this.updateDetectionOverlay();
    }

    updateDetectionOverlay() {
        const detectionFeed = document.getElementById('detection-feed');
        if (!detectionFeed) return;

        // Remove existing overlays
        const existingOverlay = detectionFeed.querySelector('.detection-overlay');
        if (existingOverlay) {
            existingOverlay.remove();
        }

        // Create new overlay based on mode
        const overlay = document.createElement('div');
        overlay.className = 'detection-overlay';
        
        if (this.detectionMode === 'thermal') {
            overlay.classList.add('thermal-mode');
        } else if (this.detectionMode === 'night') {
            overlay.classList.add('night-mode');
        } else if (this.detectionMode === 'enhanced') {
            overlay.classList.add('enhanced-mode');
        }

        detectionFeed.appendChild(overlay);
    }

    updateSensitivityDisplay() {
        // Show temporary indicator
        this.showNotification(`Detection sensitivity set to ${this.sensitivity}/10`, 'info');
    }

    updateTargetClasses() {
        const checkboxes = document.querySelectorAll('.target-classes input[type="checkbox"]:checked');
        this.targetClasses = Array.from(checkboxes).map(cb => cb.id.replace('class-', ''));
        
        console.log('Target classes updated:', this.targetClasses);
    }

    async runDetection() {
        if (this.isDetectionActive) {
            this.showNotification('Detection already in progress', 'warning');
            return;
        }

        try {
            this.isDetectionActive = true;
            this.showDetectionProgress();
            
            // Prepare detection parameters
            const detectionParams = {
                mode: this.detectionMode,
                sensitivity: this.sensitivity,
                target_classes: this.targetClasses,
                facial_recognition: this.facialRecognitionEnabled,
                threat_assessment: this.threatAssessmentEnabled
            };

            // Call AI detection API
            const response = await fetch('/api/detect-objects/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(detectionParams)
            });

            const data = await response.json();

            if (data.success) {
                this.processDetectionResults(data);
                this.showNotification(`Detection complete: ${data.analysis.total_objects} objects found`, 'success');
            } else {
                this.showNotification(data.error, 'error');
            }

        } catch (error) {
            console.error('Detection error:', error);
            this.showNotification('Detection failed', 'error');
        } finally {
            this.isDetectionActive = false;
            this.hideDetectionProgress();
        }
    }

    showDetectionProgress() {
        const runBtn = document.getElementById('run-detection');
        if (runBtn) {
            runBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            runBtn.disabled = true;
        }

        // Show progress overlay on detection feed
        const detectionFeed = document.getElementById('detection-feed');
        if (detectionFeed) {
            const progressOverlay = document.createElement('div');
            progressOverlay.className = 'detection-progress-overlay';
            progressOverlay.innerHTML = `
                <div class="progress-content">
                    <div class="scanning-line"></div>
                    <div class="progress-text">AI ANALYSIS IN PROGRESS</div>
                    <div class="progress-details">
                        <div>Mode: ${this.detectionMode.toUpperCase()}</div>
                        <div>Sensitivity: ${this.sensitivity}/10</div>
                        <div>Classes: ${this.targetClasses.join(', ')}</div>
                    </div>
                </div>
            `;
            detectionFeed.appendChild(progressOverlay);
        }
    }

    hideDetectionProgress() {
        const runBtn = document.getElementById('run-detection');
        if (runBtn) {
            runBtn.innerHTML = '<i class="fas fa-play"></i> Run Detection';
            runBtn.disabled = false;
        }

        // Remove progress overlay
        const progressOverlay = document.querySelector('.detection-progress-overlay');
        if (progressOverlay) {
            progressOverlay.remove();
        }
    }

    processDetectionResults(data) {
        this.detectionResults = data.detections;
        
        // Update detection display
        this.updateDetectionDisplay(data.detections);
        
        // Update results list
        this.updateResultsList(data.detections);
        
        // Process facial recognition results
        if (data.facial_results && data.facial_results.length > 0) {
            this.processFacialRecognition(data.facial_results);
        }
        
        // Process threat assessments
        if (data.threat_assessments && data.threat_assessments.length > 0) {
            this.processThreatAssessments(data.threat_assessments);
        }
        
        // Handle generated alerts
        if (data.alerts && data.alerts.length > 0) {
            this.processGeneratedAlerts(data.alerts);
        }
        
        // Update analytics
        this.updateDetectionAnalytics(data.analysis);
    }

    updateDetectionDisplay(detections) {
        const detectionFeed = document.getElementById('detection-feed');
        if (!detectionFeed) return;

        // Remove existing detection markers
        const existingMarkers = detectionFeed.querySelectorAll('.detection-marker');
        existingMarkers.forEach(marker => marker.remove());

        // Add detection markers
        detections.forEach((detection, index) => {
            const marker = document.createElement('div');
            marker.className = `detection-marker ${detection.object_type}`;
            marker.style.left = detection.bounding_box.x + 'px';
            marker.style.top = detection.bounding_box.y + 'px';
            marker.style.width = detection.bounding_box.width + 'px';
            marker.style.height = detection.bounding_box.height + 'px';
            
            marker.innerHTML = `
                <div class="marker-label">
                    ${detection.object_type} (${detection.confidence.toFixed(1)}%)
                </div>
            `;
            
            // Add click handler for details
            marker.addEventListener('click', () => {
                this.showDetectionDetails(detection);
            });
            
            detectionFeed.appendChild(marker);
            
            // Animate marker appearance
            setTimeout(() => {
                marker.classList.add('visible');
            }, index * 200);
        });
    }

    updateResultsList(detections) {
        const resultsList = document.getElementById('detection-results');
        if (!resultsList) return;

        resultsList.innerHTML = '';

        detections.forEach(detection => {
            const resultItem = document.createElement('div');
            resultItem.className = 'result-item';
            resultItem.innerHTML = `
                <div class="result-icon ${detection.object_type}"></div>
                <div class="result-details">
                    <div class="result-type">${detection.object_type.charAt(0).toUpperCase() + detection.object_type.slice(1)}</div>
                    <div class="result-confidence">Confidence: ${detection.confidence.toFixed(1)}%</div>
                    <div class="result-timestamp">${new Date(detection.timestamp).toLocaleTimeString()}</div>
                </div>
                <div class="result-actions">
                    <button class="btn btn-sm btn-military" onclick="objectDetection.showDetectionDetails(${JSON.stringify(detection).replace(/"/g, '"')})">
                        <i class="fas fa-info"></i>
                    </button>
                </div>
            `;
            resultsList.appendChild(resultItem);
        });
    }

    showDetectionDetails(detection) {
        const modal = document.createElement('div');
        modal.className = 'detection-details-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h4>Detection Details</h4>
                    <button class="close-btn" onclick="this.parentElement.parentElement.parentElement.remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="detection-info">
                        <div class="info-row">
                            <label>Object Type:</label>
                            <span>${detection.object_type.charAt(0).toUpperCase() + detection.object_type.slice(1)}</span>
                        </div>
                        <div class="info-row">
                            <label>Confidence:</label>
                            <span>${detection.confidence.toFixed(1)}%</span>
                        </div>
                        <div class="info-row">
                            <label>Detection Time:</label>
                            <span>${new Date(detection.timestamp).toLocaleString()}</span>
                        </div>
                        <div class="info-row">
                            <label>Location:</label>
                            <span>Lat: ${detection.location.lat.toFixed(6)}, Lng: ${detection.location.lng.toFixed(6)}</span>
                        </div>
                        <div class="info-row">
                            <label>Detection Mode:</label>
                            <span>${detection.detection_mode.toUpperCase()}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }

    async toggleContinuousDetection() {
        const btn = document.getElementById('continuous-detection');
        if (!btn) return;

        if (this.continuousDetectionActive) {
            // Stop continuous detection
            clearInterval(this.continuousInterval);
            this.continuousDetectionActive = false;
            btn.innerHTML = '<i class="fas fa-play"></i> Continuous';
            btn.classList.remove('active');
            this.showNotification('Continuous detection stopped', 'info');
        } else {
            // Start continuous detection
            this.continuousDetectionActive = true;
            btn.innerHTML = '<i class="fas fa-stop"></i> Stop';
            btn.classList.add('active');
            this.showNotification('Continuous detection started', 'info');
            
            // Run detection every 10 seconds
            this.continuousInterval = setInterval(() => {
                if (!this.isDetectionActive) {
                    this.runDetection();
                }
            }, 10000);
        }
    }

    exportResults() {
        if (this.detectionResults.length === 0) {
            this.showNotification('No detection results to export', 'warning');
            return;
        }
        
        // Prepare export data
        const exportData = {
            timestamp: new Date().toISOString(),
            detection_mode: this.detectionMode,
            sensitivity: this.sensitivity,
            target_classes: this.targetClasses,
            total_detections: this.detectionResults.length,
            results: this.detectionResults
        };
        
        // Create and download JSON file
        const dataStr = JSON.stringify(exportData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `detection_results_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        
        this.showNotification('Detection results exported successfully', 'success');
    }

    async loadDetectionHistory() {
        try {
            const response = await fetch('/api/detections/');
            const data = await response.json();
            
            if (data.success) {
                // Update statistics display
                this.updateDetectionStatistics(data.statistics);
            }
        } catch (error) {
            console.error('Error loading detection history:', error);
        }
    }

    updateDetectionStatistics(stats) {
        // Update various statistics displays
        console.log('Detection Statistics:', stats);
    }

    initDetectionDisplay() {
        // Initialize detection feed with placeholder
        const detectionFeed = document.getElementById('detection-feed');
        if (detectionFeed && !detectionFeed.querySelector('img')) {
            detectionFeed.innerHTML = `
                <div class="detection-placeholder">
                    <i class="fas fa-camera"></i>
                    <p>Click "Run Detection" to analyze current feed</p>
                </div>
            `;
        }
    }

    processFacialRecognition(facialResults) {
        console.log('Facial recognition results:', facialResults);
    }

    processThreatAssessments(threatAssessments) {
        console.log('Threat assessments:', threatAssessments);
    }

    processGeneratedAlerts(alerts) {
        console.log('Generated alerts:', alerts);
    }

    updateDetectionAnalytics(analysis) {
        console.log('Detection analytics:', analysis);
    }

    async runBatchDetection() {
        this.showNotification('Batch detection not implemented yet', 'info');
    }

    showNotification(message, type = 'info') {
        // Use global notification system
        if (typeof showNotification === 'function') {
            showNotification(message, type);
        } else {
            console.log(`${type.toUpperCase()}: ${message}`);
        }
    }
}

// CSS for object detection enhancements
const detectionStyles = `
    .detection-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 5;
    }
    
    .detection-overlay.thermal-mode {
        background: linear-gradient(45deg, rgba(255, 0, 0, 0.1), rgba(255, 255, 0, 0.1));
    }
    
    .detection-overlay.night-mode {
        background: linear-gradient(45deg, rgba(0, 255, 0, 0.1), rgba(0, 0, 255, 0.1));
    }
    
    .detection-overlay.enhanced-mode {
        background: linear-gradient(45deg, rgba(255, 255, 255, 0.05), rgba(0, 255, 255, 0.05));
    }
    
    .detection-progress-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10;
    }
    
    .progress-content {
        text-align: center;
        color: var(--military-highlight);
    }
    
    .scanning-line {
        width: 200px;
        height: 2px;
        background: var(--military-highlight);
        margin: 0 auto 1rem;
        animation: scanProgress 2s linear infinite;
    }
    
    @keyframes scanProgress {
        0% { transform: scaleX(0); }
        50% { transform: scaleX(1); }
        100% { transform: scaleX(0); }
    }
    
    .progress-text {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .progress-details {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .detection-marker {
        position: absolute;
        border: 2px solid var(--military-highlight);
        background: rgba(74, 136, 128, 0.2);
        opacity: 0;
        transition: opacity 0.3s ease;
        cursor: pointer;
    }
    
    .detection-marker.visible {
        opacity: 1;
    }
    
    .detection-marker.person {
        border-color: var(--military-success);
    }
    
    .detection-marker.weapon {
        border-color: var(--military-danger);
        animation: weaponAlert 1s infinite;
    }
    
    .detection-marker.vehicle {
        border-color: var(--military-warning);
    }
    
    @keyframes weaponAlert {
        0%, 100% { box-shadow: 0 0 10px var(--military-danger); }
        50% { box-shadow: 0 0 20px var(--military-danger); }
    }
    
    .marker-label {
        position: absolute;
        top: -25px;
        left: 0;
        background: var(--military-green);
        color: white;
        padding: 2px 6px;
        font-size: 0.7rem;
        border-radius: 3px;
        white-space: nowrap;
    }
    
    .detection-placeholder {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        color: var(--military-text);
        opacity: 0.6;
    }
    
    .detection-placeholder i {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .detection-details-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
    }
    
    .modal-content {
        background: var(--military-green);
        border: 1px solid var(--military-highlight);
        border-radius: 5px;
        max-width: 500px;
        width: 90%;
    }
    
    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        border-bottom: 1px solid var(--military-highlight);
    }
    
    .modal-body {
        padding: 1rem;
    }
    
    .info-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    
    .info-row label {
        font-weight: bold;
        color: var(--military-highlight);
    }
    
    .close-btn {
        background: none;
        border: none;
        color: var(--military-text);
        font-size: 1.2rem;
        cursor: pointer;
    }
    
    .close-btn:hover {
        color: var(--military-highlight);
    }
`;

// Inject styles
const detectionStyleSheet = document.createElement('style');
detectionStyleSheet.textContent = detectionStyles;
document.head.appendChild(detectionStyleSheet);

// Initialize object detection system when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.objectDetection = new ObjectDetectionSystem();
});

// Global function for running object detection (called from main.js)
function runObjectDetection() {
    if (window.objectDetection) {
        window.objectDetection.runDetection();
    }
}
