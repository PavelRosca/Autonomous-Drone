#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String
import keyboard
import threading
import time

class DroneGimbalKeyboardController(Node):
    """
    Controller cu tastatur pentru drona PX4 și gimbal
    
    Comenzi drona:
      WASD - mișcare (W=sus, S=jos, A=stânga, D=dreapta)
      Q/E - yaw drona (Q=stânga, E=dreapta)
      T - armare, Y - dezarmare
      O - offboard mode, L - land
      
    Comenzi gimbal:
      Arrow Up/Down - pitch gimbal (tilt up/down)
      Arrow Left/Right - roll gimbal (tilt stânga/dreapta)
      , / . - yaw gimbal (rotație)
      C - center gimbal
      V - gimbal straight down
    """
    
    def __init__(self):
        super().__init__('keyboard_controller')
        
        # Publishers
        self.gimbal_control_pub = self.create_publisher(Float32MultiArray, '/gimbal_control', 10)
        self.gimbal_keyboard_pub = self.create_publisher(String, '/gimbal_keyboard_command', 10)
        self.drone_command_pub = self.create_publisher(Float32MultiArray, '/drone_keyboard_command', 10)
        
        # Stare
        self.gimbal_pitch = -45.0
        self.gimbal_roll = 0.0
        self.gimbal_yaw = 0.0
        
        self.get_logger().info("Keyboard Controller started")
        self.get_logger().info("Arrow keys = gimbal tilt, , / . = gimbal yaw, C = center gimbal, V = straight down")
    
    def send_gimbal_command(self, pitch, roll, yaw):
        """Trimite comanda gimbal"""
        msg = Float32MultiArray()
        msg.data = [float(pitch), float(roll), float(yaw)]
        self.gimbal_control_pub.publish(msg)
        self.gimbal_pitch = pitch
        self.gimbal_roll = roll
        self.gimbal_yaw = yaw
    
    def send_keyboard_gimbal_command(self, cmd):
        """Trimite comanda gimbal prin tastatur"""
        msg = String()
        msg.data = cmd
        self.gimbal_keyboard_pub.publish(msg)
    
    def send_drone_command(self, vx, vy, vz, yaw_rate):
        """Trimite comanda drona"""
        msg = Float32MultiArray()
        msg.data = [float(vx), float(vy), float(vz), float(yaw_rate)]
        self.drone_command_pub.publish(msg)
    
    def run_keyboard_listener(self):
        """Ascultă inputul tastaturi"""
        print("\n=== PX4 Typhoon H480 Control ===")
        print("\n Gimbal Control (Camera):")
        print("  ↑ ↓ → ← = Pitch/Roll")
        print("  , . = Yaw left/right")
        print("  C = Center gimbal")
        print("  V = Straight down")
        print("\n Drone Control:")
        print("  W/A/S/D = Forward/Left/Back/Right")
        print("  Q/E = Yaw left/right")
        print("  Space/X = Up/Down")
        print("  T = Arm, Y = Disarm")
        print("  O = Offboard, L = Land")
        print("  ESC = Exit\n")
        
        step = 5
        
        while True:
            try:
                # Gimbal control
                if keyboard.is_pressed('up'):
                    self.send_keyboard_gimbal_command("UP")
                    time.sleep(0.1)
                
                elif keyboard.is_pressed('down'):
                    self.send_keyboard_gimbal_command("DOWN")
                    time.sleep(0.1)
                
                elif keyboard.is_pressed('left'):
                    self.send_keyboard_gimbal_command("LEFT")
                    time.sleep(0.1)
                
                elif keyboard.is_pressed('right'):
                    self.send_keyboard_gimbal_command("RIGHT")
                    time.sleep(0.1)
                
                elif keyboard.is_pressed(','):
                    self.send_keyboard_gimbal_command("YAW_LEFT")
                    time.sleep(0.1)
                
                elif keyboard.is_pressed('.'):
                    self.send_keyboard_gimbal_command("YAW_RIGHT")
                    time.sleep(0.1)
                
                elif keyboard.is_pressed('c'):
                    self.send_keyboard_gimbal_command("CENTER")
                    self.get_logger().info("Gimbal centered")
                    time.sleep(0.3)
                
                elif keyboard.is_pressed('v'):
                    self.send_keyboard_gimbal_command("DOWN_FULL")
                    self.get_logger().info("Gimbal pointed straight down")
                    time.sleep(0.3)
                
                # Drone movement
                vx = vy = vz = yaw_rate = 0.0
                
                if keyboard.is_pressed('w'):
                    vx = 2.0  # Forward
                if keyboard.is_pressed('s'):
                    vx = -2.0  # Backward
                if keyboard.is_pressed('a'):
                    vy = -2.0  # Left
                if keyboard.is_pressed('d'):
                    vy = 2.0  # Right
                if keyboard.is_pressed('space'):
                    vz = 2.0  # Up
                if keyboard.is_pressed('x'):
                    vz = -2.0  # Down
                if keyboard.is_pressed('q'):
                    yaw_rate = -20.0  # Rotate left
                if keyboard.is_pressed('e'):
                    yaw_rate = 20.0  # Rotate right
                
                if vx != 0 or vy != 0 or vz != 0 or yaw_rate != 0:
                    self.send_drone_command(vx, vy, vz, yaw_rate)
                
                # Drone commands
                if keyboard.is_pressed('t'):
                    self.get_logger().info("ARM command sent")
                    cmd = String()
                    cmd.data = "ARM"
                    self.drone_command_pub.publish(cmd)
                    time.sleep(0.5)
                
                elif keyboard.is_pressed('y'):
                    self.get_logger().info("DISARM command sent")
                    cmd = String()
                    cmd.data = "DISARM"
                    self.drone_command_pub.publish(cmd)
                    time.sleep(0.5)
                
                elif keyboard.is_pressed('o'):
                    self.get_logger().info("OFFBOARD mode requested")
                    cmd = String()
                    cmd.data = "OFFBOARD"
                    self.drone_command_pub.publish(cmd)
                    time.sleep(0.5)
                
                elif keyboard.is_pressed('l'):
                    self.get_logger().info("LAND command sent")
                    cmd = String()
                    cmd.data = "LAND"
                    self.drone_command_pub.publish(cmd)
                    time.sleep(0.5)
                
                elif keyboard.is_pressed('esc'):
                    self.get_logger().info("Exiting...")
                    break
                
                time.sleep(0.05)
            
            except Exception as e:
                self.get_logger().error(f"Error: {e}")
                time.sleep(0.1)


def main(args=None):
    rclpy.init(args=args)
    controller = DroneGimbalKeyboardController()
    
    # Rulează listener-ul în thread-ul principal
    try:
        controller.run_keyboard_listener()
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
