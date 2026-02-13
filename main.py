"""
Hand Gesture Control - Main Application
Combines hand tracking, gesture recognition, and screen control
"""

import cv2
import time
import numpy as np
from hand_tracker import HandTracker
from gesture_recognition import GestureRecognizer
from screen_controller import ScreenController


class HandGestureController:
    def __init__(self, camera_id=0, sensitivity=1.0):
        """
        Initialize the Hand Gesture Controller
        
        Args:
            camera_id (int): Camera device ID
            sensitivity (float): Mouse movement sensitivity
        """
        self.camera_id = camera_id
        self.sensitivity = sensitivity
        
        # Initialize components
        self.hand_tracker = HandTracker(max_hands=2, detection_confidence=0.7)
        self.gesture_recognizer = GestureRecognizer(smoothing_frames=5)
        self.screen_controller = ScreenController(sensitivity=sensitivity)
        
        # Shadow Clone Jutsu variables
        self.shadow_clone_active = False
        self.clone_activation_time = 0
        self.clone_duration = 3.0  # seconds
        self.num_clones = 4
        
        # Camera setup
        self.cap = None
        self.frame_width = 640
        self.frame_height = 480
        
        # Control variables
        self.is_running = False
        self.show_landmarks = True
        self.show_fps = True
        self.control_enabled = True
        
        # Performance tracking
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        
        # Status display
        self.current_gesture = "none"
        self.status_message = "Ready"
        
        print("Hand Gesture Controller initialized")
        print("Controls:")
        print("- ESC: Exit application")
        print("- SPACE: Toggle gesture control on/off")
        print("- 'l': Toggle landmark display")
        print("- 'r': Reset gesture recognizer")
        print("- 's': Take screenshot")
    
    def initialize_camera(self):
        """Initialize camera capture"""
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            
            if not self.cap.isOpened():
                raise Exception(f"Cannot open camera {self.camera_id}")
            
            print(f"Camera {self.camera_id} initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False
    
    def run(self):
        """Main application loop"""
        if not self.initialize_camera():
            return
        
        self.is_running = True
        print("\\nStarting Hand Gesture Control...")
        print("Show your hand to the camera and make gestures!")
        
        try:
            while self.is_running:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error reading frame from camera")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                frame_height, frame_width = frame.shape[:2]
                
                # Process hand tracking
                frame, hands_found = self.hand_tracker.find_hands(frame, draw=self.show_landmarks)
                
                if hands_found:
                    # Get hand landmarks
                    hand_landmarks = self.hand_tracker.find_position(frame, draw=False)
                    
                    if len(hand_landmarks) > 0:
                        # Get finger states
                        fingers = self.hand_tracker.fingers_up()
                        
                        # Recognize gesture
                        gesture, gesture_data = self.gesture_recognizer.recognize_gesture(
                            fingers, hand_landmarks, (frame_width, frame_height)
                        )
                        
                        self.current_gesture = gesture
                        
                        # Execute screen control if enabled
                        if self.control_enabled and gesture != "none":
                            self.screen_controller.execute_gesture_action(gesture, gesture_data)
                            self.status_message = f"Executing: {gesture}"
                        else:
                            self.status_message = f"Detected: {gesture} (Control: {'ON' if self.control_enabled else 'OFF'})"
                        
                        # Draw gesture information
                        self._draw_gesture_info(frame, gesture, fingers)
                        
                        # Draw hand center and index finger tip
                        if self.show_landmarks:
                            self._draw_key_points(frame, hand_landmarks)
                
                else:
                    self.current_gesture = "none"
                    self.status_message = "No hands detected"
                
                # Draw UI elements
                self._draw_ui(frame)
                
                # Update FPS
                self._update_fps()
                
                # Show frame
                cv2.imshow('Hand Gesture Control', frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if not self._handle_keypress(key):
                    break
        
        except KeyboardInterrupt:
            print("\\nInterrupted by user")
        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            self._cleanup()
    
    def _draw_gesture_info(self, frame, gesture, fingers):
        """Draw gesture information on frame"""
        # Gesture name
        cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Finger states
        finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        for i, (name, state) in enumerate(zip(finger_names, fingers)):
            color = (0, 255, 0) if state else (0, 0, 255)
            cv2.putText(frame, f"{name}: {'UP' if state else 'DOWN'}", 
                       (10, 60 + i * 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    def _draw_key_points(self, frame, hand_landmarks):
        """Draw key hand points"""
        if len(hand_landmarks) > 8:  # Index finger tip
            index_tip = hand_landmarks[8]
            cv2.circle(frame, (index_tip[1], index_tip[2]), 10, (0, 255, 255), -1)
            cv2.putText(frame, "Index", (index_tip[1] + 15, index_tip[2]), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        if len(hand_landmarks) > 4:  # Thumb tip
            thumb_tip = hand_landmarks[4]
            cv2.circle(frame, (thumb_tip[1], thumb_tip[2]), 8, (255, 0, 255), -1)
    
    def _draw_ui(self, frame):
        """Draw user interface elements"""
        frame_height, frame_width = frame.shape[:2]
        
        # Status message
        cv2.putText(frame, self.status_message, (10, frame_height - 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Control status
        control_text = f"Control: {'ENABLED' if self.control_enabled else 'DISABLED'}"
        control_color = (0, 255, 0) if self.control_enabled else (0, 0, 255)
        cv2.putText(frame, control_text, (10, frame_height - 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, control_color, 2)
        
        # FPS counter
        if self.show_fps:
            cv2.putText(frame, f"FPS: {self.current_fps:.1f}", (frame_width - 100, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Instructions
        instructions = [
            "ESC: Exit | SPACE: Toggle Control",
            "L: Landmarks | R: Reset | S: Screenshot"
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (10, frame_height - 120 + i * 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    
    def _update_fps(self):
        """Update FPS counter"""
        self.fps_counter += 1
        current_time = time.time()
        
        if current_time - self.fps_start_time >= 1.0:
            self.current_fps = self.fps_counter / (current_time - self.fps_start_time)
            self.fps_counter = 0
            self.fps_start_time = current_time
    
    def _handle_keypress(self, key):
        """Handle keyboard input"""
        if key == 27:  # ESC key
            print("Exiting...")
            return False
        elif key == ord(' '):  # Space key
            self.control_enabled = not self.control_enabled
            self.screen_controller.emergency_stop()
            print(f"Gesture control: {'ENABLED' if self.control_enabled else 'DISABLED'}")
        elif key == ord('l') or key == ord('L'):  # L key
            self.show_landmarks = not self.show_landmarks
            print(f"Landmarks: {'SHOWN' if self.show_landmarks else 'HIDDEN'}")
        elif key == ord('r') or key == ord('R'):  # R key
            self.gesture_recognizer.reset_state()
            self.screen_controller.emergency_stop()
            print("Gesture recognizer reset")
        elif key == ord('s') or key == ord('S'):  # S key
            timestamp = int(time.time())
            filename = f"gesture_screenshot_{timestamp}.jpg"
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite(filename, cv2.flip(frame, 1))
                print(f"Screenshot saved: {filename}")
        elif key == ord('+') or key == ord('='):  # Increase sensitivity
            self.sensitivity = min(3.0, self.sensitivity + 0.1)
            self.screen_controller.set_sensitivity(self.sensitivity)
        elif key == ord('-') or key == ord('_'):  # Decrease sensitivity
            self.sensitivity = max(0.1, self.sensitivity - 0.1)
            self.screen_controller.set_sensitivity(self.sensitivity)
        
        return True
    
    def _cleanup(self):
        """Clean up resources"""
        print("\\nCleaning up...")
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.screen_controller.emergency_stop()
        print("Cleanup complete")


def main():
    """Main function"""
    print("=" * 50)
    print("       HAND GESTURE CONTROL SYSTEM")
    print("=" * 50)
    print()
    
    try:
        # Create and run the application
        app = HandGestureController(camera_id=0, sensitivity=1.0)
        app.run()
        
    except Exception as e:
        print(f"Application error: {e}")
    
    print("\\nThank you for using Hand Gesture Control!")


if __name__ == "__main__":
    main()
