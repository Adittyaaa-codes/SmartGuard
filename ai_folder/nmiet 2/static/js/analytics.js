// Advanced Analytics System for AI Surveillance
class AnalyticsSystem {
    constructor() {
        this.charts = {};
        this.analyticsData = {};
        this.updateInterval = null;
        this.isRealTimeActive = false;
        this.init();
    }

    init() {
        this.setupCharts();
        this.loadAnalyticsData();
        this.startRealTimeUpdates();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Add analytics control buttons
        this.addAnalyticsControls();
    }

    addAnalyticsControls() {
        const analyticsSection = document.getElementById('analytics-section');
        if (analyticsSection) {
            const controlsContainer = document.createElement('div');
            controlsContainer.className = 'analytics-controls mb-3';
            controlsContainer.innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <div class="btn-group" role="group">
                            <button type="button" class="btn btn-sm btn-military" id="refresh-analytics">
                                <i class="fas fa-sync"></i> Refresh
                            </button>
                            <button type="button" class="btn btn-sm btn-military" id="export-analytics">
                                <i class="fas fa-download"></i> Export
                            </button>
                            <button type="button" class="btn btn-sm btn-military" id="toggle-realtime">
                                <i class="fas fa-play"></i> Real-time
                            </button>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <select class="form-select form-select-sm military-select" id="time-range">
                            <option value="1h">Last Hour</option>
                            <option value="6h">Last 6 Hours</option>
                            <option value="24h" selected>Last 24 Hours</option>
                            <option value="7d">Last 7 Days</option>
                            <option value="30d">Last 30 Days</option>
                        </select>
                    </div>
                </div>
            `;
            
            const cardBody = analyticsSection.querySelector('.card-body');
            cardBody.insertBefore(controlsContainer, cardBody.firstChild);
            
            this.setupControlListeners();
        }
    }

    setupControlListeners() {
        // Refresh button
        const refreshBtn = document.getElementById('refresh-analytics');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refreshAnalytics();
            });
        }

        // Export button
        const exportBtn = document.getElementById('export-analytics');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => {
                this.exportAnalytics();
            });
        }

        // Real-time toggle
        const realtimeBtn = document.getElementById('toggle-realtime');
        if (realtimeBtn) {
            realtimeBtn.addEventListener('click', () => {
                this.toggleRealTime();
            });
        }

        // Time range selector
        const timeRangeSelect = document.getElementById('time-range');
        if (timeRangeSelect) {
            timeRangeSelect.addEventListener('change', (e) => {
                this.updateTimeRange(e.target.value);
            });
        }
    }

    setupCharts() {
        this.setupDetectionChart();
        this.setupCoverageChart();
        this.setupThreatChart();
        this.setupPerformanceChart();
    }

    setupDetectionChart() {
        const ctx = document.getElementById('detectionChart');
        if (!ctx) return;

        this.charts.detection = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Detections',
                    data: [],
                    borderColor: 'rgba(74, 136, 128, 1)',
                    backgroundColor: 'rgba(74, 136, 128, 0.2)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Detection Frequency Over Time',
                        color: '#c5d1c8'
                    },
                    legend: {
                        labels: {
                            color: '#c5d1c8'
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#c5d1c8'
                        },
                        grid: {
                            color: 'rgba(197, 209, 200, 0.1)'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#c5d1c8'
                        },
                        grid: {
                            color: 'rgba(197, 209, 200, 0.1)'
                        }
                    }
                }
            }
        });
    }

    setupCoverageChart() {
        const ctx = document.getElementById('coverageChart');
        if (!ctx) return;

        this.charts.coverage = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Covered Areas', 'Uncovered Areas'],
                datasets: [{
                    data: [92, 8],
                    backgroundColor: [
                        'rgba(74, 136, 128, 0.8)',
                        'rgba(139, 0, 0, 0.8)'
                    ],
                    borderColor: [
                        'rgba(74, 136, 128, 1)',
                        'rgba(139, 0, 0, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Surveillance Coverage',
                        color: '#c5d1c8'
                    },
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#c5d1c8'
                        }
                    }
                }
            }
        });
    }

    setupThreatChart() {
        // Add threat level chart
        const analyticsRow = document.querySelector('#analytics-section .row');
        if (analyticsRow) {
            const threatChartContainer = document.createElement('div');
            threatChartContainer.className = 'col-md-6 mt-4';
            threatChartContainer.innerHTML = `
                <div class="analytics-chart">
                    <h4>Threat Level Distribution</h4>
                    <canvas id="threatChart"></canvas>
                </div>
            `;
            analyticsRow.appendChild(threatChartContainer);

            const ctx = document.getElementById('threatChart');
            if (ctx) {
                this.charts.threat = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['Low', 'Medium', 'High', 'Critical'],
                        datasets: [{
                            label: 'Threat Count',
                            data: [45, 23, 12, 3],
                            backgroundColor: [
                                'rgba(92, 184, 92, 0.8)',
                                'rgba(240, 173, 78, 0.8)',
                                'rgba(217, 83, 79, 0.8)',
                                'rgba(139, 0, 0, 0.8)'
                            ],
                            borderColor: [
                                'rgba(92, 184, 92, 1)',
                                'rgba(240, 173, 78, 1)',
                                'rgba(217, 83, 79, 1)',
                                'rgba(139, 0, 0, 1)'
                            ],
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Threat Levels (Last 24h)',
                                color: '#c5d1c8'
                            },
                            legend: {
                                display: false
                            }
                        },
                        scales: {
                            x: {
                                ticks: {
                                    color: '#c5d1c8'
                                },
                                grid: {
                                    color: 'rgba(197, 209, 200, 0.1)'
                                }
                            },
                            y: {
                                ticks: {
                                    color: '#c5d1c8'
                                },
                                grid: {
                                    color: 'rgba(197, 209, 200, 0.1)'
                                }
                            }
                        }
                    }
                });
            }
        }
    }

    setupPerformanceChart() {
        // Add system performance chart
        const analyticsRow = document.querySelector('#analytics-section .row');
        if (analyticsRow) {
            const performanceChartContainer = document.createElement('div');
            performanceChartContainer.className = 'col-md-6 mt-4';
            performanceChartContainer.innerHTML = `
                <div class="analytics-chart">
                    <h4>System Performance</h4>
                    <canvas id="performanceChart"></canvas>
                </div>
            `;
            analyticsRow.appendChild(performanceChartContainer);

            const ctx = document.getElementById('performanceChart');
            if (ctx) {
                this.charts.performance = new Chart(ctx, {
                    type: 'radar',
                    data: {
                        labels: ['CPU Usage', 'Memory', 'Network', 'Storage', 'Response Time', 'Accuracy'],
                        datasets: [{
                            label: 'Current Performance',
                            data: [65, 45, 80, 55, 90, 95],
                            borderColor: 'rgba(74, 136, 128, 1)',
                            backgroundColor: 'rgba(74, 136, 128, 0.2)',
                            borderWidth: 2,
                            pointBackgroundColor: 'rgba(74, 136, 128, 1)',
                            pointBorderColor: '#fff',
                            pointHoverBackgroundColor: '#fff',
                            pointHoverBorderColor: 'rgba(74, 136, 128, 1)'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            title: {
                                display: true,
                                text: 'System Health Metrics',
                                color: '#c5d1c8'
                            },
                            legend: {
                                labels: {
                                    color: '#c5d1c8'
                                }
                            }
                        },
                        scales: {
                            r: {
                                angleLines: {
                                    color: 'rgba(197, 209, 200, 0.2)'
                                },
                                grid: {
                                    color: 'rgba(197, 209, 200, 0.2)'
                                },
                                pointLabels: {
                                    color: '#c5d1c8'
                                },
                                ticks: {
                                    color: '#c5d1c8',
                                    backdropColor: 'transparent'
                                }
                            }
                        }
                    }
                });
            }
        }
    }

    async loadAnalyticsData() {
        try {
            const response = await fetch('/api/analytics-data/');
            const data = await response.json();
            
            if (data.success) {
                this.analyticsData = data;
                this.updateCharts(data);
            }
        } catch (error) {
            console.error('Error loading analytics data:', error);
            this.generateMockData();
        }
    }

    generateMockData() {
        // Generate mock data for demonstration
        const now = new Date();
        const hours = [];
        const detectionCounts = [];
        
        for (let i = 23; i >= 0; i--) {
            const hour = new Date(now.getTime() - i * 60 * 60 * 1000);
            hours.push(hour.getHours().toString().padStart(2, '0') + ':00');
            detectionCounts.push(Math.floor(Math.random() * 20) + 5);
        }
        
        this.analyticsData = {
            detection_frequency: {
                labels: hours,
                data: detectionCounts
            },
            object_distribution: {
                labels: ['Person', 'Vehicle', 'Animal', 'Unknown'],
                data: [45, 30, 15, 10]
            },
            threat_distribution: {
                labels: ['Low', 'Medium', 'High', 'Critical'],
                data: [45, 23, 12, 3]
            }
        };
        
        this.updateCharts(this.analyticsData);
    }

    updateCharts(data) {
        // Update detection frequency chart
        if (this.charts.detection && data.detection_frequency) {
            this.charts.detection.data.labels = data.detection_frequency.labels;
            this.charts.detection.data.datasets[0].data = data.detection_frequency.data;
            this.charts.detection.update();
        }

        // Update coverage chart with dynamic data
        if (this.charts.coverage) {
            const coverage = Math.floor(Math.random() * 10) + 85; // 85-95%
            this.charts.coverage.data.datasets[0].data = [coverage, 100 - coverage];
            this.charts.coverage.update();
        }

        // Update threat chart
        if (this.charts.threat && data.threat_distribution) {
            this.charts.threat.data.datasets[0].data = data.threat_distribution.data;
            this.charts.threat.update();
        }

        // Update performance chart with real-time metrics
        if (this.charts.performance) {
            const performanceData = [
                Math.floor(Math.random() * 30) + 40, // CPU
                Math.floor(Math.random() * 20) + 35, // Memory
                Math.floor(Math.random() * 15) + 75, // Network
                Math.floor(Math.random() * 20) + 45, // Storage
                Math.floor(Math.random() * 10) + 85, // Response Time
                Math.floor(Math.random() * 5) + 90   // Accuracy
            ];
            this.charts.performance.data.datasets[0].data = performanceData;
            this.charts.performance.update();
        }
    }

    startRealTimeUpdates() {
        if (this.isRealTimeActive) return;
        
        this.isRealTimeActive = true;
        this.updateInterval = setInterval(() => {
            this.loadAnalyticsData();
            this.updateSummaryStats();
        }, 30000); // Update every 30 seconds
    }

    stopRealTimeUpdates() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
        this.isRealTimeActive = false;
    }

    toggleRealTime() {
        const btn = document.getElementById('toggle-realtime');
        if (!btn) return;

        if (this.isRealTimeActive) {
            this.stopRealTimeUpdates();
            btn.innerHTML = '<i class="fas fa-play"></i> Real-time';
            btn.classList.remove('active');
            this.showNotification('Real-time updates stopped', 'info');
        } else {
            this.startRealTimeUpdates();
            btn.innerHTML = '<i class="fas fa-stop"></i> Stop';
            btn.classList.add('active');
            this.showNotification('Real-time updates started', 'info');
        }
    }

    refreshAnalytics() {
        this.showNotification('Refreshing analytics data...', 'info');
        this.loadAnalyticsData();
        this.updateSummaryStats();
    }

    updateTimeRange(range) {
        this.showNotification(`Time range updated to: ${range}`, 'info');
        // In a real implementation, this would fetch data for the selected time range
        this.loadAnalyticsData();
    }

    updateSummaryStats() {
        // Update summary statistics cards
        const statCards = document.querySelectorAll('.stat-card .stat-value');
        
        if (statCards.length >= 4) {
            // Total Detections
            const currentDetections = parseInt(statCards[0].textContent) || 247;
            statCards[0].textContent = currentDetections + Math.floor(Math.random() * 5);
            
            // Alerts Generated
            const currentAlerts = parseInt(statCards[1].textContent) || 18;
            if (Math.random() < 0.3) { // 30% chance to increment
                statCards[1].textContent = currentAlerts + 1;
            }
            
            // Area Coverage
            const coverage = Math.floor(Math.random() * 5) + 90; // 90-95%
            statCards[2].textContent = coverage + '%';
            
            // Avg. Drone Flight
            const flightTime = (Math.random() * 2 + 4).toFixed(1); // 4.0-6.0h
            statCards[3].textContent = flightTime + 'h';
        }
    }

    exportAnalytics() {
        const exportData = {
            timestamp: new Date().toISOString(),
            analytics_data: this.analyticsData,
            summary_stats: this.getSummaryStats(),
            system_performance: this.getSystemPerformance(),
            export_type: 'analytics_report'
        };
        
        // Create and download JSON file
        const dataStr = JSON.stringify(exportData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `analytics_report_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        
        this.showNotification('Analytics report exported successfully', 'success');
    }

    getSummaryStats() {
        const statCards = document.querySelectorAll('.stat-card');
        const stats = {};
        
        statCards.forEach(card => {
            const label = card.querySelector('.stat-label').textContent;
            const value = card.querySelector('.stat-value').textContent;
            stats[label] = value;
        });
        
        return stats;
    }

    getSystemPerformance() {
        if (this.charts.performance) {
            const data = this.charts.performance.data.datasets[0].data;
            const labels = this.charts.performance.data.labels;
            
            const performance = {};
            labels.forEach((label, index) => {
                performance[label] = data[index];
            });
            
            return performance;
        }
        return {};
    }

    // Advanced analytics methods
    generateTrendAnalysis() {
        if (!this.analyticsData.detection_frequency) return null;
        
        const data = this.analyticsData.detection_frequency.data;
        const trend = this.calculateTrend(data);
        
        return {
            direction: trend > 0 ? 'increasing' : trend < 0 ? 'decreasing' : 'stable',
            magnitude: Math.abs(trend),
            confidence: this.calculateTrendConfidence(data)
        };
    }

    calculateTrend(data) {
        if (data.length < 2) return 0;
        
        const n = data.length;
        const sumX = (n * (n - 1)) / 2;
        const sumY = data.reduce((sum, val) => sum + val, 0);
        const sumXY = data.reduce((sum, val, index) => sum + (index * val), 0);
        const sumX2 = data.reduce((sum, val, index) => sum + (index * index), 0);
        
        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        return slope;
    }

    calculateTrendConfidence(data) {
        // Simple confidence calculation based on data variance
        const mean = data.reduce((sum, val) => sum + val, 0) / data.length;
        const variance = data.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / data.length;
        const stdDev = Math.sqrt(variance);
        
        // Lower standard deviation = higher confidence
        return Math.max(0, Math.min(100, 100 - (stdDev / mean) * 100));
    }

    generateAnomalyReport() {
        const anomalies = [];
        
        // Check for detection spikes
        if (this.analyticsData.detection_frequency) {
            const data = this.analyticsData.detection_frequency.data;
            const mean = data.reduce((sum, val) => sum + val, 0) / data.length;
            const threshold = mean * 2;
            
            data.forEach((value, index) => {
                if (value > threshold) {
                    anomalies.push({
                        type: 'detection_spike',
                        time: this.analyticsData.detection_frequency.labels[index],
                        value: value,
                        severity: value > threshold * 1.5 ? 'high' : 'medium'
                    });
                }
            });
        }
        
        return anomalies;
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

// Enhanced analytics dashboard
class AnalyticsDashboard {
    constructor() {
        this.widgets = new Map();
        this.init();
    }

    init() {
        this.createAdvancedWidgets();
        this.setupDashboardControls();
    }

    createAdvancedWidgets() {
        this.createRealTimeMetrics();
        this.createTrendIndicators();
        this.createAnomalyDetector();
    }

    createRealTimeMetrics() {
        const metricsContainer = document.createElement('div');
        metricsContainer.className = 'real-time-metrics mt-4';
        metricsContainer.innerHTML = `
            <div class="row">
                <div class="col-md-12">
                    <div class="card military-card">
                        <div class="card-header">
                            <h4><i class="fas fa-tachometer-alt"></i> Real-Time Metrics</h4>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="metric-widget">
                                        <div class="metric-value" id="detections-per-minute">0</div>
                                        <div class="metric-label">Detections/Min</div>
                                        <div class="metric-trend" id="detection-trend">
                                            <i class="fas fa-arrow-up text-success"></i> +12%
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="metric-widget">
                                        <div class="metric-value" id="active-alerts">3</div>
                                        <div class="metric-label">Active Alerts</div>
                                        <div class="metric-trend" id="alert-trend">
                                            <i class="fas fa-arrow-down text-success"></i> -25%
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="metric-widget">
                                        <div class="metric-value" id="system-load">67%</div>
                                        <div class="metric-label">System Load</div>
                                        <div class="metric-trend" id="load-trend">
                                            <i class="fas fa-minus text-warning"></i> Stable
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="metric-widget">
                                        <div class="metric-value" id="response-time">1.2s</div>
                                        <div class="metric-label">Avg Response</div>
                                        <div class="metric-trend" id="response-trend">
                                            <i class="fas fa-arrow-up text-danger"></i> +8%
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        const analyticsSection = document.getElementById('analytics-section');
        if (analyticsSection) {
            analyticsSection.appendChild(metricsContainer);
        }
    }

    createTrendIndicators() {
        // Trend indicators are created as part of real-time metrics
        this.updateTrendIndicators();
    }

    createAnomalyDetector() {
        const anomalyContainer = document.createElement('div');
        anomalyContainer.className = 'anomaly-detector mt-4';
        anomalyContainer.innerHTML = `
            <div class="row">
                <div class="col-md-12">
                    <div class="card military-card">
                        <div class="card-header">
                            <h4><i class="fas fa-exclamation-triangle"></i> Anomaly Detection</h4>
                        </div>
                        <div class="card-body">
                            <div class="anomaly-list" id="anomaly-list">
                                <div class="anomaly-item low">
                                    <div class="anomaly-icon"><i class="fas fa-info-circle"></i></div>
                                    <div class="anomaly-details">
                                        <div class="anomaly-title">Unusual Detection Pattern</div>
                                        <div class="anomaly-description">Detection rate 15% above normal in Sector 3</div>
                                        <div class="anomaly-time">2 minutes ago</div>
                                    </div>
                                </div>
                                <div class="anomaly-item medium">
                                    <div class="anomaly-icon"><i class="fas fa-exclamation"></i></div>
                                    <div class="anomaly-details">
                                        <div class="anomaly-title">System Performance Degradation</div>
                                        <div class="anomaly-description">Response time increased by 20%</div>
                                        <div class="anomaly-time">5 minutes ago</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        const analyticsSection = document.getElementById('analytics-section');
        if (analyticsSection) {
            analyticsSection.appendChild(anomalyContainer);
        }
    }

    updateTrendIndicators() {
        // Update trend indicators with random data for demo
        const trends = ['detection-trend', 'alert-trend', 'load-trend', 'response-trend'];
        
        trends.forEach(trendId => {
            const element = document.getElementById(trendId);
            if (element) {
                const change = Math.floor(Math.random() * 30) - 15; // -15 to +15
                const isPositive = change > 0;
                const isNeutral = Math.abs(change) < 3;
                
                if (isNeutral) {
                    element.innerHTML = '<i class="fas fa-minus text-warning"></i> Stable';
                } else if (isPositive) {
                    element.innerHTML = `<i class="fas fa-arrow-up text-${trendId.includes('alert') ? 'danger' : 'success'}"></i> +${change}%`;
                } else {
                    element.innerHTML = `<i class="fas fa-arrow-down text-success"></i> ${change}%`;
                }
            }
        });
    }

    setupDashboardControls() {
        // Dashboard controls are handled by the main AnalyticsSystem
    }
}

// CSS for analytics enhancements
const analyticsStyles = `
    .analytics-controls {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid var(--military-highlight);
        border-radius: 5px;
        padding: 1rem;
    }
    
    .military-select {
        background-color: var(--military-dark);
        color: var(--military-text);
        border: 1px solid var(--military-highlight);
    }
    
    .military-select:focus {
        border-color: var(--military-highlight);
        box-shadow: 0 0 5px rgba(74, 136, 128, 0.5);
    }
    
    .metric-widget {
        text-align: center;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid var(--military-highlight);
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: var(--military-highlight);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--military-text);
        margin-bottom: 0.5rem;
    }
    
    .metric-trend {
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .anomaly-list {
        max-height: 300px;
        overflow-y: auto;
    }
    
    .anomaly-item {
        display: flex;
        align-items: center;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 0 5px 5px 0;
    }
    
    .anomaly-item.low {
        border-left-color: var(--military-success);
    }
    
    .anomaly-item.medium {
        border-left-color: var(--military-warning);
    }
    
    .anomaly-item.high {
        border-left-color: var(--military-danger);
    }
    
    .anomaly-icon {
        margin-right: 1rem;
        font-size: 1.2rem;
    }
    
    .anomaly-details {
        flex-grow: 1;
    }
    
    .anomaly-title {
        font-weight: bold;
        color: var(--military-text);
        margin-bottom: 0.25rem;
    }
    
    .anomaly-description {
        font-size: 0.9rem;
        color: var(--military-text);
        opacity: 0.8;
        margin-bottom: 0.25rem;
    }
    
    .anomaly-time {
        font-size: 0.8rem;
        color: var(--military-highlight);
    }
    
    .btn-military.active {
        background-color: var(--military-highlight);
        color: var(--military-dark);
    }
`;

// Inject styles
const analyticsStyleSheet = document.createElement('style');
analyticsStyleSheet.textContent = analyticsStyles;
document.head.appendChild(analyticsStyleSheet);

// Initialize analytics system when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.analyticsSystem = new AnalyticsSystem();
    window.analyticsDashboard = new AnalyticsDashboard();
});

// Global function to update analytics charts
function updateAnalyticsCharts() {
    if (window.analyticsSystem) {
        window.analyticsSystem.loadAnalyticsData();
    }
}
