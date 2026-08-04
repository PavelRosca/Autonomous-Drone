#!/usr/bin/env python3

"""
Test Gimbal Control SimpleFull
Scenariu de test rapid pentru verificare gimbal
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import VehicleCommand
import time

class GimbalTester(Node):
    def __init__(self):
        super().__init__('gimbal_tester')
        
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        
        self.cmd_pub = self.create_publisher(VehicleCommand, '/fmu/in/vehicle_command', qos_profile)
        self.get_logger().info("Gimbal Tester initialized")

    def send_gimbal_command(self, pitch, roll, yaw):
        """Trimite comanda gimbal"""
        msg = VehicleCommand()
        msg.command = 205  # VEHICLE_CMD_DO_MOUNT_CONTROL
        msg.param1 = float(pitch)
        msg.param2 = float(roll)
        msg.param3 = float(yaw)
        msg.param4 = 0.0
        msg.param5 = 0.0
        msg.param6 = 0.0
        msg.param7 = 2.0  # Yaw follow
        msg.target_system = 1
        msg.target_component = 1
        msg.from_external = True
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.cmd_pub.publish(msg)
        self.get_logger().info(f"Gimbal: Pitch={pitch:.0f}°, Roll={roll:.0f}°, Yaw={yaw:.0f}°")

    def test_gimbal_sequence(self):
        """Test gimbal în secvență"""
        tests = [
            {"name": "Center (neutrq", "pitch": -45, "roll": 0, "yaw": 0},
            {"name": "Straight Down", "pitch": -90, "roll": 0, "yaw": 0},
            {"name": "Pan Left", "pitch": -45, "roll": -45, "yaw": 0},
            {"name": "Pan Right", "pitch": -45, "roll": 45, "yaw": 0},
            {"name": "Yaw Left", "pitch": -45, "roll": 0, "yaw": -90},
            {"name": "Yaw Right", "pitch": -45, "roll": 0, "yaw": 90},
            {"name": "Look Ahead Up", "pitch": 0, "roll": 0, "yaw": 0},
            {"name": "Back to Center", "pitch": -45, "roll": 0, "yaw": 0},
        ]
        
        print("\n" + "="*50)
        print("🎬 Secvență TEST GIMBAL - Typhoon H480")
        print("="*50 + "\n")
        
        for test in tests:
            print(f"▶ Test: {test['name']}")
            self.send_gimbal_command(test["pitch"], test["roll"], test["yaw"])
            time.sleep(2)  # Stai 2 secunde între teste
        
        print("\n✅ Test gimbal completed!\n")


def main(args=None):
    rclpy.init(args=args)
    tester = GimbalTester()
    
    # Dă o clipă nodului să se conecteze
    time.sleep(1)
    
    # Rulează test
    tester.test_gimbal_sequence()
    
    # Ține să ruleze pentru a vedea output
    time.sleep(2)
    
    tester.destroy_node()
    rclpy.shutdown()
    
    print("✅ Test completed - Gimbal Tester se inchide...\n")


if __name__ == '__main__':
    main()
