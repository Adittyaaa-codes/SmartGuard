import cv2
import numpy as np
import streamlit as st
from ultralytics import YOLO
import time
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium

# -----------------------------------------------------
# Multi-Sensor Simulator for Military Applications
# -----------------------------------------------------

class MultiSensorSimulator:
    def __init__(self):
        """Initialize multi-sensor simulation capabilities"""
        self.radar_range = 5000  # meters
        self.thermal_baseline = 25  # Celsius
        
        # GPS simulation - Military base coordinates (New Delhi area)
        self.base_lat = 28.6139  # New Delhi latitude
        self.base_lon = 77.2090  # New Delhi longitude
        self.base_alt = 216.0    # Altitude in meters
        self.gps_accuracy = 3.5  # GPS accuracy in meters
        
    def generate_thermal_data(self, rgb_frame):
        """Generate thermal imaging data from RGB frame"""
        # Convert to grayscale for thermal base
        gray = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2GRAY)
        
        # Apply thermal colormap
        thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
        
        # Generate temperature overlay
        height, width = gray.shape
        temp_overlay = np.random.normal(self.thermal_baseline, 5, (height, width))
        
        # Simulate human body heat (higher temperature areas)
        for _ in range(np.random.randint(1, 3)):
            x = np.random.randint(50, width-50)
            y = np.random.randint(50, height-50)
            size = np.random.randint(20, 35)
            cv2.circle(temp_overlay, (x, y), size, 37, -1)  # Body temperature
        
        return thermal, temp_overlay
    
    def generate_radar_data(self):
        """Generate radar sweep data with targets"""
        angles = np.linspace(0, 360, 180)
        ranges = []
        targets = []
        
        for angle in angles:
            rand = np.random.random()
            
            if rand > 0.95:  # 5% chance of detection
                if rand > 0.98:  # High priority target
                    distance = np.random.uniform(1000, 5000)
                    targets.append({
                        'type': 'VEHICLE', 
                        'range': distance, 
                        'bearing': angle,
                        'priority': 'HIGH'
                    })
                else:  # Personnel
                    distance = np.random.uniform(100, 1000)
                    targets.append({
                        'type': 'PERSONNEL', 
                        'range': distance, 
                        'bearing': angle,
                        'priority': 'MEDIUM'
                    })
                ranges.append(distance)
            else:
                ranges.append(self.radar_range)  # No detection
        
        return angles, ranges, targets
    
    def generate_lidar_data(self):
        """Generate 3D LIDAR point cloud data"""
        # Ground plane points
        n_points = 200
        x = np.random.uniform(-25, 25, n_points)
        y = np.random.uniform(-25, 25, n_points)
        z = np.random.uniform(-1, 1, n_points)  # Ground level
        
        # Add some elevated objects (buildings, vehicles)
        for _ in range(3):
            obj_x = np.random.uniform(-20, 20, 30)
            obj_y = np.random.uniform(-20, 20, 30)
            obj_z = np.random.uniform(2, 8, 30)  # Elevated objects
            
            x = np.concatenate([x, obj_x])
            y = np.concatenate([y, obj_y])
            z = np.concatenate([z, obj_z])
        
        return x, y, z
    
    def generate_ir_data(self, rgb_frame):
        """Generate infrared imaging data"""
        # Convert to grayscale
        gray = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2GRAY)
        
        # Enhance contrast for IR effect
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Apply IR colormap
        ir_image = cv2.applyColorMap(enhanced, cv2.COLORMAP_HOT)
        
        return ir_image
    
    def generate_gps_data(self):
        """Generate GPS coordinates with military precision"""
        # Simulate slight movement around base coordinates
        lat_offset = np.random.uniform(-0.001, 0.001)  # ~100m variation
        lon_offset = np.random.uniform(-0.001, 0.001)  # ~100m variation
        alt_offset = np.random.uniform(-5, 5)          # 5m altitude variation
        
        current_lat = self.base_lat + lat_offset
        current_lon = self.base_lon + lon_offset
        current_alt = self.base_alt + alt_offset
        
        # GPS quality metrics
        hdop = np.random.uniform(0.8, 2.1)  # Horizontal Dilution of Precision
        satellites = np.random.randint(8, 12)  # Number of satellites
        
        return {
            'latitude': current_lat,
            'longitude': current_lon,
            'altitude': current_alt,
            'accuracy': self.gps_accuracy,
            'hdop': hdop,
            'satellites': satellites,
            'timestamp': time.time()
        }
    
    def create_tactical_map(self, gps_data, persons=None, threats=None):
        """Create tactical map with GPS location and detected entities"""
        # Create base map
        m = folium.Map(
            location=[gps_data['latitude'], gps_data['longitude']],
            zoom_start=18,
            tiles='OpenStreetMap'
        )
        
        # Add satellite imagery layer
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='Google Satellite',
            name='Satellite View',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Current position marker
        folium.Marker(
            [gps_data['latitude'], gps_data['longitude']],
            popup=f"""
            <b>Military Base Position</b><br>
            Lat: {gps_data['latitude']:.6f}<br>
            Lon: {gps_data['longitude']:.6f}<br>
            Alt: {gps_data['altitude']:.1f}m<br>
            Accuracy: {gps_data['accuracy']}m<br>
            Satellites: {gps_data['satellites']}
            """,
            icon=folium.Icon(color='blue', icon='crosshairs', prefix='fa')
        ).add_to(m)
        
        # Add accuracy circle
        folium.Circle(
            location=[gps_data['latitude'], gps_data['longitude']],
            radius=gps_data['accuracy'],
            color='blue',
            fillColor='lightblue',
            fillOpacity=0.2,
            popup=f'GPS Accuracy: {gps_data["accuracy"]}m'
        ).add_to(m)
        
        # Add detected persons
        if persons:
            for i, person in enumerate(persons):
                # Generate nearby coordinates for detected persons
                person_lat = gps_data['latitude'] + np.random.uniform(-0.0001, 0.0001)
                person_lon = gps_data['longitude'] + np.random.uniform(-0.0001, 0.0001)
                
                color = 'red' if person['status'] == 'DANGER' else 'green'
                icon_name = 'exclamation-triangle' if person['status'] == 'DANGER' else 'user'
                
                folium.Marker(
                    [person_lat, person_lon],
                    popup=f"""
                    <b>{person['name']}</b><br>
                    Status: {person['status']}<br>
                    Confidence: {person['confidence']:.2f}<br>
                    Threats: {len(person.get('nearby_threats', []))}
                    """,
                    icon=folium.Icon(color=color, icon=icon_name, prefix='fa')
                ).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        return m

# -----------------------------------------------------
# Enhanced Threat Detection System
# -----------------------------------------------------

class EnhancedThreatDetector:
    def __init__(self):
        """Initialize the enhanced threat detection system"""
        # Load YOLO model
        self.model = YOLO('yolov8n.pt')
        
        # Initialize multi-sensor simulator
        self.sensor_sim = MultiSensorSimulator()
        
        # Performance optimization
        self.frame_skip_counter = 0
        self.detection_interval = 2
        self.last_detection_result = ([], [])
        
        # Threat keywords
        self.threat_keywords = [
            'scissors', 'knife', 'blade', 'pen', 'pencil', 
            'stick', 'tool', 'utensil', 'bottle', 'cup',
            'toothbrush', 'brush', 'spoon', 'fork',
            'remote', 'phone', 'cell phone', 'chips',
            'baseball bat', 'bat', 'hammer', 'screwdriver',
            'umbrella', 'cane', 'ruler'
        ]
        
        # Camera settings
        self.cap = None
        self.is_running = False
        
    def detect_threats(self, frame):
        """Detect persons and threats with performance optimization"""
        # Frame skipping for better performance
        self.frame_skip_counter += 1
        if self.frame_skip_counter < self.detection_interval:
            return self.last_detection_result
        
        self.frame_skip_counter = 0
        
        # Run optimized detection
        results = self.model(frame, conf=0.3, verbose=False, imgsz=416)
        
        persons = []
        threat_objects = []
        
        # Process detections
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    bbox = box.xyxy[0].tolist()
                    class_name = self.model.names[class_id]
                    
                    # Detect persons
                    if class_name.lower() == 'person':
                        persons.append({
                            'name': 'PERSON',
                            'confidence': confidence,
                            'bbox': [int(x) for x in bbox],
                            'status': 'SAFE',
                            'nearby_threats': []
                        })
                    
                    # Detect threat objects
                    else:
                        is_threat = any(keyword in class_name.lower() 
                                      for keyword in self.threat_keywords)
                        
                        if is_threat:
                            # Map pen misclassifications
                            if class_name.lower() in ['toothbrush', 'baseball bat', 'bat']:
                                display_name = 'SHARP OBJECT (Pen-like)'
                                threat_level = 'IMMEDIATE_THREAT'
                                risk_score = confidence * 0.9
                            else:
                                display_name = class_name.upper()
                                threat_level = 'POTENTIAL_THREAT'
                                risk_score = confidence * 0.7
                            
                            threat_objects.append({
                                'name': display_name,
                                'confidence': confidence,
                                'bbox': [int(x) for x in bbox],
                                'threat_level': threat_level,
                                'risk_score': risk_score,
                                'original_class': class_name
                            })
        
        # Associate threats with persons
        for person in persons:
            person_bbox = person['bbox']
            person_center_x = (person_bbox[0] + person_bbox[2]) / 2
            person_center_y = (person_bbox[1] + person_bbox[3]) / 2
            
            # Add GPS location metadata for person
            person['gps_offset'] = {
                'lat_offset': np.random.uniform(-0.0001, 0.0001),
                'lon_offset': np.random.uniform(-0.0001, 0.0001)
            }
            
            nearby_threats = []
            
            for threat in threat_objects:
                threat_bbox = threat['bbox']
                threat_center_x = (threat_bbox[0] + threat_bbox[2]) / 2
                threat_center_y = (threat_bbox[1] + threat_bbox[3]) / 2
                
                # Calculate distance
                distance = ((person_center_x - threat_center_x) ** 2 + 
                           (person_center_y - threat_center_y) ** 2) ** 0.5
                
                # Proximity threshold
                proximity_threshold = min(frame.shape[1], frame.shape[0]) * 0.3
                
                if distance < proximity_threshold:
                    nearby_threats.append(threat)
            
            # Update person status
            if nearby_threats:
                person['status'] = 'DANGER'
                person['nearby_threats'] = nearby_threats
                person['name'] = f"ARMED PERSON ({len(nearby_threats)} threats)"
            else:
                person['status'] = 'SAFE'
                person['name'] = "SAFE PERSON"
        
        # Cache results
        self.last_detection_result = (persons, threat_objects)
        
        return persons, threat_objects
    
    def draw_detections(self, frame, persons, threat_objects):
        """Draw detection boxes with person safety assessment"""
        height, width = frame.shape[:2]
        
        # Header
        cv2.rectangle(frame, (0, 0), (width, 80), (0, 0, 0), -1)
        cv2.putText(frame, "MILITARY PERSON SAFETY MONITORING", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Count safe and danger persons
        safe_count = len([p for p in persons if p['status'] == 'SAFE'])
        danger_count = len([p for p in persons if p['status'] == 'DANGER'])
        
        status_text = f"Safe: {safe_count} | Danger: {danger_count}"
        cv2.putText(frame, status_text, (10, 55), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 1)
        
        # Overall status
        if danger_count > 0:
            status, color = "ARMED PERSONS DETECTED", (0, 0, 255)
        elif safe_count > 0:
            status, color = "ALL PERSONS SAFE", (0, 255, 0)
        else:
            status, color = "MONITORING AREA", (0, 255, 255)
            
        cv2.putText(frame, status, (10, height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Draw persons
        for person in persons:
            bbox = person['bbox']
            
            if person['status'] == 'DANGER':
                color = (0, 0, 255)  # Red for dangerous persons
                thickness = 4
                # Pulsing effect
                pulse = int(time.time() * 5) % 2
                if pulse:
                    thickness = 6
            else:
                color = (0, 255, 0)  # Green for safe persons
                thickness = 3
            
            # Draw bounding box
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), 
                         (int(bbox[2]), int(bbox[3])), color, thickness)
            
            # Labels
            cv2.putText(frame, person['status'], (int(bbox[0]), int(bbox[1]) - 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            cv2.putText(frame, person['name'], (int(bbox[0]), int(bbox[1]) - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        
        return frame
    
    def start_camera(self):
        """Start optimized camera capture"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return False
        
        # Optimized camera settings
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        self.is_running = True
        return True
    
    def get_frame(self):
        """Get processed frame with threat detection"""
        if not self.cap or not self.is_running:
            return None, [], []
        
        ret, frame = self.cap.read()
        if not ret:
            return None, [], []
        
        # Flip frame horizontally
        frame = cv2.flip(frame, 1)
        
        # Detect threats
        persons, threat_objects = self.detect_threats(frame)
        
        # Draw detections
        processed_frame = self.draw_detections(frame, persons, threat_objects)
        
        return processed_frame, persons, threat_objects
    
    def stop_camera(self):
        """Stop camera capture"""
        self.is_running = False
        if self.cap:
            self.cap.release()

# -----------------------------------------------------
# Streamlit Enhanced Multi-Sensor App
# -----------------------------------------------------

def main():
    st.set_page_config(
        page_title="Military Multi-Sensor System",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #FF0000, #8B0000);
            padding: 1rem;
            text-align: center;
            color: white;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .threat-alert {
            background-color: #FF4444;
            color: white;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
        }
        .secure-status {
            background-color: #44AA44;
            color: white;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>INDIAN MILITARY MULTI-SENSOR SYSTEM</h1>
            <h2>Person Safety Monitoring with Sensor Fusion</h2>
            <p>Live Camera Demo with Thermal, IR, Radar & LIDAR</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize detector
    if 'detector' not in st.session_state:
        with st.spinner("Initializing Enhanced AI System..."):
            st.session_state.detector = EnhancedThreatDetector()
        st.success("Multi-Sensor AI System Ready!")
    
    detector = st.session_state.detector
    
    # Control buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("Start Multi-Sensor Detection", key="start_btn"):
            if detector.start_camera():
                st.session_state.camera_running = True
                st.success("Multi-Sensor System Active!")
            else:
                st.error("Camera not accessible!")
    
    with col2:
        if st.button("Stop Detection", key="stop_btn"):
            detector.stop_camera()
            st.session_state.camera_running = False
            st.info("System Stopped")
    
    with col3:
        auto_refresh = st.checkbox("Auto Refresh", value=True)
    
    # Main multi-sensor interface
    if st.session_state.get('camera_running', False):
        
        # Create main layout
        main_col, sensor_col = st.columns([2, 1])
        
        with main_col:
            st.subheader("Live Person Safety Monitoring")
            video_placeholder = st.empty()
            status_placeholder = st.empty()
        
        with sensor_col:
            st.subheader("Multi-Sensor Data")
            
            # Sensor tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Thermal", "IR", "Radar", "LIDAR", "GPS/Map"])
            
            with tab1:
                thermal_placeholder = st.empty()
                temp_metric = st.empty()
            
            with tab2:
                ir_placeholder = st.empty()
            
            with tab3:
                radar_placeholder = st.empty()
                radar_info = st.empty()
            
            with tab4:
                lidar_placeholder = st.empty()
            
            with tab5:
                gps_metrics = st.empty()
                map_placeholder = st.empty()
        
        # Real-time processing loop
        if auto_refresh:
            while st.session_state.get('camera_running', False):
                frame, persons, threat_objects = detector.get_frame()
                
                if frame is not None:
                    # Main video display
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    video_placeholder.image(frame_rgb, channels="RGB", width=480)
                    
                    # Generate multi-sensor data
                    thermal_img, temp_data = detector.sensor_sim.generate_thermal_data(frame)
                    ir_img = detector.sensor_sim.generate_ir_data(frame)
                    radar_angles, radar_ranges, radar_targets = detector.sensor_sim.generate_radar_data()
                    lidar_x, lidar_y, lidar_z = detector.sensor_sim.generate_lidar_data()
                    gps_data = detector.sensor_sim.generate_gps_data()
                    
                    # Update sensor displays
                    # Thermal imaging
                    thermal_rgb = cv2.cvtColor(thermal_img, cv2.COLOR_BGR2RGB)
                    thermal_placeholder.image(thermal_rgb, width=280, caption="Thermal Imaging")
                    temp_metric.metric("Avg Temperature", f"{temp_data.mean():.1f}°C")
                    
                    # IR imaging
                    ir_rgb = cv2.cvtColor(ir_img, cv2.COLOR_BGR2RGB)
                    ir_placeholder.image(ir_rgb, width=280, caption="Infrared Spectrum")
                    
                    # Radar display
                    fig_radar = go.Figure()
                    
                    # Add radar contacts
                    detected_ranges = [r for r in radar_ranges if r < detector.sensor_sim.radar_range]
                    detected_angles = [radar_angles[i] for i, r in enumerate(radar_ranges) 
                                     if r < detector.sensor_sim.radar_range]
                    
                    if detected_ranges:
                        fig_radar.add_trace(go.Scatterpolar(
                            r=detected_ranges,
                            theta=detected_angles,
                            mode='markers',
                            marker=dict(size=4, color='lime'),
                            name='Contacts'
                        ))
                    
                    # Add priority targets
                    for target in radar_targets[:3]:
                        color = 'red' if target['priority'] == 'HIGH' else 'orange'
                        fig_radar.add_trace(go.Scatterpolar(
                            r=[target['range']],
                            theta=[target['bearing']],
                            mode='markers+text',
                            marker=dict(size=8, color=color),
                            text=[target['type']],
                            name=target['type']
                        ))
                    
                    fig_radar.update_layout(
                        polar=dict(
                            radialaxis=dict(visible=True, range=[0, 5000]),
                            angularaxis=dict(direction="clockwise")
                        ),
                        showlegend=False,
                        height=250,
                        margin=dict(t=30, b=10, l=10, r=10)
                    )
                    
                    radar_placeholder.plotly_chart(fig_radar, use_container_width=True)
                    
                    # Radar info
                    if radar_targets:
                        radar_text = f"**Contacts:** {len(radar_targets)}\n"
                        for target in radar_targets[:2]:
                            radar_text += f"• {target['type']} at {target['range']:.0f}m\n"
                        radar_info.markdown(radar_text)
                    
                    # LIDAR 3D visualization
                    fig_lidar = go.Figure(data=[go.Scatter3d(
                        x=lidar_x[:150],
                        y=lidar_y[:150],
                        z=lidar_z[:150],
                        mode='markers',
                        marker=dict(
                            size=2,
                            color=lidar_z[:150],
                            colorscale='Plasma',
                            opacity=0.6
                        )
                    )])
                    
                    fig_lidar.update_layout(
                        scene=dict(
                            xaxis_title='X (m)',
                            yaxis_title='Y (m)',
                            zaxis_title='Z (m)'
                        ),
                        height=250,
                        margin=dict(t=30, b=10, l=10, r=10)
                    )
                    
                    lidar_placeholder.plotly_chart(fig_lidar, use_container_width=True)
                    
                    # GPS and Map display
                    gps_metrics.markdown(f"""
                    **GPS Coordinates:**
                    - **Latitude:** {gps_data['latitude']:.6f}°
                    - **Longitude:** {gps_data['longitude']:.6f}°  
                    - **Altitude:** {gps_data['altitude']:.1f}m
                    - **Accuracy:** {gps_data['accuracy']}m
                    - **Satellites:** {gps_data['satellites']}
                    - **HDOP:** {gps_data['hdop']:.2f}
                    """)
                    
                    # Create and display tactical map
                    try:
                        tactical_map = detector.sensor_sim.create_tactical_map(gps_data, persons, threat_objects)
                        map_data = st_folium(tactical_map, width=280, height=250, returned_data=["last_object_clicked"])
                    except Exception as e:
                        map_placeholder.error("Map requires folium package. Install with: pip install folium streamlit-folium")
                    
                    # Status display
                    safe_count = len([p for p in persons if p['status'] == 'SAFE'])
                    danger_count = len([p for p in persons if p['status'] == 'DANGER'])
                    
                    if danger_count > 0:
                        status_placeholder.markdown(
                            f'<div class="threat-alert">ARMED PERSONS DETECTED ({danger_count})</div>',
                            unsafe_allow_html=True
                        )
                    elif safe_count > 0:
                        status_placeholder.markdown(
                            f'<div class="secure-status">ALL PERSONS SAFE ({safe_count})</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        status_placeholder.markdown(
                            '<div class="secure-status">MONITORING AREA</div>',
                            unsafe_allow_html=True
                        )
                
                # Optimized refresh rate for 24+ FPS
                time.sleep(0.04)
        
        else:
            # Manual mode
            if st.button("Capture Frame"):
                frame, persons, threat_objects = detector.get_frame()
                
                if frame is not None:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    st.image(frame_rgb, channels="RGB", use_column_width=True)
                    
                    safe_count = len([p for p in persons if p['status'] == 'SAFE'])
                    danger_count = len([p for p in persons if p['status'] == 'DANGER'])
                    
                    if danger_count > 0:
                        st.error(f"ARMED PERSONS DETECTED ({danger_count})")
                    elif safe_count > 0:
                        st.success(f"ALL PERSONS SAFE ({safe_count})")
                    else:
                        st.info("MONITORING AREA")
    
    else:
        st.info("Click 'Start Multi-Sensor Detection' to begin advanced surveillance")
        st.markdown("""
            ### Enhanced Features:
            - **Person Safety Assessment**: Identifies armed vs safe individuals
            - **Thermal Imaging**: Heat signature detection and analysis
            - **Infrared Spectrum**: Night vision and heat source identification
            - **Radar Sweep**: Long-range target detection and tracking
            - **LIDAR Point Cloud**: 3D environmental mapping and obstacle detection
            - **GPS & Tactical Maps**: Real-time location tracking with interactive maps
            - **Optimized Performance**: 24+ FPS with advanced algorithms
        """)

if __name__ == "__main__":
    main()