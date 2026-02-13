"""
Screen Controller Module
Maps finger movements and gestures to screen actions using pyautogui
"""

import pyautogui
import numpy as np
import time
from collections import deque

# Disable pyautogui fail-safe (be careful!)
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01  # Small pause between commands


class ScreenController:
    def __init__(self, screen_width=None, screen_height=None, sensitivity=1.0):
        """
        Initialize the ScreenController
        
        Args:
            screen_width (int): Screen width in pixels (None for auto-detect)
            screen_height (int): Screen height in pixels (None for auto-detect)
            sensitivity (float): Mouse movement sensitivity multiplier
        """
        # Get screen dimensions
        if screen_width is None or screen_height is None:
            self.screen_width, self.screen_height = pyautogui.size()
        else:
            self.screen_width = screen_width
            self.screen_height = screen_height
        
        self.sensitivity = sensitivity
        
        # Control states
        self.is_mouse_pressed = False
        self.last_mouse_pos = [0, 0]
        self.click_cooldown = 0.3  # seconds between clicks
        self.last_click_time = 0
        self.scroll_cooldown = 0.1  # seconds between scroll actions
        self.last_scroll_time = 0
        
        # Movement smoothing
        self.movement_history = deque(maxlen=3)
        self.movement_threshold = 5  # pixels - minimum movement to register
        
        # Gesture state tracking
        self.previous_gesture = "none"
        self.gesture_start_time = time.time()
        
        print(f"Screen Controller initialized for {self.screen_width}x{self.screen_height} display")
    
    def execute_gesture_action(self, gesture, gesture_data):
        """
        Execute screen action based on recognized gesture
        
        Args:
            gesture: Recognized gesture name
            gesture_data: Additional gesture data (position, distances, etc.)
        """
        current_time = time.time()
        
        try:
            if gesture == "pointing":
                self._handle_pointing(gesture_data)
            elif gesture == "click":
                self._handle_click(gesture_data, current_time)
            elif gesture == "drag":
                self._handle_drag(gesture_data)
            elif gesture == "scroll":
                self._handle_scroll(gesture_data, current_time)
            elif gesture == "open_palm":
                self._handle_stop()
            elif gesture == "zoom":
                self._handle_zoom(gesture_data, current_time)
            elif gesture == "fist":
                self._handle_fist()
            else:
                # Unknown gesture or "none" - release any held mouse buttons
                if self.is_mouse_pressed:
                    pyautogui.mouseUp()
                    self.is_mouse_pressed = False
        
        except Exception as e:
            print(f"Error executing gesture action: {e}")
    
    def _handle_pointing(self, gesture_data):
        """Handle pointing gesture - move mouse cursor"""
        if "position" not in gesture_data:
            return
        
        # Convert normalized position to screen coordinates
        normalized_pos = gesture_data["position"]
        screen_x = int(normalized_pos[0] * self.screen_width)
        screen_y = int(normalized_pos[1] * self.screen_height)
        
        # Apply sensitivity and smoothing
        screen_x = int(screen_x * self.sensitivity)
        screen_y = int(screen_y * self.sensitivity)
        
        # Ensure coordinates are within screen bounds
        screen_x = max(0, min(screen_x, self.screen_width - 1))
        screen_y = max(0, min(screen_y, self.screen_height - 1))
        
        # Add movement smoothing
        self.movement_history.append([screen_x, screen_y])
        smooth_pos = self._smooth_movement()
        
        # Check if movement is significant enough
        if self._movement_threshold_met(smooth_pos):
            pyautogui.moveTo(smooth_pos[0], smooth_pos[1])
            self.last_mouse_pos = smooth_pos
    
    def _handle_click(self, gesture_data, current_time):
        """Handle click gesture - perform mouse click"""
        # Cooldown check
        if current_time - self.last_click_time < self.click_cooldown:
            return
        
        if "position" in gesture_data:
            # Move to position first
            self._handle_pointing(gesture_data)
            time.sleep(0.05)  # Small delay before clicking
        
        # Perform click
        pyautogui.click()
        self.last_click_time = current_time
        print("Click executed")
    
    def _handle_drag(self, gesture_data):
        """Handle drag gesture - drag mouse"""
        if "position" not in gesture_data:
            return
        
        # Convert position
        normalized_pos = gesture_data["position"]
        screen_x = int(normalized_pos[0] * self.screen_width * self.sensitivity)
        screen_y = int(normalized_pos[1] * self.screen_height * self.sensitivity)
        
        # Ensure coordinates are within bounds
        screen_x = max(0, min(screen_x, self.screen_width - 1))
        screen_y = max(0, min(screen_y, self.screen_height - 1))
        
        # Start dragging if not already
        if not self.is_mouse_pressed:
            pyautogui.mouseDown()
            self.is_mouse_pressed = True
            print("Drag started")
        
        # Drag to new position
        pyautogui.dragTo(screen_x, screen_y, duration=0.01)
    
    def _handle_scroll(self, gesture_data, current_time):
        """Handle scroll gesture - scroll up/down based on hand movement"""
        # Cooldown check
        if current_time - self.last_scroll_time < self.scroll_cooldown:
            return
        
        if "position" not in gesture_data or len(self.movement_history) < 2:
            return
        
        # Calculate vertical movement direction
        current_pos = gesture_data["position"]
        if len(self.movement_history) > 0:
            prev_pos = self.movement_history[-1]
            dy = current_pos[1] - (prev_pos[1] / self.screen_height)
            
            # Scroll based on vertical movement
            if abs(dy) > 0.01:  # Threshold for scroll sensitivity
                scroll_amount = int(dy * 5)  # Scale scroll amount
                if scroll_amount != 0:
                    pyautogui.scroll(scroll_amount)
                    self.last_scroll_time = current_time
    
    def _handle_stop(self):
        """Handle stop gesture - release all mouse buttons and stop actions"""
        if self.is_mouse_pressed:
            pyautogui.mouseUp()
            self.is_mouse_pressed = False
            print("Mouse released - Stop gesture")
    
    def _handle_zoom(self, gesture_data, current_time):
        """Handle zoom gesture - simulate zoom in/out"""
        # This could be implemented as Ctrl+scroll or other zoom shortcuts
        if current_time - self.last_scroll_time < self.scroll_cooldown:
            return
        
        # Simple zoom implementation using Ctrl+Plus/Minus
        if "thumb_index_distance" in gesture_data:
            distance = gesture_data["thumb_index_distance"]
            # Zoom in for larger distance, zoom out for smaller
            if distance > 60:
                pyautogui.hotkey('ctrl', 'plus')
            elif distance < 30:
                pyautogui.hotkey('ctrl', 'minus')
            
            self.last_scroll_time = current_time
    
    def _handle_fist(self):
        """Handle fist gesture - could be used for special actions"""
        # Release any pressed mouse buttons
        if self.is_mouse_pressed:
            pyautogui.mouseUp()
            self.is_mouse_pressed = False
    
    def _smooth_movement(self):
        """Apply smoothing to mouse movement"""
        if len(self.movement_history) == 0:
            return [0, 0]
        
        # Calculate average position from recent history
        positions = list(self.movement_history)
        avg_x = sum(pos[0] for pos in positions) / len(positions)
        avg_y = sum(pos[1] for pos in positions) / len(positions)
        
        return [int(avg_x), int(avg_y)]
    
    def _movement_threshold_met(self, new_pos):
        """Check if movement meets minimum threshold"""
        if not self.last_mouse_pos:
            return True
        
        distance = np.sqrt((new_pos[0] - self.last_mouse_pos[0])**2 + 
                          (new_pos[1] - self.last_mouse_pos[1])**2)
        
        return distance >= self.movement_threshold
    
    def calibrate_screen_area(self, top_left, bottom_right):
        """
        Calibrate the active screen area for gesture control
        
        Args:
            top_left: [x, y] coordinates of top-left corner
            bottom_right: [x, y] coordinates of bottom-right corner
        """
        self.calibrated_area = {
            'x': top_left[0],
            'y': top_left[1],
            'width': bottom_right[0] - top_left[0],
            'height': bottom_right[1] - top_left[1]
        }
        print(f"Screen area calibrated: {self.calibrated_area}")
    
    def set_sensitivity(self, sensitivity):
        """Set mouse movement sensitivity"""
        self.sensitivity = max(0.1, min(sensitivity, 3.0))
        print(f"Sensitivity set to: {self.sensitivity}")
    
    def emergency_stop(self):
        """Emergency stop - release all controls"""
        if self.is_mouse_pressed:
            pyautogui.mouseUp()
            self.is_mouse_pressed = False
        print("Emergency stop executed")
    
    def simulate_keyboard_shortcut(self, keys):
        """
        Simulate keyboard shortcut
        
        Args:
            keys: List of keys to press simultaneously
        """
        try:
            pyautogui.hotkey(*keys)
            print(f"Keyboard shortcut executed: {' + '.join(keys)}")
        except Exception as e:
            print(f"Error executing keyboard shortcut: {e}")
    
    def get_current_mouse_position(self):
        """Get current mouse position"""
        return pyautogui.position()
    
    def is_position_on_screen(self, x, y):
        """Check if position is within screen bounds"""
        return 0 <= x < self.screen_width and 0 <= y < self.screen_height
