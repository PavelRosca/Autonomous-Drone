#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import VehicleCommand
from std_msgs.msg import Float32MultiArray, String
from geometry_msgs.msg import Vector3Stamped

class GimbalController(Node):
    """
    Controller pentru gimbal-ul camerei pe drona PX4 Typhoon H480
    Controlează: pitch (tilt up/down), roll (side-to-side), yaw (rotație)
    """
    
    def __init__(self) -> None:
        super().__init__('gimbal_controller')
        
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        
        # Publisher pentru comenzi gimbal
        self.vehicle_command_publisher = self.create_publisher(
            VehicleCommand, '/fmu/in/vehicle_command', qos_profile)
        
        # Subscribers pentru control gimbal
        # Format: [pitch_degrees, roll_degrees, yaw_degrees]
        self.create_subscription(
            Float32MultiArray, '/gimbal_control', self.gimbal_control_callback, qos_profile)
        
        # Pentru control manual prin tasteri
        self.create_subscription(
            String, '/gimbal_keyboard_command', self.keyboard_command_callback, qos_profile)
        
        # Pentru trackare automată (urma obiectelor/personae)
        self.create_subscription(
            Vector3Stamped, '/gimbal_target_position', self.target_position_callback, qos_profile)
        
        # Stare gimbal
        self.gimbal_pitch = 0.0      # -90 (jos) la 0 (față)
        self.gimbal_roll = 0.0       # -45 la 45 (side-to-side)
        self.gimbal_yaw = 0.0        # 0-360 (rotație)
        
        # Viteze de mișcare
        self.pitch_speed = 10.0      # grade/secundă
        self.roll_speed = 5.0        # grade/secundă
        self.yaw_speed = 15.0        # grade/secundă
        
        # Limite gimbal
        self.pitch_min = -90.0
        self.pitch_max = 0.0
        self.roll_min = -45.0
        self.roll_max = 45.0
        
        # Timer pentru actualizare continuă
        self.create_timer(0.1, self.gimbal_update_timer)
        
        self.get_logger().info("Gimbal Controller inițializat pentru Typhoon H480")
    
    def gimbal_control_callback(self, msg):
        """
        Primește valori de control pentru gimbal
        msg.data = [pitch, roll, yaw] în grade
        """
        if len(msg.data) >= 3:
            self.gimbal_pitch = max(self.pitch_min, min(self.pitch_max, float(msg.data[0])))
            self.gimbal_roll = max(self.roll_min, min(self.roll_max, float(msg.data[1])))
            self.gimbal_yaw = float(msg.data[2]) % 360.0
            
            self.get_logger().info(
                f"Gimbal: Pitch={self.gimbal_pitch:.1f}° Roll={self.gimbal_roll:.1f}° Yaw={self.gimbal_yaw:.1f}°")
    
    def keyboard_command_callback(self, msg):
        """
        Comenzi gimbal prin tastatur
        Comenzi: UP, DOWN, LEFT, RIGHT, YAW_LEFT, YAW_RIGHT, CENTER
        """
        cmd = msg.data.strip().upper()
        step = 5.0
        
        if cmd == "UP":
            self.gimbal_pitch = min(self.pitch_max, self.gimbal_pitch + step)
        elif cmd == "DOWN":
            self.gimbal_pitch = max(self.pitch_min, self.gimbal_pitch - step)
        elif cmd == "LEFT":
            self.gimbal_roll = max(self.roll_min, self.gimbal_roll - step)
        elif cmd == "RIGHT":
            self.gimbal_roll = min(self.roll_max, self.gimbal_roll + step)
        elif cmd == "YAW_LEFT":
            self.gimbal_yaw = (self.gimbal_yaw - 10.0) % 360.0
        elif cmd == "YAW_RIGHT":
            self.gimbal_yaw = (self.gimbal_yaw + 10.0) % 360.0
        elif cmd == "CENTER":
            self.gimbal_pitch = -45.0
            self.gimbal_roll = 0.0
            self.gimbal_yaw = 0.0
        elif cmd == "DOWN_FULL":
            self.gimbal_pitch = self.pitch_min  # -90 (vertical jos)
        
        self.get_logger().info(f"Comanda tastatur: {cmd}")
    
    def target_position_callback(self, msg):
        """
        Trackare automată - calculează gimbal angles pentru a viza target
        msg.position = (x, y, z) - poziția țintei în raport cu drona
        """
        x, y, z = msg.vector.x, msg.vector.y, msg.vector.z
        
        # Calculează pitch (tilt vertical)
        # z negativ = jos, deci pitch < 0
        distance_horizontal = math.sqrt(x**2 + y**2)
        if distance_horizontal > 0.1:
            self.gimbal_pitch = -math.degrees(math.atan2(abs(z), distance_horizontal))
        
        # Calculează yaw (rotație orizontală)
        if x != 0 or y != 0:
            self.gimbal_yaw = math.degrees(math.atan2(y, x))
        
        # Nu schimbă roll pentru auto-tracking
        self.gimbal_roll = 0.0
    
    def send_gimbal_command(self, pitch: float, roll: float, yaw: float):
        """
        Trimite comanda de control gimbal la PX4
        Folosește comanda VehicleCommand VEHICLE_CMD_DO_MOUNT_CONTROL (205)
        """
        msg = VehicleCommand()
        msg.command = 205  # VEHICLE_CMD_DO_MOUNT_CONTROL
        
        # Param1: pitch (grade)
        msg.param1 = float(pitch)
        # Param2: roll (grade)
        msg.param2 = float(roll)
        # Param3: yaw (grade)
        msg.param3 = float(yaw)
        # Param4: stabilize (0=roll, 1=tilt, 2=pan)
        msg.param4 = 0.0  # 0 = normal gimbal mode
        # Param5: roll mode (0=auto, 1=manual)
        msg.param5 = 0.0
        # Param6: yaw mode (0=auto, 1=manual)
        msg.param6 = 0.0
        # Param7: Mount mode (0=retracted, 1=neutral, 2=yaw follow, 3=yaw lock)
        msg.param7 = 2.0  # Yaw follow mode
        
        msg.target_system = 1
        msg.target_component = 1
        msg.from_external = True
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        
        self.vehicle_command_publisher.publish(msg)
    
    def gimbal_update_timer(self):
        """Trimite comenzi de update gimbal în mod regulat"""
        self.send_gimbal_command(self.gimbal_pitch, self.gimbal_roll, self.gimbal_yaw)


def main(args=None):
    rclpy.init(args=args)
    gimbal_controller = GimbalController()
    
    try:
        rclpy.spin(gimbal_controller)
    except KeyboardInterrupt:
        pass
    finally:
        gimbal_controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
