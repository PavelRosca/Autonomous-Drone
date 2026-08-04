# 🎬 PX4 Typhoon H480 - Control Architecture

## 📐 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    HARDWARE LAYER                              │
│  ┌──────────────────┐                 ┌──────────────────┐     │
│  │  PX4 Autopilot  │                 │  Gimbal Motor    │     │
│  │  (Pixhawk)      │◄────MAVLink────►│  (3-axis)        │     │
│  └──────────────────┘                 └──────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                    ┌─ UDP Port 14540 ─┐
                    │   14541, 14542   │
                    │   14560, 14570   │
                    └──────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         PX4 SITL                               │
│              (Gazebo Simulation / Real Flight)                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
                    ┌─ ROS2 Topic Bridge ─┐
                    │   (micrortps_agent)   │
                    └──────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ROS2 DAEMON (ROS2)                        │
│                   (DDS Middleware)                             │
└─────────────────────────────────────────────────────────────────┘
        ▲                    ▲                          ▲
        │                    │                          │
        │                    │                          │
   SUBSCRIBE            SUBSCRIBE              SUBSCRIBE & PUBLISH
        │                    │                          │
        ▼                    ▼                          ▼
┌────────────────┐  ┌──────────────────┐  ┌──────────────────────┐
│  GIMBAL        │  │  KEYBOARD        │  │   OFFBOARD           │
│  CONTROLLER    │  │  CONTROLLER      │  │   CONTROL            │
│  (GimbalCtrl)  │  │  (KeyboardCtrl)  │  │  (OffboardCtrlGimbal)│
├────────────────┤  ├──────────────────┤  ├──────────────────────┤
│ • Pitch        │  │ • Arrow keys     │  │ • Waypoint nav       │
│ • Roll         │  │ • WASD motion    │  │ • Obstacle avoid     │
│ • Yaw          │  │ • Arm/Disarm     │  │ • Person tracking    │
│ • Auto-track   │  │ • Offboard mode  │  │ • Gimbal integration │
│ • Presets      │  │ • Gimbal preset  │  │ • Manual override    │
└────────────────┘  └──────────────────┘  └──────────────────────┘
     │ Publishes         │ Publishes          │ Publishes
     │ gimbal_control    │ gimbal commands    │ vehicle_command
     │                   │ drone_commands     │ trajectory_setpoint
     │                   │                    │
     └─────────┬─────────┴────────────────────┴──► /fmu/in/* topics
               │
               │
               ▼
        ┌────────────────┐
        │ /fmu/in topics │
        │ (to drone)     │
        └────────────────┘
               │
               └──► VehicleCommand
                    OffboardControlMode
                    TrajectorySetpoint
```

---

## 📊 ROS2 Topic Flow

```
INPUT SOURCES
│
├─► /gimbal_control             ──►┐
│   [pitch, roll, yaw]             │
│                                  │
├─► /gimbal_keyboard_command   ──►┤
│   "UP", "DOWN", "CENTER", etc   │
│                                  ├──► OffboardControlWithGimbal
├─► /drone_keyboard_command    ──►│    • Validates inputs
│   [vx, vy, vz, yaw_rate]        │    • Integrates all sources
│                                  │    • Generates commands
├─► /clicked_waypoints         ──►│
│   [x1, y1, z1, x2, y2, z2, ...]│
│                                  │
└─► /person_position           ──►┘
    "person: left|right|center"

OUTPUT COMMANDS
│
├─► /fmu/in/vehicle_command ─────────► PX4
│   (arm, disarm, offboard, gimbal)      │
│                                        ├──► Vehicle Motion
├─► /fmu/in/offboard_control_mode ────►  │    Gimbal Control
│   (activate offboard velocity mode)    │
│                                        │
└─► /fmu/in/trajectory_setpoint ───────►┘
    (position or velocity setpoints)

TELEMETRY FEEDBACK
│
├─ /fmu/out/vehicle_local_position ◄─── PX4 (position, velocity)
├─ /fmu/out/vehicle_status         ◄─── PX4 (armed, mode, battery)
└─ /gazebo_ros_head_rplidar_controller/out ◄─── LIDAR (obstacle data)
```

---

## 🔄 Control Flow Sequence

### Scenario: Manual Flight with Gimbal Control

```
┌──────────────────────────────────────────────────────────────────┐
│                      HUMAN OPERATOR                              │
│                   (Keyboard Input)                               │
└──────────────┬───────────────────────────────────────────────────┘
               │ [Presses T]
               ▼
        ┌──────────────┐
        │ KeyboardCtrl │
        │ publishes:   │
        │ "ARM"        │
        └──────┬───────┘
               │
               ▼
    ┌───────────────────────────┐
    │ OffboardControlWithGimbal │
    │ receives ARM command      │
    └──────┬────────────────────┘
           │
           ▼
    ┌──────────────────────────────┐
    │ publish VehicleCommand       │
    │ VEHICLE_CMD_ARM_DISARM       │
    └──────┬───────────────────────┘
           │
           ▼
    ┌────────────────────┐
    │ /fmu/in/vehicle_  │
    │ command ──────────►  PX4 ──► Motoare pornesc
    └────────────────────┘
    
            [Presses O]
               │
               ▼
    ┌──────────────────────────────┐
    │ KeyboardCtrl publishes:      │
    │ "OFFBOARD"                   │
    └──────┬───────────────────────┘
           │
           ▼
    ┌──────────────────────────────┐
    │ OffboardControlWithGimbal    │
    │ publish OffboardControlMode  │
    │ publish vehicle_command      │
    │ DO_SET_MODE to OFFBOARD      │
    └──────┬───────────────────────┘
           │
           ▼
    /fmu/in/offboard_control_mode ──► PX4 ──► Manual control active
    
    
            [Presses Arrow Up]
               │
               ▼
    ┌──────────────────────────────┐
    │ KeyboardCtrl publishes:      │
    │ /gimbal_keyboard_command:    │
    │ "UP"                         │
    └──────┬───────────────────────┘
           │
           ▼
    ┌──────────────────────────────┐
    │ GimbalController handles UP  │
    │ gimbal_pitch += 5 degrees    │
    │ sends new gimbal_control     │
    └──────┬───────────────────────┘
           │
           ▼
    ┌──────────────────────────────┐
    │ OffboardControlWithGimbal    │
    │ calls send_gimbal_command()  │
    │ pitch = -40 degrees          │
    └──────┬───────────────────────┘
           │
           ▼
    publish VehicleCommand:
    • command = 205 (MOUNT_CONTROL)
    • param1 = -40 (pitch)
    • param2 = 0 (roll)
    │
    ▼
    /fmu/in/vehicle_command ──► PX4 ──► Send to gimbal motor
                                         Camera tilts up
```

---

## 🎮 Input Handling Precedence

```
Priority 1: Emergency/Critical Commands
├─ DISARM (immediate)
├─ LAND (immediate)
└─ Emergency gimbal center

Priority 2: Mode Commands
├─ OFFBOARD mode
├─ ARM
└─ Mode switches

Priority 3: Movement Velocity
├─ Keyboard WASD
├─ ROS topic velocity
└─ Waypoint auto-nav

Priority 4: Gimbal Position
├─ Arrow keys (manual)
├─ Auto-tracking (person/object)
└─ Preset positions

Priority 5: Diagnostics/Testing
├─ GimbalTester mode
├─ Logging
└─ Debug output
```

---

## 📈 State Machine - Offboard Control

```
                    ┌──────────────┐
                    │  DISARMED    │
                    │   (Ground)   │
                    └──────┬───────┘
                           │ [T] ARM
                           ▼
                    ┌──────────────┐
                    │   ARMED      │
                    │  (Motors OK) │
                    └──────┬───────┘
                           │ [O] OFFBOARD
                           ▼
                    ┌──────────────────┐
                    │  OFFBOARD MODE   │
                    │  (Manual Control)│
                    └──────┬───────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐      ┌──────────┐      ┌────────── ┐
   │ Manual  │      │ Waypoint │      │ Obstacle │
   │ Control │◄────►│ Tracking │◄────►│ Avoidance│
   │(Keyboard)      │  (Auto)  │      │  (LIDAR) │
   └─────────┘      └──────────┘      └───────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │ [L] LAND
                           ▼
                    ┌──────────────────┐
                    │  LANDING MODE    │
                    │ (Auto descent)   │
                    └──────┬───────────┘
                           │ (Auto disarm)
                           ▼
                    ┌──────────────┐
                    │  DISARMED    │
                    │  (Landed)    │
                    └──────────────┘
```

---

## 🛠️ Component Responsibilities

| Component | Responsibility | Topics |
|-----------|-----------------|--------|
| **GimbalControl.py** | Direct gimbal ctrl | /gimbal_control, /gimbal_keyboard_command |
| **KeyboardController.py** | User input → ROS | /drone_keyboard_command, /drone_string_command |
| **OffboardControl.WithGimbal.py** | Orchestration | All /fmu/in/* (output), All /fmu/out/* (input) |
| **GimbalTester.py** | Quick validation | /fmu/in/vehicle_command (gimbal commands) |
| **GimbalPresets.py** | Reference configs | None (utility module) |

---

## 🚀 Execution Timeline

```
t=0s:  Start offboard_control_with_gimbal.py
       └─► Initialize nodes, publishers, subscribers
       
t=0.1s: Start key

board_controller.py
       └─► Begin listening for keyboard input
       
t=0.2s: Start gimbal_control.py
       └─► Begin gimbal subscription monitoring
       
t=1s:  [User presses T] → Send ARM command
       └─► Motors arm, PWM = ~1100us
       
t=2s:  [User presses O] → Activate OFFBOARD
       └─► Control mode switches to offboard
       
t=2.1s: Timer callback running at 10Hz
        ├─► Check input (keyboard, topics)
        ├─► Publish gimbal command (every 100ms)
        └─► Update trajectory setpoints
        
t=2.5s: [User presses Space] → Vertical velocity +2 m/s
        └─► Drone moves up, gimbal tracks
        
t=2.6s: [User presses ↑] → Gimbal pitch +5°
        └─► Camera tilts up
        
t=5s:   [User presses L] → LAND command
        └─► Start descent, controllers reduce height
        
t=8s:   Drone reaches ground, auto-disarm (PX4 feature)
        └─► System returns to DISARMED state
```

---

## 🔌 ROS Message Types

```
Input Messages:
1. Float32MultiArray
   - /gimbal_control: [pitch°, roll°, yaw°]
   - /drone_keyboard_command: [vx m/s, vy m/s, vz m/s, yaw_rate°/s]
   - /clicked_waypoints: [x1, y1, z1, x2, y2, z2, ...]

2. String
   - /gimbal_keyboard_command: "UP" | "DOWN" | "CENTER" | etc
   - /drone_string_command: "ARM" | "DISARM" | "OFFBOARD" | "LAND"

3. LaserScan
   - /gazebo_ros_head_rplidar_controller/out: LIDAR range data

Output Messages:
1. VehicleCommand (px4_msgs)
   - /fmu/in/vehicle_command: MAVLink commands (param1-7)

2. OffboardControlMode (px4_msgs)
   - /fmu/in/offboard_control_mode: Control mode flags

3. TrajectorySetpoint (px4_msgs)
   - /fmu/in/trajectory_setpoint: Position/velocity setpoints
```

---

## 📡 Communication Protocol

```
PX4 ◄─────────► Pixhawk ◄──────────► PX4 SITL (Gazebo)
                  (UDP)               /fmu/out/* (telemetry)
                                      /fmu/in/*  (commands)
                                           │
                                           │ micrortps_agent
                                           │
                                      ROS2 DDS
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
              GimbalControl         KeyboardController    OffboardControlWithGimbal
```

---

**Remember:** Toate componentele comunică prin ROS2 topics (DDS middleware). Sincronizarea se întîmplă în timer callbacks la 10Hz.
