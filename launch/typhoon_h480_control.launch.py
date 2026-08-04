#!/usr/bin/env python3

"""
ROS2 Launch file pentru Typhoon H480 Control
Pornește: Control node + Gimbal Controller + Keyboard Controller
"""

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import FindExecutable

def generate_launch_description():
    return LaunchDescription([
        # Offboard Control cu Gimbal
        ExecuteProcess(
            cmd=[FindExecutable(name='python3'), '-u',
                 'src/px4_ros_com/src/examples/offboard_py/OffboardControlWithGimbal.py'],
            output='screen',
            name='offboard_control'
        ),
        
        # Gimbal Controller standalone
        ExecuteProcess(
            cmd=[FindExecutable(name='python3'), '-u',
                 'src/px4_ros_com/src/examples/offboard_py/GimbalControl.py'],
            output='screen',
            name='gimbal_controller'
        ),
        
        # Keyboard Controller (optional)
        ExecuteProcess(
            cmd=[FindExecutable(name='python3'), '-u',
                 'src/px4_ros_com/src/examples/offboard_py/KeyboardController.py'],
            output='screen',
            name='keyboard_controller'
        ),
    ])
