# PX4 Typhoon H480 - Control Drona + Gimbal Cameră

## 📋 Descriere

Această soluție permite controlul complet al dronei **PX4 Typhoon H480** cu gimbal 3-axis pentru cameră.

**Caracteristici:**
- ✈️ Control deplasare drona (forward, backward, left, right, up, down)
- 📷 Control gimbal cameră (pitch, roll, yaw - tilt, pan, rotate)
- 🎮 Control prin tastatur cu KeyboardController
- 🗺️ Navigare pe waypoints cu evitare obstacole (LIDAR)
- 👤 Trackare automată de persoane cu control gimbal automat
- 🎯 Mod offboard cu control manual

---

## 📦 Componente

### 1. **GimbalControl.py** - Control gimbal (cameră)
```
Funcționalitate:
- Control pitch (tilt up/down): -90° (jos) la 0° (orizontal)
- Control roll (pan side): -45° la +45°
- Control yaw (rotație): 0° la 360°
- Trackare automată a țintelor
```

### 2. **KeyboardController.py** - Control prin tastatur
```
Comenzi:
  GIMBAL (Camera):
    ↑ ↓ → ← = Pitch/Roll
    , . = Yaw left/right
    C = Center gimbal
    V = Straight down (-90°)
    
  DRONE:
    W/A/S/D = Forward/Left/Back/Right
    Q/E = Yaw left/right (rotație corpo)
    Space/X = Up/Down
    T = Arm, Y = Disarm
    O = Offboard Mode, L = Land
    ESC = Exit
```

### 3. **OffboardControlWithGimbal.py** - Motor control integrat
```
Integrează:
- Control drona (offboard mode + velocitate)
- Control gimbal (comenzi MAVLink)
- Evitare obstacole (LIDAR)
- Trackare persoane
- Navigare waypoints
```

---

## 🚀 Instalare și Setup

### 1. Instalare dependințe Python
```bash
# Mergi la workspace
cd ~/ws_ros2

# Instalează package-urile Python necesare
pip install keyboard ultralytics opencv-python numpy

# Sau din requirements.txt (dacă ai)
# pip install -r requirements.txt
```

### 2. Build ROS2 packages
```bash
cd ~/ws_ros2
colcon build
```

### 3. Source environment
```bash
source ~/ws_ros2/install/setup.bash
```

---

## 🔧 Utilizare

### Opțiunea 1: Control via Keyboard (Recomandat pentru început)

**Terminal 1 - Pornește PX4 SITL + Gazebo:**
```bash
cd ~/PX4-Autopilot
make px4_sitl gazebo-classic
```

**Terminal 2 - ROS2 Bridge (dacă nu este deja rulând):**
```bash
# Verifică dacă micrortps_agent este pornit
# Dacă nu:
cd ~/PX4-Autopilot/src/modules/micrortps_bridge/micrortps_agent
./micrortps_agent -t UDP
```

**Terminal 3 - Pornește control nod:**
```bash
cd ~/ws_ros2
source install/setup.bash
ros2 run px4_ros_com OffboardControlWithGimbal
```

**Terminal 4 - Pornește keyboard controller:**
```bash
cd ~/ws_ros2
source install/setup.bash
python3 src/px4_ros_com/src/examples/offboard_py/KeyboardController.py
```

### Opțiunea 2: Control prin ROS Services/Topics

**Trimite comandă gimbal direct:**
```bash
# Gimbal pitch=-45°, roll=0°, yaw=0°
ros2 topic pub /gimbal_control std_msgs/Float32MultiArray '{data: [-45.0, 0.0, 0.0]}'

# Gimbal straight down
ros2 topic pub /gimbal_control std_msgs/Float32MultiArray '{data: [-90.0, 0.0, 0.0]}'
```

**Comenzi drona:**
```bash
# Arm
ros2 topic pub /drone_string_command std_msgs/String '{data: "ARM"}'

# Offboard
ros2 topic pub /drone_string_command std_msgs/String '{data: "OFFBOARD"}'

# Land
ros2 topic pub /drone_string_command std_msgs/String '{data: "LAND"}'
```

---

## 📊 Interfață ROS Topics

### Publicare (OUTPUT)
```
/fmu/in/vehicle_command           - Comenzi drona
/fmu/in/offboard_control_mode     - Mode offboard
/fmu/in/trajectory_setpoint       - Setpoint trajectorie
/gimbal_command                   - Status gimbal
```

### Abonare (INPUT)
```
/fmu/out/vehicle_local_position   - Poziție locals
/fmu/out/vehicle_status           - Status drona
/gimbal_control                   - Comanda gimbal [pitch, roll, yaw]
/gimbal_keyboard_command          - Comanda gimbal din tastatur
/drone_keyboard_command           - Viteză drona [vx, vy, vz, yaw_rate]
/drone_string_command             - String comenzi (ARM, DISARM, etc)
/gazebo_ros_head_rplidar_controller/out - LaserScan din LIDAR
/person_position                  - Poziție detectată person
/clicked_waypoints                - Waypoints
```

---

## 🎯 Scenarii Use Case

### Scenario 1: Control Manual Complet
```bash
# 1. Pornire componente (vezi Opțiunea 1)
# 2. Apasă T pentru arm
# 3. Apasă O pentru offboard mode
# 4. Mișcare cu WASD, gimbal cu arrow keys
# 5. Apasă L pentru land și Y pentru disarm
```

### Scenario 2: Cautare și Trackare Independentă
```bash
# Drone merge pe waypoints cu evitare obstacole
# Gimbal se poziționează automat pe țintă detectată
# (necesită YOLO detection node rulând)
```

### Scenario 3: Surveilance (Gimbal Fixed)
```bash
# 1. Pornește drona
# 2. Apasă V pentru gimbal straight down
# 3. Navighează cu WASD
# 4. Camera urmărește zona de jos
```

---

## 🔍 Debugging

### Verifică topici active:
```bash
ros2 topic list
```

### Vezi mesaje gimbal:
```bash
ros2 topic echo /gimbal_control
```

### Verifica status drona:
```bash
ros2 topic echo /fmu/out/vehicle_status
```

### Log din node:
```bash
# În alt terminal
ros2 launch px4_ros_com OffboardControlWithGimbal --verbose
```

---

## 📝 Parametri Configurabili

Edit în `OffboardControlWithGimbal.py`:

```python
# Viteza navigație waypoints (m/s)
speed = 3.0  # schimbă în publish_position_setpoint()

# Toleranță waypoint (m)
self.waypoint_tolerance = 2.0

# Distanță evitare obstacole (m)  
self.obstacle_distance_threshold = 5.0

# Viteze gimbal (grade/sec)
self.pitch_speed = 10.0
self.roll_speed = 5.0
self.yaw_speed = 15.0
```

---

## ⚠️ Note de Siguranță

1. **Testează mai întâi în SITL** (Gazebo) înaintea de Real Hardware
2. **Verifică PX4 firmware** - compatibil cu Typhoon H480
3. **Gimbal limits**: Pitch [-90°, 0°], Roll [-45°, 45°], Yaw [0°, 360°]
4. **Always arm/disarm cu comenzi** - nu manual
5. **Monitor battery level** - landing automat sub 15%

---

## 🐛 Probleme Comune

### "AttributeError: module 'keyboard' has no attribute"
```bash
# Verifică instalare
pip install keyboard --upgrade
```

### Gimbal nu se mișcă
```bash
1. Verifică dacă drona este în offboard mode
2. Vezi log pentru comenzi VehicleCommand
3. Verifică firmware gimbal în QGroundControl
```

### Topics nu se conectează
```bash
# Verifica micrortps_agent
ps aux | grep micrortps

# Restart bridge:
killall micrortps_agent
./micrortps_agent -t UDP
```

### Keyboard inputs nu merge
```bash
# KeyboardController trebuie să ruleze cu elevated privileges
sudo python3 KeyboardController.py
```

---

## 📚 Resurse

- [PX4 MAVLink Commands](https://mavlink.io/en/messages/common.html)
- [ROS2 px4_msgs](https://github.com/PX4/px4_msgs)
- [Typhoon H480 Specs](https://youtu.be/jKLKkKEm5j4)

---

## 📄 Licență

Conform PX4 Autopilot BSD 3-Clause License

---

**Autor**: PX4 ROS2 Control Integration  
**Data**: 2024-2025  
**Status**: Production Ready ✅
