import cv2, os, time, numpy as np
import streamlit as st
from ultralytics import YOLO
import threading
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime
import torch
from roboflow import Roboflow

# -----------------------------------------------------
# Military Drone Sensor Simulator
# -----------------------------------------------------
class MilitaryDroneSensorSimulator:
    def __init__(self):
        self.radar_range = 5000  # meters
        self.lidar_points = 1000
        self.thermal_temp_range = (-40, 60)  # Celsius
        
    def generate_thermal_data(self, rgb_frame):
        """Convert RGB to realistic thermal imaging"""
        # Convert to grayscale and enhance for thermal effect
        gray = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2GRAY)
        
        # Apply thermal colormap
        thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
        
        # Generate temperature overlay
        height, width = gray.shape
        temp_overlay = np.random.normal(25, 8, (height, width))  # Base 25°C ± 8°C
        
        # Simulate human body heat signatures (37°C)
        for _ in range(np.random.randint(1, 3)):
            x = np.random.randint(50, width-50)
            y = np.random.randint(50, height-50)
            size = np.random.randint(25, 40)
            cv2.circle(temp_overlay, (x, y), size, 37, -1)
        
        # Add environmental heat sources
        for _ in range(np.random.randint(0, 2)):
            x = np.random.randint(30, width-30)
            y = np.random.randint(30, height-30)
            cv2.rectangle(temp_overlay, (x-20, y-20), (x+20, y+20), 45, -1)  # Hot objects
        
        return thermal, temp_overlay
    
    def generate_radar_data(self):
        """Simulate military radar sweep with realistic targets"""
        angles = np.linspace(0, 360, 360)
        ranges = []
        targets = []
        
        for angle in angles:
            # Simulate different types of radar contacts
            rand = np.random.random()
            
            if rand > 0.98:  # Aircraft signature (2% chance)
                distance = np.random.uniform(5000, 15000)
                targets.append({
                    'type': 'AIRCRAFT', 
                    'range': distance, 
                    'bearing': angle,
                    'rcs': 10,  # Radar Cross Section
                    'priority': 'HIGH'
                })
            elif rand > 0.95:  # Vehicle signature (3% chance)
                distance = np.random.uniform(1000, 5000)
                targets.append({
                    'type': 'VEHICLE', 
                    'range': distance, 
                    'bearing': angle,
                    'rcs': 5,
                    'priority': 'MEDIUM'
                })
            elif rand > 0.92:  # Personnel signature (3% chance)
                distance = np.random.uniform(100, 1000)
                targets.append({
                    'type': 'PERSONNEL', 
                    'range': distance, 
                    'bearing': angle,
                    'rcs': 1,
                    'priority': 'LOW'
                })
            else:
                distance = self.radar_range  # No detection
            
            ranges.append(distance)
        
        return angles, ranges, targets
    
    def generate_lidar_data(self):
        """Generate realistic 3D LIDAR point cloud with structures"""
        # Ground plane
        ground_points = 300
        x_ground = np.random.uniform(-50, 50, ground_points)
        y_ground = np.random.uniform(-50, 50, ground_points) 
        z_ground = np.random.uniform(-2, 2, ground_points)
        
        # Building structures
        buildings = []
        for i in range(3):  # 3 buildings
            bx = np.random.uniform(-40, 40)
            by = np.random.uniform(-40, 40)
            bw = np.random.uniform(5, 15)
            bh = np.random.uniform(5, 20)
            
            # Create building walls
            wall_points = 100
            bx_pts = np.random.uniform(bx, bx+bw, wall_points)
            by_pts = np.random.uniform(by, by+bw, wall_points)
            bz_pts = np.random.uniform(0, bh, wall_points)
            
            buildings.extend([bx_pts, by_pts, bz_pts])
        
        # Vehicle signatures
        vehicles = []
        for i in range(2):  # 2 vehicles
            vx = np.random.uniform(-30, 30)
            vy = np.random.uniform(-30, 30)
            
            # Vehicle outline
            vehicle_points = 20
            vx_pts = np.random.uniform(vx, vx+4, vehicle_points)
            vy_pts = np.random.uniform(vy, vy+8, vehicle_points)
            vz_pts = np.random.uniform(0, 2, vehicle_points)
            
            vehicles.extend([vx_pts, vy_pts, vz_pts])
        
        # Combine all points
        x = np.concatenate([x_ground] + [buildings[i] for i in range(0, len(buildings), 3)] + [vehicles[i] for i in range(0, len(vehicles), 3)])
        y = np.concatenate([y_ground] + [buildings[i] for i in range(1, len(buildings), 3)] + [vehicles[i] for i in range(1, len(vehicles), 3)])
        z = np.concatenate([z_ground] + [buildings[i] for i in range(2, len(buildings), 3)] + [vehicles[i] for i in range(2, len(vehicles), 3)])
        
        return x, y, z
    
    def generate_ir_data(self, rgb_frame):
        """Generate military-grade infrared imaging"""
        # Convert to grayscale
        gray = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2GRAY)
        
        # Apply military IR characteristics
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Add IR noise and grain
        noise = np.random.normal(0, 3, enhanced.shape).astype(np.uint8)
        ir_image = cv2.add(enhanced, noise)
        
        # Apply military IR colormap (bone/hot)
        ir_colored = cv2.applyColorMap(ir_image, cv2.COLORMAP_HOT)
        
        return ir_colored

# -----------------------------------------------------
# Dataset Download Function  
# -----------------------------------------------------
def download_weapon_dataset():
    """Download OD-WeaponDetection dataset"""
    print("📥 Downloading weapon detection dataset...")
    rf = Roboflow(api_key="EJI3GWljQHGWxShDqKu6")
    project = rf.workspace("ufg-lr3ua").project("ari-dasci-od-weapondetection-xml-to-yolo-txt")
    dataset = project.version(2).download("yolov8")
    print(f"✅ Dataset downloaded to: {dataset.location}")
    return dataset.location

# -----------------------------------------------------
# Enhanced Military Drone Threat Detection System
# -----------------------------------------------------
class MilitaryDroneThreatDetector:
    def __init__(self, use_weapon_model=True):
        print("🚁 Initializing Military Drone Multi-Sensor System...")
        
        # Initialize sensor simulator
        self.sensor_sim = MilitaryDroneSensorSimulator()
        
        # Initialize weapon detection model
        weapon_model_path = "runs/detect/weapon_detector/weights/best.pt"
        
        if use_weapon_model and os.path.exists(weapon_model_path):
            self.model = YOLO(weapon_model_path)
            print("✅ Military Weapon Detection Model Loaded")
            self.using_weapon_model = True
            self.weapon_classes = {
                0: 'knife', 1: 'pistol', 2: 'smartphone',
                3: 'monedero', 4: 'billete', 5: 'tarjeta'
            }
        else:
            self.model = YOLO('yolov8n.pt')
            print("✅ Standard Detection Model Loaded")
            self.using_weapon_model = False
            self.threat_keywords = [
                'scissors', 'knife', 'blade', 'pen', 'pencil', 'stick',
                'tool', 'bottle', 'cup', 'phone', 'remote', 'bat'
            ]
    
    def train_weapon_model(self):
        """Train specialized weapon detection model"""
        st.info("🔥 Training Military Weapon Detection Model...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("📥 Downloading military weapon dataset...")
            progress_bar.progress(10)
            
            dataset_path = download_weapon_dataset()
            progress_bar.progress(30)
            
            status_text.text("🏋️ Training neural network...")
            model = YOLO('yolov8s.pt')
            
            results = model.train(
                data=f"{dataset_path}/data.yaml",
                epochs=30, imgsz=640, batch=16,
                name='weapon_detector', patience=8, save=True,
                device='cuda' if torch.cuda.is_available() else 'cpu'
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Military weapon detection model trained!")
            
            # Update to use trained model
            self.model = YOLO('runs/detect/weapon_detector/weights/best.pt')
            self.using_weapon_model = True
            
            st.success("🎯 Model training completed! Enhanced threat detection active.")
            return results
            
        except Exception as e:
            st.error(f"❌ Training failed: {e}")
            return None
    
    def detect_threats(self, frame):
        """Military-grade threat detection with person tracking"""
        results = self.model(frame, conf=0.3, verbose=False, imgsz=480)
        
        persons = []
        threats = []
        
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    bbox = box.xyxy[0].tolist()
                    class_name = self.model.names[class_id]
                    
                    if class_name.lower() == 'person':
                        persons.append({
                            'name': 'PERSONNEL',
                            'confidence': confidence,
                            'bbox': [int(x) for x in bbox],
                            'threat_level': 'NEUTRAL',
                            'status': 'MONITORING'
                        })
                    else:
                        # Weapon/threat detection logic
                        is_weapon = False
                        threat_level = 'MONITOR'
                        
                        if self.using_weapon_model:
                            weapon_name = self.weapon_classes.get(class_id, 'unknown')
                            if weapon_name in ['knife', 'pistol']:
                                is_weapon = True
                                threat_level = 'IMMEDIATE_THREAT'
                        else:
                            if any(keyword in class_name.lower() for keyword in self.threat_keywords):
                                is_weapon = True
                                threat_level = 'POTENTIAL_THREAT'
                        
                        if is_weapon or confidence > 0.5:
                            threats.append({
                                'name': class_name.upper(),
                                'confidence': confidence,
                                'bbox': [int(x) for x in bbox],
                                'threat_level': threat_level,
                                'type': 'weapon' if is_weapon else 'object'
                            })
        
        return persons + threats

# -----------------------------------------------------
# Streamlit Multi-Sensor Dashboard
# -----------------------------------------------------
def create_military_dashboard():
    st.set_page_config(
        page_title="🚁 Military Drone Command Center", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for military theme
    st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background-color: #0e1117;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e3a3a 0%, #2d4a4a 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00ff41;
        color: white;
        margin: 10px 0;
    }
    .threat-alert {
        background: linear-gradient(135deg, #4a1e1e 0%, #6d2c2c 100%);
        border-left: 4px solid #ff0000;
    }
    .safe-status {
        background: linear-gradient(135deg, #1e4a1e 0%, #2c6d2c 100%);
        border-left: 4px solid #00ff41;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #1e3a3a, #2d4a4a); border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='color: #00ff41; font-size: 2.5rem; margin: 0;'>🚁 MILITARY DRONE COMMAND CENTER</h1>
        <h3 style='color: #ffffff; margin: 10px 0 0 0;'>Multi-Sensor Threat Detection System</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize detector
    if 'detector' not in st.session_state:
        st.session_state.detector = MilitaryDroneThreatDetector()
    
    # Sidebar Controls
    with st.sidebar:
        st.title("🎛️ Mission Control")
        
        # Mission status
        st.subheader("🎯 Mission Status")
        mission_status = st.selectbox("Status", ["STANDBY", "ACTIVE", "PATROL", "ENGAGE"])
        
        # Sensor controls
        st.subheader("📡 Sensor Array")
        active_sensors = st.multiselect(
            "Active Sensors",
            ["Visual", "Thermal", "Radar", "LIDAR", "Infrared"],
            default=["Visual", "Thermal", "Radar"]
        )
        
        # Threat levels
        st.subheader("⚠️ Threat Settings")
        threat_sensitivity = st.slider("Detection Sensitivity", 0.1, 0.9, 0.3)
        
        # Model training
        st.subheader("🤖 AI Training")
        if st.button("🔥 Train Weapon Model"):
            st.session_state.detector.train_weapon_model()
    
    # Main sensor display grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Visual Threat Detection")
        visual_placeholder = st.empty()
        threat_status_placeholder = st.empty()
    
    with col2:
        st.subheader("🌡️ Thermal Imaging")
        thermal_placeholder = st.empty()
        temp_metrics_placeholder = st.empty()
    
    # Radar and LIDAR row
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("📡 Radar Sweep")
        radar_placeholder = st.empty()
    
    with col4:
        st.subheader("📊 LIDAR Point Cloud")
        lidar_placeholder = st.empty()
    
    # IR and metrics row
    col5, col6 = st.columns(2)
    
    with col5:
        st.subheader("🔴 Infrared Spectrum")
        ir_placeholder = st.empty()
    
    with col6:
        st.subheader("📈 Mission Metrics")
        metrics_placeholder = st.empty()
    
    # Real-time surveillance
    if st.button("🚀 Start Multi-Sensor Surveillance", type="primary"):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("❌ Camera not accessible")
            return
        
        # Real-time loop
        frame_count = 0
        threat_detections = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Generate multi-sensor data
            if "Thermal" in active_sensors:
                thermal_img, temp_data = st.session_state.detector.sensor_sim.generate_thermal_data(frame)
            if "Radar" in active_sensors:
                radar_angles, radar_ranges, radar_targets = st.session_state.detector.sensor_sim.generate_radar_data()
            if "LIDAR" in active_sensors:
                lidar_x, lidar_y, lidar_z = st.session_state.detector.sensor_sim.generate_lidar_data()
            if "Infrared" in active_sensors:
                ir_img = st.session_state.detector.sensor_sim.generate_ir_data(frame)
            
            # Threat detection
            detections = st.session_state.detector.detect_threats(frame)
            
            # Count threats
            current_threats = len([d for d in detections if d.get('threat_level') != 'NEUTRAL'])
            threat_detections += current_threats
            
            # Update visual display
            if "Visual" in active_sensors:
                # Draw detection boxes
                display_frame = frame.copy()
                for detection in detections:
                    bbox = detection['bbox']
                    threat_level = detection.get('threat_level', 'MONITOR')
                    
                    # Color coding
                    if threat_level == 'IMMEDIATE_THREAT':
                        color = (0, 0, 255)  # Red
                    elif threat_level == 'POTENTIAL_THREAT':
                        color = (0, 165, 255)  # Orange
                    elif threat_level == 'NEUTRAL':
                        color = (0, 255, 0)  # Green
                    else:
                        color = (255, 255, 0)  # Cyan
                    
                    # Draw detection
                    cv2.rectangle(display_frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
                    cv2.putText(display_frame, f"{detection['name']} {detection['confidence']:.2f}", 
                              (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
                visual_placeholder.image(display_frame, channels="BGR", use_column_width=True)
                
                # Threat status
                if current_threats > 0:
                    threat_status_placeholder.markdown("""
                    <div class='metric-card threat-alert'>
                        <h3>🚨 THREATS DETECTED</h3>
                        <p>Active Threats: {}</p>
                        <p>Status: ENGAGING TARGETS</p>
                    </div>
                    """.format(current_threats), unsafe_allow_html=True)
                else:
                    threat_status_placeholder.markdown("""
                    <div class='metric-card safe-status'>
                        <h3>✅ AREA SECURE</h3>
                        <p>No Active Threats</p>
                        <p>Status: MONITORING</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Update thermal display
            if "Thermal" in active_sensors:
                thermal_placeholder.image(thermal_img, channels="BGR", use_column_width=True)
                temp_metrics_placeholder.metric("Average Temperature", f"{temp_data.mean():.1f}°C")
            
            # Update radar
            if "Radar" in active_sensors:
                fig_radar = go.Figure()
                
                # Plot radar sweep
                detected_ranges = [r for r in radar_ranges if r < st.session_state.detector.sensor_sim.radar_range]
                detected_angles = [radar_angles[i] for i, r in enumerate(radar_ranges) if r < st.session_state.detector.sensor_sim.radar_range]
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=detected_ranges[:50],
                    theta=detected_angles[:50],
                    mode='markers',
                    marker=dict(size=6, color='lime'),
                    name='Contacts'
                ))
                
                # Add target annotations
                for target in radar_targets[:5]:  # Show first 5 targets
                    fig_radar.add_trace(go.Scatterpolar(
                        r=[target['range']],
                        theta=[target['bearing']],
                        mode='markers+text',
                        marker=dict(size=10, color='red' if target['priority'] == 'HIGH' else 'orange'),
                        text=[target['type']],
                        name=target['type']
                    ))
                
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 15000], color='white'),
                        angularaxis=dict(color='white'),
                        bgcolor="black"
                    ),
                    showlegend=False,
                    height=400,
                    paper_bgcolor="black",
                    font_color="white"
                )
                
                radar_placeholder.plotly_chart(fig_radar, use_container_width=True)
            
            # Update LIDAR
            if "LIDAR" in active_sensors:
                fig_lidar = go.Figure(data=[go.Scatter3d(
                    x=lidar_x[:300],
                    y=lidar_y[:300],
                    z=lidar_z[:300],
                    mode='markers',
                    marker=dict(
                        size=2,
                        color=lidar_z[:300],
                        colorscale='Plasma',
                        opacity=0.8
                    )
                )])
                
                fig_lidar.update_layout(
                    scene=dict(
                        xaxis_title='X (meters)',
                        yaxis_title='Y (meters)',
                        zaxis_title='Z (meters)',
                        bgcolor="black",
                        xaxis=dict(gridcolor='gray'),
                        yaxis=dict(gridcolor='gray'),
                        zaxis=dict(gridcolor='gray')
                    ),
                    height=400,
                    paper_bgcolor="black"
                )
                
                lidar_placeholder.plotly_chart(fig_lidar, use_container_width=True)
            
            # Update IR
            if "Infrared" in active_sensors:
                ir_placeholder.image(ir_img, channels="BGR", use_column_width=True)
            
            # Update metrics
            metrics_placeholder.markdown(f"""
            <div class='metric-card'>
                <h4>📊 Mission Statistics</h4>
                <p>Frames Processed: {frame_count}</p>
                <p>Total Threats: {threat_detections}</p>
                <p>Active Sensors: {len(active_sensors)}</p>
                <p>System Status: {'🔴 ALERT' if current_threats > 0 else '🟢 OPERATIONAL'}</p>
                <p>Mission Time: {frame_count // 10}s</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Control frame rate
            time.sleep(0.1)
            
            # Break condition (you can add stop button logic)
            if frame_count > 1000:  # Auto-stop after ~100 seconds
                break
        
        cap.release()

# -----------------------------------------------------
# Main Application
# -----------------------------------------------------
def main():
    create_military_dashboard()

if __name__ == "__main__":
    main()
