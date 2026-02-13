"""
Configuration Module
Handles calibration, sensitivity settings, and gesture customization
"""

import json
import os
import cv2
import numpy as np


class GestureConfig:
    def __init__(self, config_file="gesture_config.json"):
        """
        Initialize the GestureConfig
        
        Args:
            config_file (str): Path to configuration file
        """
        self.config_file = config_file
        self.config = self.load_default_config()
        self.load_config()
        
    def load_default_config(self):
        """Load default configuration settings"""
        return {
            "sensitivity": {
                "mouse_movement": 1.0,
                "click_threshold": 40,
                "drag_threshold": 30,
                "scroll_sensitivity": 5
            },
            "timing": {
                "click_cooldown": 0.3,
                "scroll_cooldown": 0.1,
                "gesture_hold_threshold": 0.5
            },
            "detection": {
                "detection_confidence": 0.7,
                "tracking_confidence": 0.5,
                "smoothing_frames": 5,
                "movement_threshold": 5
            },
            "screen": {
                "calibrated_area": None,  # Will be set during calibration
                "mirror_mode": True,
                "control_zone": {
                    "enabled": False,
                    "x": 0.2,
                    "y": 0.2,
                    "width": 0.6,
                    "height": 0.6
                }
            },
            "gestures": {
                "pointing": {"enabled": True, "fingers": [0, 1, 0, 0, 0]},
                "click": {"enabled": True, "distance_threshold": 40},
                "drag": {"enabled": True, "distance_threshold": 30},
                "scroll": {"enabled": True, "fingers": [0, 1, 1, 0, 0]},
                "zoom": {"enabled": True, "fingers": [0, 1, 1, 1, 0]},
                "stop": {"enabled": True, "fingers": [1, 1, 1, 1, 1]}
            },
            "display": {
                "show_landmarks": True,
                "show_fps": True,
                "show_gesture_info": True,
                "frame_width": 640,
                "frame_height": 480
            }
        }
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    saved_config = json.load(f)
                    # Merge with defaults (in case new settings were added)
                    self._merge_config(saved_config)
                print(f"Configuration loaded from {self.config_file}")
            else:
                print("Using default configuration")
        except Exception as e:
            print(f"Error loading configuration: {e}")
            print("Using default configuration")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            print(f"Configuration saved to {self.config_file}")
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def _merge_config(self, saved_config):
        """Merge saved configuration with defaults"""
        def merge_dict(default, saved):
            for key, value in saved.items():
                if key in default:
                    if isinstance(value, dict) and isinstance(default[key], dict):
                        merge_dict(default[key], value)
                    else:
                        default[key] = value
        
        merge_dict(self.config, saved_config)
    
    def get(self, section, key=None, default=None):
        """Get configuration value"""
        if key is None:
            return self.config.get(section, default)
        return self.config.get(section, {}).get(key, default)
    
    def set(self, section, key, value):
        """Set configuration value"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
    
    def calibrate_screen_area(self, cap):
        """
        Interactive screen area calibration
        
        Args:
            cap: OpenCV video capture object
            
        Returns:
            calibrated_area: Dictionary with calibration data
        """
        print("\\nScreen Area Calibration")
        print("=" * 30)
        print("Instructions:")
        print("1. Position your hand at the TOP-LEFT corner of desired control area")
        print("2. Press SPACE to capture top-left corner")
        print("3. Position your hand at the BOTTOM-RIGHT corner")
        print("4. Press SPACE to capture bottom-right corner")
        print("5. Press ESC to cancel calibration")
        
        corners = []
        corner_names = ["TOP-LEFT", "BOTTOM-RIGHT"]
        current_corner = 0
        
        while current_corner < 2:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            frame_height, frame_width = frame.shape[:2]
            
            # Draw instructions
            instruction = f"Position hand at {corner_names[current_corner]} corner, then press SPACE"
            cv2.putText(frame, instruction, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            # Draw crosshair at center
            center_x, center_y = frame_width // 2, frame_height // 2
            cv2.line(frame, (center_x - 20, center_y), (center_x + 20, center_y), (0, 255, 0), 2)
            cv2.line(frame, (center_x, center_y - 20), (center_x, center_y + 20), (0, 255, 0), 2)
            
            # Show already captured corners
            for i, corner in enumerate(corners):
                cv2.circle(frame, corner, 10, (0, 0, 255), -1)
                cv2.putText(frame, corner_names[i], (corner[0] + 15, corner[1]), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            
            cv2.imshow('Calibration', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Space key
                corners.append((center_x, center_y))
                print(f"{corner_names[current_corner]} corner captured: ({center_x}, {center_y})")
                current_corner += 1
            elif key == 27:  # ESC key
                print("Calibration cancelled")
                cv2.destroyWindow('Calibration')
                return None
        
        cv2.destroyWindow('Calibration')
        
        if len(corners) == 2:
            # Calculate calibrated area
            top_left = corners[0]
            bottom_right = corners[1]
            
            # Normalize coordinates
            calibrated_area = {
                "top_left": [top_left[0] / frame_width, top_left[1] / frame_height],
                "bottom_right": [bottom_right[0] / frame_width, bottom_right[1] / frame_height],
                "width": abs(bottom_right[0] - top_left[0]) / frame_width,
                "height": abs(bottom_right[1] - top_left[1]) / frame_height
            }
            
            self.set("screen", "calibrated_area", calibrated_area)
            self.save_config()
            
            print(f"Calibration complete!")
            print(f"Control area: {calibrated_area}")
            return calibrated_area
        
        return None
    
    def test_sensitivity(self, cap, hand_tracker, gesture_recognizer):
        """
        Interactive sensitivity testing
        
        Args:
            cap: OpenCV video capture object
            hand_tracker: HandTracker instance
            gesture_recognizer: GestureRecognizer instance
        """
        print("\\nSensitivity Testing")
        print("=" * 20)
        print("Use +/- keys to adjust sensitivity")
        print("Press ESC when satisfied")
        
        current_sensitivity = self.get("sensitivity", "mouse_movement")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            frame, hands_found = hand_tracker.find_hands(frame, draw=True)
            
            if hands_found:
                hand_landmarks = hand_tracker.find_position(frame)
                if len(hand_landmarks) > 0:
                    fingers = hand_tracker.fingers_up()
                    gesture, gesture_data = gesture_recognizer.recognize_gesture(
                        fingers, hand_landmarks, frame.shape[:2]
                    )
                    
                    # Show gesture info
                    cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Show current sensitivity
            cv2.putText(frame, f"Sensitivity: {current_sensitivity:.1f}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            cv2.putText(frame, "Use +/- to adjust, ESC to finish", (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow('Sensitivity Test', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('+') or key == ord('='):
                current_sensitivity = min(3.0, current_sensitivity + 0.1)
                print(f"Sensitivity: {current_sensitivity:.1f}")
            elif key == ord('-') or key == ord('_'):
                current_sensitivity = max(0.1, current_sensitivity - 0.1)
                print(f"Sensitivity: {current_sensitivity:.1f}")
            elif key == 27:  # ESC
                break
        
        cv2.destroyWindow('Sensitivity Test')
        
        self.set("sensitivity", "mouse_movement", current_sensitivity)
        self.save_config()
        print(f"Sensitivity set to: {current_sensitivity:.1f}")
    
    def create_gesture_profile(self, profile_name):
        """Create a custom gesture profile"""
        profiles_dir = "gesture_profiles"
        os.makedirs(profiles_dir, exist_ok=True)
        
        profile_file = os.path.join(profiles_dir, f"{profile_name}.json")
        
        # Create a copy of current config as new profile
        with open(profile_file, 'w') as f:
            json.dump(self.config, f, indent=4)
        
        print(f"Gesture profile '{profile_name}' created")
        return profile_file
    
    def load_gesture_profile(self, profile_name):
        """Load a gesture profile"""
        profiles_dir = "gesture_profiles"
        profile_file = os.path.join(profiles_dir, f"{profile_name}.json")
        
        if os.path.exists(profile_file):
            with open(profile_file, 'r') as f:
                self.config = json.load(f)
            print(f"Gesture profile '{profile_name}' loaded")
            return True
        else:
            print(f"Gesture profile '{profile_name}' not found")
            return False
    
    def list_gesture_profiles(self):
        """List available gesture profiles"""
        profiles_dir = "gesture_profiles"
        if not os.path.exists(profiles_dir):
            return []
        
        profiles = []
        for file in os.listdir(profiles_dir):
            if file.endswith('.json'):
                profiles.append(file[:-5])  # Remove .json extension
        
        return profiles
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.load_default_config()
        self.save_config()
        print("Configuration reset to defaults")
    
    def export_config(self, filename):
        """Export configuration to a file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.config, f, indent=4)
            print(f"Configuration exported to {filename}")
        except Exception as e:
            print(f"Error exporting configuration: {e}")
    
    def import_config(self, filename):
        """Import configuration from a file"""
        try:
            with open(filename, 'r') as f:
                self.config = json.load(f)
            self.save_config()
            print(f"Configuration imported from {filename}")
        except Exception as e:
            print(f"Error importing configuration: {e}")


def main():
    """Configuration utility main function"""
    print("Gesture Control Configuration Utility")
    print("=" * 40)
    
    config = GestureConfig()
    
    while True:
        print("\\nOptions:")
        print("1. View current configuration")
        print("2. Reset to defaults")
        print("3. Create gesture profile")
        print("4. Load gesture profile")
        print("5. List gesture profiles")
        print("6. Export configuration")
        print("7. Import configuration")
        print("8. Exit")
        
        choice = input("\\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            print("\\nCurrent Configuration:")
            print(json.dumps(config.config, indent=2))
        
        elif choice == '2':
            confirm = input("Reset to defaults? (y/n): ")
            if confirm.lower() == 'y':
                config.reset_to_defaults()
        
        elif choice == '3':
            profile_name = input("Enter profile name: ")
            config.create_gesture_profile(profile_name)
        
        elif choice == '4':
            profiles = config.list_gesture_profiles()
            if profiles:
                print("Available profiles:", profiles)
                profile_name = input("Enter profile name to load: ")
                config.load_gesture_profile(profile_name)
            else:
                print("No profiles available")
        
        elif choice == '5':
            profiles = config.list_gesture_profiles()
            if profiles:
                print("Available profiles:", profiles)
            else:
                print("No profiles available")
        
        elif choice == '6':
            filename = input("Enter filename to export to: ")
            config.export_config(filename)
        
        elif choice == '7':
            filename = input("Enter filename to import from: ")
            config.import_config(filename)
        
        elif choice == '8':
            break
        
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
