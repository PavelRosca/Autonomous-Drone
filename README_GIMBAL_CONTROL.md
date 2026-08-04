# 🎬 **PX4 Typhoon H480 - Complete Gimbal Control Solution**

> **Status**: ✅ **PRODUCTION READY** | Version 1.0 | Feb 5, 2025

---

## 🎯 What You've Got

A **complete, production-ready solution** for controlling a **PX4 Typhoon H480** drone with:
- ✈️ **Full drone control** (movement, altitude, rotation)
- 📷 **3-axis gimbal camera control** (pitch/tilt, roll/pan, yaw/rotate)
- 🎮 **Keyboard interface** for manual operation
- 🗺️ **Autonomous waypoint navigation** with obstacle avoidance
- 👤 **Person detection & tracking** with automatic gimbal control
- 🧪 **Testing tools** for quick validation

---

## 📦 **What's Included**

### 🔧 **5 Core Python Scripts**

| Script | Purpose | Status |
|--------|---------|--------|
| [OffboardControlWithGimbal.py](src/px4_ros_com/src/examples/offboard_py/OffboardControlWithGimbal.py) | Main control engine | ✅ Executable |
| [GimbalControl.py](src/px4_ros_com/src/examples/offboard_py/GimbalControl.py) | Gimbal controller | ✅ Executable |
| [KeyboardController.py](src/px4_ros_com/src/examples/offboard_py/KeyboardController.py) | Keyboard input handler | ✅ Executable |
| [GimbalTester.py](src/px4_ros_com/src/examples/offboard_py/GimbalTester.py) | Quick test tool | ✅ Executable |
| [GimbalPresets.py](src/px4_ros_com/src/examples/offboard_py/GimbalPresets.py) | Preset configurations | ✅ Reference |

### 📚 **4 Documentation Guides**

| Document | Content |
|----------|---------|
| [QUICKSTART_GIMBAL.txt](QUICKSTART_GIMBAL.txt) | 5-minute setup & test |
| [GIMBAL_SOLUTION_SUMMARY.md](GIMBAL_SOLUTION_SUMMARY.md) | Complete reference |
| [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) | System design & flow |
| [setup_gimbal.sh](setup_gimbal.sh) | Automated setup script |

### 📋 **Supporting Files**

| File | Purpose |
|------|---------|
| [requirements.txt](requirements.txt) | Python dependencies |
| [launch/typhoon_h480_control.launch.py](launch/typhoon_h480_control.launch.py) | ROS2 launch file |

---

## 🚀 **Quick Start (5 Minutes)**

### **Step 1: One-Time Setup**
```bash
cd ~/ws_ros2
bash setup_gimbal.sh
```

### **Step 2: Run 3 Terminals**

**Terminal 1** - PX4 Simulator:
```bash
cd ~/PX4-Autopilot
make px4_sitl gazebo-classic
# Wait for "simulation started"
```

**Terminal 2** - Control Engine:
```bash
~/run_gimbal_control.sh
# Or: python3 ~/ws_ros2/src/px4_ros_com/src/examples/offboard_py/OffboardControlWithGimbal.py
```

**Terminal 3** - Keyboard Controller:
```bash
~/run_keyboard_controller.sh
# Or: python3 ~/ws_ros2/src/px4_ros_com/src/examples/offboard_py/KeyboardController.py
```

### **Step 3: Fly!**

```
🎮 Keyboard Controls:
  [T] Arm
  [O] Offboard Mode
  [Space] Up / [X] Down
  [W/A/S/D] Forward/Left/Back/Right
  [↑↓←→] Gimbal Tilt/Pan (Camera)
  [C] Center Gimbal / [V] Straight Down
  [L] Land / [Y] Disarm
  [ESC] Exit
```

Done! You're controlling the drone 🎉

---

## 📖 **Detailed Usage**

### **Three Control Modes**

#### **1️⃣ Manual Control (Keyboard)** ✅ Recommended
```bash
KeyboardController.py provides:
- Arrow keys for gimbal movement
- WASD for drone movement  
- Single-key commands (T=arm, L=land)
- Real-time feedback
```

#### **2️⃣ ROS Topics Control** (Programmatic)
```bash
# Set gimbal angle
ros2 topic pub /gimbal_control std_msgs/Float32MultiArray '{data: [-45, 0, 0]}'

# Drone commands
ros2 topic pub /drone_string_command std_msgs/String '{data: "OFFBOARD"}'

# Velocity control
ros2 topic pub /drone_keyboard_command std_msgs/Float32MultiArray '{data: [1.0, 0, 0, 0]}'
```

#### **3️⃣ Autonomous Navigation**
```bash
# Send waypoints → drone navigates automatically
ros2 topic pub /clicked_waypoints std_msgs/Float32MultiArray \
  '{data: [0, 0, -5, 10, 10, -5, 20, 0, -5]}'
```

---

## 🎬 **Gimbal Angles Reference**

```
PITCH (Vertical Tilt):
  0°    → Camera looking straight ahead (forward)
  -45°  → 45° down (neutral, recommended)
  -90°  → Straight down (nadir, for photos)

ROLL (Horizontal Pan):
  0°    → Centered
  ±45°  → Maximum side tilt

YAW (Rotation):
  0°    → Forward
  90°   → Right
  180°  → Backward
  270°  → Left
```

### **Preset Angles for Common Scenarios**

| Preset | Pitch | Roll | Yaw | Use Case |
|--------|-------|------|-----|----------|
| LOOK_AHEAD | 0° | 0° | 0° | Forward view |
| CENTER | -45° | 0° | 0° | Neutral position |
| STRAIGHT_DOWN | -90° | 0° | 0° | Aerial photography |
| SURVEILLANCE | -60° | 0° | 180° | Rear view |
| PERSON_TRACKING | -45° | 0° | 0° | Ground tracking |
| LANDING | -75° | 0° | 0° | Landing operations |

```bash
# Use presets
python3 GimbalPresets.py  # List all
python3 GimbalPresets.py STRAIGHT_DOWN  # Load specific
```

---

## 🔍 **Topic Map**

```
INPUTS:
  /gimbal_control [pitch, roll, yaw]
  /gimbal_keyboard_command "UP"/"DOWN"/etc
  /drone_keyboard_command [vx, vy, vz, yaw_rate]
  /drone_string_command "ARM"/"DISARM"/etc
  /clicked_waypoints [x1, y1, z1, ...]

OUTPUTS:
  /fmu/in/vehicle_command (to drone)
  /fmu/in/trajectory_setpoint (position/velocity)
  /fmu/in/offboard_control_mode (control flags)
  
SENSING:
  /fmu/out/vehicle_local_position (drone position)
  /fmu/out/vehicle_status (drone state)
  /gazebo_ros_head_rplidar_controller/out (LIDAR)
```

---

## 🧪 **Testing & Debugging**

### **Quick Test Gimbal**
```bash
python3 ~/ws_ros2/src/px4_ros_com/src/examples/offboard_py/GimbalTester.py
# Runs 8-step gimbal test sequence automatically
```

### **Monitor Topics**
```bash
# Watch gimbal commands
ros2 topic echo /gimbal_control

# Watch drone position
ros2 topic echo /fmu/out/vehicle_local_position

# List all active topics
ros2 topic list

# Check node status
ros2 node list
```

### **Troubleshooting**

| Problem | Solution |
|---------|----------|
| Gimbal not moving | Check drone in offboard mode first (press O) |
| Keyboard not responsive | Run with sudo: `sudo python3 KeyboardController.py` |
| No topics appearing | Check micrortps_agent running, restart if needed |
| ROS connection failing | Verify ROS2 daemon: `ros2 daemon status` |

---

## ⚙️ **Configuration**

Edit `OffboardControlWithGimbal.py` to adjust:

```python
# Drone speeds
speed = 3.0                    # m/s forward speed
zspeed = 3.0                   # m/s vertical speed

# Gimbal speeds
pitch_speed = 10.0             # degrees/sec
roll_speed = 5.0
yaw_speed = 15.0

# Navigation
waypoint_tolerance = 2.0       # meters to waypoint
obstacle_distance_threshold = 5.0  # LIDAR detection range
```

---

## 🏗️ **Architecture Overview**

```
┌─────────────────────────────────────────────────┐
│         PX4 Autopilot (Pixhawk)                │
│  (Could be SITL in Gazebo or Real Hardware)    │
└────────────────────┬────────────────────────────┘
                     │ MAVLink commands via UDP
                     │
              ┌──────▼─────────────────────────┐
              │   micrortps_agent Bridge       │
              │   (ROS2 ↔ PX4 Gateway)        │
              └──────┬─────────────────────────┘
                     │
              /fmu/in/* /fmu/out/*
                     │
    ┌────────────────┼────────────────┐
    │                │                │
    ▼                ▼                ▼
  GIMBAL        KEYBOARD         OFFBOARD
  CONTROL       CONTROLLER       CONTROL
    │                │                │
    └────────────────┼────────────────┘
                     │
              ┌──────▼─────────────┐
              │    ROS2 DDS       │
              │   (middleware)    │
              └───────────────────┘
```

---

## 📊 **System Requirements**

### **Software**
- ROS2 (Humble or later)
- Python 3.9+
- PX4 Autopilot v1.14+
- Gazebo (for SITL simulation)

### **Hardware**
- PC with 4GB+ RAM
- Linux (Ubuntu 20.04+ recommended)
- For real drone: Compatible Pixhawk + Gimbal

### **Python Packages**
```bash
keyboard  # Keyboard input
numpy     # Numerical operations
rclpy     # ROS2 Python client
# Optional:
ultralytics  # YOLO detection
opencv-python  # Video processing
```

---

## 🎓 **Learning Path**

1. **Start Here** → [QUICKSTART_GIMBAL.txt](QUICKSTART_GIMBAL.txt)
2. **Understand Architecture** → [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)
3. **Full Reference** → [GIMBAL_SOLUTION_SUMMARY.md](GIMBAL_SOLUTION_SUMMARY.md)
4. **Advanced Setup** → Individual script documentation

---

## 🔗 **File Locations**

```
~/ws_ros2/
├── QUICKSTART_GIMBAL.txt           ← Start here!
├── GIMBAL_SOLUTION_SUMMARY.md      ← Full guide
├── ARCHITECTURE_DIAGRAM.md         ← System design
├── README_GIMBAL_CONTROL.md        ← This file
├── setup_gimbal.sh                 ← Auto setup
├── requirements.txt                ← Dependencies
├── run_gimbal_control.sh           ← Quick run script
├── run_keyboard_controller.sh       ← Keyboard input
└── src/px4_ros_com/src/examples/offboard_py/
    ├── OffboardControlWithGimbal.py
    ├── GimbalControl.py
    ├── KeyboardController.py
    ├── GimbalTester.py
    ├── GimbalPresets.py
    └── GIMBAL_SETUP_README.md
```

---

## 💡 **Pro Tips**

✅ **Always test in SITL first** before flying real drone  
✅ **Monitor CPU/telemetry** on flight computer  
✅ **Keep gimbal calibrated** before operations  
✅ **Log flights** for debugging and improvement  
✅ **Use presets** for consistent gimbal positions  
✅ **Keyboard needs elevated privileges** on Linux (sudo)  
✅ **Check battery** before autonomous missions  

---

## 🐛 **Common Issues & Fixes**

### Issue: "Module keyboard not found"
```bash
pip install keyboard --upgrade
# If on Linux, may need: sudo apt-get install linux-headers-generic
```

### Issue: Gimbal commands not working
```bash
# 1. Verify drone is in OFFBOARD mode
ros2 topic pub /drone_string_command std_msgs/String '{data: "OFFBOARD"}'

# 2. Check gimbal message format
ros2 topic echo /gimbal_control

# 3. Verify command reaching PX4
ros2 topic echo /fmu/in/vehicle_command
```

### Issue: Can't connect to ROS
```bash
# Check ROS daemon
ros2 daemon status
ros2 daemon stop
ros2 daemon start

# Check scope
ros2 topic list
ros2 node list
```

---

## 📞 **Support Resources**

- **PX4 Docs**: https://docs.px4.io
- **ROS2 Docs**: https://docs.ros.org
- **MAVLink Protocol**: https://mavlink.io
- **Gazebo Simulator**: https://gazebosim.org

---

## 📝 **Version History**

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Feb 5, 2025 | Initial release - Full gimbal + drone control |

---

## 🎉 **You're Ready!**

Everything is set up. Pick a terminal and start flying!

```bash
# Option 1: Run setup script
bash ~/ws_ros2/setup_gimbal.sh

# Option 2: Manual start
~/run_gimbal_control.sh     # Terminal 2
~/run_keyboard_controller.sh # Terminal 3

# Option 3: Quick test
~/test_gimbal.sh
```

**Happy flying! 🚀📷**

---

**Last Updated**: Feb 5, 2025  
**Status**: ✅ Production Ready  
**License**: BSD 3-Clause (PX4 Autopilot)
