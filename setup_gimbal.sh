#!/bin/bash
# Setup script for PX4 Typhoon H480 Gimbal Control
# Run this to prepare everything

set -e  # Exit on any error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  PX4 TYPHOON H480 GIMBAL SETUP - Automated Setup Script   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Workspace paths
WS_ROOT="$HOME/ws_ros2"
PX4_ROOT="$HOME/PX4-Autopilot"
SCRIPT_DIR="$WS_ROOT/src/px4_ros_com/src/examples/offboard_py"

echo -e "${YELLOW}Step 1: Checking workspace paths...${NC}"
if [ ! -d "$WS_ROOT" ]; then
    echo -e "${RED}ERROR: Workspace not found at $WS_ROOT${NC}"
    exit 1
fi

if [ ! -d "$PX4_ROOT" ]; then
    echo -e "${RED}ERROR: PX4 not found at $PX4_ROOT${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Workspace paths OK${NC}"
echo ""

# Install Python dependencies
echo -e "${YELLOW}Step 2: Installing Python dependencies...${NC}"
pip install keyboard ultralytics opencv-python numpy rclpy 2>/dev/null || \
pip3 install keyboard ultralytics opencv-python numpy rclpy

echo -e "${GREEN}✓ Python packages installed${NC}"
echo ""

# Build ROS2
echo -e "${YELLOW}Step 3: Building ROS2 packages...${NC}"
cd "$WS_ROOT"
colcon build 2>/dev/null || {
    echo -e "${RED}Build failed. Check workspace setup.${NC}"
    exit 1
}
echo -e "${GREEN}✓ ROS2 build complete${NC}"
echo ""

# Create symlinks for easy access
echo -e "${YELLOW}Step 4: Creating symlinks for easy access...${NC}"

# Create quick-access scripts in home directory
cat > "$HOME/run_gimbal_control.sh" << 'EOF'
#!/bin/bash
cd ~/ws_ros2
source install/setup.bash
python3 src/px4_ros_com/src/examples/offboard_py/OffboardControlWithGimbal.py
EOF

cat > "$HOME/run_keyboard_controller.sh" << 'EOF'
#!/bin/bash
cd ~/ws_ros2
source install/setup.bash
python3 src/px4_ros_com/src/examples/offboard_py/KeyboardController.py
EOF

cat > "$HOME/test_gimbal.sh" << 'EOF'
#!/bin/bash
cd ~/ws_ros2
source install/setup.bash
python3 src/px4_ros_com/src/examples/offboard_py/GimbalTester.py
EOF

chmod +x "$HOME/run_gimbal_control.sh"
chmod +x "$HOME/run_keyboard_controller.sh"
chmod +x "$HOME/test_gimbal.sh"

echo -e "${GREEN}✓ Symlinks created in home directory${NC}"
echo ""

# Print summary
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ✅ SETUP COMPLETE                             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo -e "${GREEN}Quick Start Commands:${NC}"
echo ""
echo "1. Terminal 1 - Start PX4 SITL:"
echo "   cd ~/PX4-Autopilot && make px4_sitl gazebo-classic"
echo ""
echo "2. Terminal 2 - Start Gimbal Control:"
echo "   ~/run_gimbal_control.sh"
echo "   OR"
echo "   python3 ~/run_gimbal_control.sh"
echo ""
echo "3. Terminal 3 - Start Keyboard Input:"
echo "   ~/run_keyboard_controller.sh"
echo "   OR"  
echo "   python3 ~/run_keyboard_controller.sh"
echo ""
echo -e "${GREEN}Test Command:${NC}"
echo "   ~/test_gimbal.sh"
echo ""

echo -e "${YELLOW}Documentation:${NC}"
echo "  - Quick Start:     cat ~/ws_ros2/QUICKSTART_GIMBAL.txt"
echo "  - Full Guide:      cat ~/ws_ros2/GIMBAL_SOLUTION_SUMMARY.md"
echo "  - Architecture:    cat ~/ws_ros2/ARCHITECTURE_DIAGRAM.md"
echo ""

echo -e "${YELLOW}Default Controls:${NC}"
echo "  Gimbal:  ↑↓←→  (arrow keys)  | C (center) | V (straight down)"
echo "  Drone:   W/A/S/D (move)      | Space/X (up/down) | Q/E (yaw)"
echo "  Control: T (arm) | O (offboard) | L (land) | Y (disarm)"
echo ""

echo -e "${GREEN}Ready to fly! 🚀${NC}"
echo ""
