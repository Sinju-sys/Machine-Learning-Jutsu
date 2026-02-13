"""
Gesture Recognition Module
Interprets hand gestures and converts them to specific commands
"""

import numpy as np
import time
from collections import deque


class GestureRecognizer:
    def __init__(self, smoothing_frames=5):
        """
        Initialize the GestureRecognizer
        
        Args:
            smoothing_frames (int): Number of frames to use for smoothing gestures
        """
        self.smoothing_frames = smoothing_frames
        self.gesture_history = deque(maxlen=smoothing_frames)
        self.previous_gesture = "none"
        self.gesture_start_time = time.time()
        self.gesture_hold_threshold = 0.5  # seconds
        
        # Gesture states
        self.is_clicking = False
        self.is_dragging = False
        self.click_start_time = 0
        self.drag_start_pos = [0, 0]
        
        # Position history for movement smoothing
        self.position_history = deque(maxlen=smoothing_frames)
    
    def recognize_gesture(self, fingers, hand_landmarks, frame_size):
        """
        Recognize gesture based on finger positions and hand landmarks
        
        Args:
            fingers: List of finger states [thumb, index, middle, ring, pinky]
            hand_landmarks: List of hand landmark positions
            frame_size: (width, height) of the video frame
            
        Returns:
            gesture: Recognized gesture name
            data: Additional data for the gesture (position, distance, etc.)
        """
        if len(hand_landmarks) == 0:
            return "none", {}
        
        # Extract key landmark positions
        index_tip = hand_landmarks[8]  # Index finger tip
        thumb_tip = hand_landmarks[4]   # Thumb tip
        middle_tip = hand_landmarks[12] # Middle finger tip
        ring_tip = hand_landmarks[16]   # Ring finger tip
        pinky_tip = hand_landmarks[20]  # Pinky finger tip
        
        # Calculate distances
        thumb_index_dist = self._calculate_distance(thumb_tip, index_tip)
        index_middle_dist = self._calculate_distance(index_tip, middle_tip)
        
        # Normalize coordinates to frame size
        normalized_index = [index_tip[1] / frame_size[0], index_tip[2] / frame_size[1]]
        
        # Add position to history for smoothing
        self.position_history.append(normalized_index)
        smoothed_pos = self._smooth_position()
        
        gesture_data = {
            "position": smoothed_pos,
            "thumb_index_distance": thumb_index_dist,
            "index_middle_distance": index_middle_dist,
            "raw_position": normalized_index
        }
        
        # Gesture recognition logic
        gesture = self._classify_gesture(fingers, thumb_index_dist, index_middle_dist)
        
        # Add gesture to history for smoothing
        self.gesture_history.append(gesture)
        stable_gesture = self._get_stable_gesture()
        
        return stable_gesture, gesture_data
    
    def _classify_gesture(self, fingers, thumb_index_dist, index_middle_dist):
        """
        Classify the gesture based on finger states and distances
        
        Args:
            fingers: List of finger states
            thumb_index_dist: Distance between thumb and index finger
            index_middle_dist: Distance between index and middle finger
            
        Returns:
            gesture: Classified gesture name
        """
        # Count extended fingers
        extended_count = sum(fingers)
        
        # Pointing gesture - Only index finger up
        if fingers == [0, 1, 0, 0, 0]:
            return "pointing"
        
        # Click gesture - Thumb and index finger close together (pinch)
        if fingers[0] == 1 and fingers[1] == 1 and thumb_index_dist < 40:
            return "click"
        
        # Drag gesture - Thumb and index finger pinched, with movement
        if fingers[0] == 1 and fingers[1] == 1 and thumb_index_dist < 30:
            return "drag"
        
        # Two finger scroll - Index and middle fingers up
        if fingers == [0, 1, 1, 0, 0]:
            return "scroll"
        
        # Open palm - All or most fingers up (for stop/pause)
        if extended_count >= 4:
            return "open_palm"
        
        # Peace sign - Index and middle fingers up, others down
        if fingers == [0, 1, 1, 0, 0]:
            return "peace"
        
        # Three fingers - Zoom gesture
        if fingers == [0, 1, 1, 1, 0]:
            return "zoom"
        
        # Fist - All fingers down
        if extended_count == 0:
            return "fist"
        
        # Default
        return "unknown"
    
    def _calculate_distance(self, point1, point2):
        """
        Calculate Euclidean distance between two points
        
        Args:
            point1, point2: Points in format [id, x, y]
            
        Returns:
            distance: Euclidean distance
        """
        x1, y1 = point1[1], point1[2]
        x2, y2 = point2[1], point2[2]
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def _smooth_position(self):
        """
        Apply smoothing to position using moving average
        
        Returns:
            smoothed_pos: Smoothed [x, y] position
        """
        if len(self.position_history) == 0:
            return [0, 0]
        
        positions = list(self.position_history)
        avg_x = sum(pos[0] for pos in positions) / len(positions)
        avg_y = sum(pos[1] for pos in positions) / len(positions)
        
        return [avg_x, avg_y]
    
    def _get_stable_gesture(self):
        """
        Get the most stable gesture from recent history
        
        Returns:
            stable_gesture: Most common gesture in recent history
        """
        if len(self.gesture_history) == 0:
            return "none"
        
        # Count occurrences of each gesture
        gesture_counts = {}
        for gesture in self.gesture_history:
            gesture_counts[gesture] = gesture_counts.get(gesture, 0) + 1
        
        # Return the most common gesture
        stable_gesture = max(gesture_counts, key=gesture_counts.get)
        
        # Require minimum consensus for stability
        if gesture_counts[stable_gesture] < len(self.gesture_history) // 2:
            return "none"
        
        return stable_gesture
    
    def is_gesture_held(self, gesture, required_duration=0.5):
        """
        Check if a gesture has been held for a minimum duration
        
        Args:
            gesture: Current gesture
            required_duration: Minimum duration in seconds
            
        Returns:
            is_held: Boolean indicating if gesture is held long enough
        """
        current_time = time.time()
        
        if gesture != self.previous_gesture:
            self.gesture_start_time = current_time
            self.previous_gesture = gesture
            return False
        
        return (current_time - self.gesture_start_time) >= required_duration
    
    def detect_swipe(self, position_history, min_distance=0.1, max_time=1.0):
        """
        Detect swipe gestures based on position history
        
        Args:
            position_history: List of recent positions
            min_distance: Minimum distance for swipe detection
            max_time: Maximum time for swipe gesture
            
        Returns:
            swipe_direction: Direction of swipe ("left", "right", "up", "down", "none")
        """
        if len(position_history) < 3:
            return "none"
        
        start_pos = position_history[0]
        end_pos = position_history[-1]
        
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance < min_distance:
            return "none"
        
        # Determine primary direction
        if abs(dx) > abs(dy):
            return "right" if dx > 0 else "left"
        else:
            return "down" if dy > 0 else "up"
    
    def reset_state(self):
        """Reset all gesture states"""
        self.is_clicking = False
        self.is_dragging = False
        self.click_start_time = 0
        self.drag_start_pos = [0, 0]
        self.gesture_history.clear()
        self.position_history.clear()
        self.previous_gesture = "none"
