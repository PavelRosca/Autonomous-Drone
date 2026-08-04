#!/usr/bin/env python3

"""
Gimbal Presets - Predefined camera positions pentru Typhoon H480
Upload fiecare preset și stochează-l pe drona
"""

class GimbalPresets:
    """Colecție de preset-uri gimbal pentru scenarii comune"""
    
    # Format: {"name": "Preset Name", "pitch": degrees, "roll": degrees, "yaw": degrees}
    
    PRESETS = {
        # Camera straight ahead
        "LOOK_AHEAD": {
            "name": "Look Ahead (Camera Forward)",
            "pitch": 0.0,
            "roll": 0.0,
            "yaw": 0.0,
            "description": "Camera Looking horizontally forward"
        },
        
        # Camera center (neutral)
        "CENTER": {
            "name": "Center Neutral",
            "pitch": -45.0,
            "roll": 0.0,
            "yaw": 0.0,
            "description": "Camera at 45 degrees down, centered"
        },
        
        # Camera straight down (nadir)
        "STRAIGHT_DOWN": {
            "name": "Straight Down (Nadir)",
            "pitch": -90.0,
            "roll": 0.0,
            "yaw": 0.0,
            "description": "Camera pointing straight down - perfect for aerial photography"
        },
        
        # Camera down-left
        "DOWN_LEFT": {
            "name": "Down-Left",
            "pitch": -90.0,
            "roll": -45.0,
            "yaw": 0.0,
            "description": "Tilted down and to the left"
        },
        
        # Camera down-right
        "DOWN_RIGHT": {
            "name": "Down-Right",
            "pitch": -90.0,
            "roll": 45.0,
            "yaw": 0.0,
            "description": "Tilted down and to the right"
        },
        
        # Surveillance - looking down-rear
        "SURVEILLANCE": {
            "name": "Surveillance (Rear)",
            "pitch": -60.0,
            "roll": 0.0,
            "yaw": 180.0,
            "description": "Looking down and backwards"
        },
        
        # Tracking mode - following ahead
        "TRACKING": {
            "name": "Tracking (Following)",
            "pitch": -30.0,
            "roll": 0.0,
            "yaw": 0.0,
            "description": "Tilted slightly down, looking ahead for tracking"
        },
        
        # Panorama - look forward
        "PANORAMA": {
            "name": "Panorama (Forward)",
            "pitch": -20.0,
            "roll": 0.0,
            "yaw": 0.0,
            "description": "Wide angle view forward for panoramic shots"
        },
        
        # Inspection mode - close range
        "INSPECTION": {
            "name": "Inspection (Close)",
            "pitch": -45.0,
            "roll": 0.0,
            "yaw": 0.0,
            "description": "Positioned for close-up inspections"
        },
        
        # Rotate 360 - starting position
        "ROTATE_START": {
            "name": "Rotate 360 Start",
            "pitch": -45.0,
            "roll": 0.0,
            "yaw": 0.0,
            "description": "Starting position for 360 degree rotation"
        },
        
        # Person tracking preset
        "PERSON_TRACKING": {
            "name": "Person Tracking",
            "pitch": -45.0,
            "roll": 0.0,
            "yaw": 0.0,
            "description": "Optimal angle for tracking persons on ground"
        },
        
        # Landing view - camera down
        "LANDING": {
            "name": "Landing View",
            "pitch": -75.0,
            "roll": 0.0,
            "yaw": 0.0,
            "description": "Gimbal angle for landing operations"
        },
    }
    
    @classmethod
    def get_preset(cls, preset_name):
        """Obține preset după nume"""
        return cls.PRESETS.get(preset_name.upper(), None)
    
    @classmethod
    def list_presets(cls):
        """Listează toate preset-urile disponibile"""
        print("\n" + "="*70)
        print("📸 GIMBAL PRESETS - Typhoon H480")
        print("="*70 + "\n")
        
        for key, preset in cls.PRESETS.items():
            print(f"🎬 {preset['name']}")
            print(f"   └─ {preset['description']}")
            print(f"   └─ Pitch: {preset['pitch']:6.1f}° | Roll: {preset['roll']:6.1f}° | Yaw: {preset['yaw']:6.1f}°\n")
    
    @classmethod
    def get_gimbal_angles(cls, preset_name):
        """Extrage unghiurile gimbal din preset"""
        preset = cls.get_preset(preset_name)
        
        if preset:
            return {
                "pitch": preset["pitch"],
                "roll": preset["roll"],
                "yaw": preset["yaw"]
            }
        return None


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("\n🎥 Gimbal Preset Manager\n")
    
    # List all presets
    GimbalPresets.list_presets()
    
    # Example: Get specific preset
    if len(sys.argv) > 1:
        preset_name = sys.argv[1]
        angles = GimbalPresets.get_gimbal_angles(preset_name)
        
        if angles:
            print(f"\n✅ Preset '{preset_name}' loaded:")
            print(f"   Pitch: {angles['pitch']}°")
            print(f"   Roll:  {angles['roll']}°")
            print(f"   Yaw:   {angles['yaw']}°\n")
        else:
            print(f"\n❌ Preset '{preset_name}' not found\n")
            sys.exit(1)
    else:
        print("\n💡 How to use:")
        print("   python3 GimbalPresets.py LOOK_AHEAD")
        print("   python3 GimbalPresets.py STRAIGHT_DOWN")
        print("   python3 GimbalPresets.py PERSON_TRACKING\n")
    
    
# ============================================================================
# INTEGRATION WITH CONTROL SCRIPT
# ============================================================================
"""
To use presets in your control script:

from GimbalPresets import GimbalPresets

def apply_gimbal_preset(preset_name):
    angles = GimbalPresets.get_gimbal_angles(preset_name)
    
    if angles:
        send_gimbal_command(
            pitch=angles['pitch'],
            roll=angles['roll'],
            yaw=angles['yaw']
        )
        print(f"Applied preset: {preset_name}")
    else:
        print(f"Preset not found: {preset_name}")

# Usage:
apply_gimbal_preset("STRAIGHT_DOWN")
apply_gimbal_preset("PERSON_TRACKING")
apply_gimbal_preset("SURVEILLANCE")
"""
