"""
Shadow Clone Jutsu Effect Module
Creates visual clone effects when the shadow clone hand seal is detected
"""

import cv2
import numpy as np
import time


class ShadowCloneEffect:
    def __init__(self, num_clones=4, effect_duration=3.0):
        """
        Initialize the Shadow Clone Effect
        
        Args:
            num_clones (int): Number of clones to display
            effect_duration (float): Duration of the effect in seconds
        """
        self.num_clones = num_clones
        self.effect_duration = effect_duration
        self.is_active = False
        self.activation_time = 0
        self.clone_positions = []
        
    def detect_shadow_clone_seal(self, hand_tracker, img):
        """
        Detect Shadow Clone Jutsu hand seal (crossed hands)
        
        Args:
            hand_tracker: HandTracker instance
            img: Current frame
            
        Returns:
            is_seal: Boolean indicating if the seal is detected
        """
        if not hand_tracker.results.multi_hand_landmarks:
            return False
        
        if len(hand_tracker.results.multi_hand_landmarks) < 2:
            return False
        
        h, w, c = img.shape
        
        # Get key landmarks for both hands
        hand1 = hand_tracker.results.multi_hand_landmarks[0].landmark
        hand2 = hand_tracker.results.multi_hand_landmarks[1].landmark
        
        # Get wrist and finger positions
        h1_wrist = hand1[0]
        h2_wrist = hand2[0]
        h1_middle_mcp = hand1[9]  # Middle finger base
        h2_middle_mcp = hand2[9]
        h1_index_tip = hand1[8]   # Index finger tip
        h2_index_tip = hand2[8]
        
        # Convert to pixel coordinates
        h1_wrist_x, h1_wrist_y = h1_wrist.x * w, h1_wrist.y * h
        h2_wrist_x, h2_wrist_y = h2_wrist.x * w, h2_wrist.y * h
        h1_middle_x = h1_middle_mcp.x * w
        h2_middle_x = h2_middle_mcp.x * w
        h1_index_x = h1_index_tip.x * w
        h2_index_x = h2_index_tip.x * w
        
        # Check if hands are crossed (fingers pointing opposite directions)
        # One hand's wrist should be on the left while its fingers point right, and vice versa
        crossed = (h1_wrist_x < h1_middle_x and h2_wrist_x > h2_middle_x and h1_wrist_x < h2_wrist_x) or \
                  (h1_wrist_x > h1_middle_x and h2_wrist_x < h2_middle_x and h1_wrist_x > h2_wrist_x)
        
        # Check if hands are at similar vertical position (overlapping)
        vertical_overlap = abs(h1_wrist_y - h2_wrist_y) < h * 0.2
        
        # Check if hands are close together horizontally (forming the seal)
        horizontal_distance = abs(h1_wrist_x - h2_wrist_x)
        close_together = horizontal_distance < w * 0.4 and horizontal_distance > w * 0.1
        
        # Check if index fingers are pointing in opposite directions
        fingers_opposite = (h1_index_x < h1_wrist_x and h2_index_x > h2_wrist_x) or \
                          (h1_index_x > h1_wrist_x and h2_index_x < h2_wrist_x)
        
        return crossed and vertical_overlap and close_together and fingers_opposite
    
    def activate(self):
        """Activate the shadow clone effect"""
        self.is_active = True
        self.activation_time = time.time()
        self._generate_clone_positions()
        
    def _generate_clone_positions(self):
        """Generate positions for clones in a circular pattern"""
        self.clone_positions = []
        angle_step = 360 / self.num_clones
        
        for i in range(self.num_clones):
            angle = np.radians(i * angle_step)
            # Offset from center
            offset_x = np.cos(angle) * 0.25
            offset_y = np.sin(angle) * 0.25
            scale = 0.4  # Clone size relative to original
            
            self.clone_positions.append({
                'offset_x': offset_x,
                'offset_y': offset_y,
                'scale': scale,
                'alpha': 0.7
            })
    
    def update(self):
        """Update effect state"""
        if self.is_active:
            elapsed = time.time() - self.activation_time
            if elapsed > self.effect_duration:
                self.is_active = False
    
    def apply_effect(self, frame):
        """
        Apply shadow clone effect to the frame
        
        Args:
            frame: Input video frame
            
        Returns:
            result_frame: Frame with clone effect applied
        """
        if not self.is_active:
            return frame
        
        h, w = frame.shape[:2]
        
        # Calculate fade effect based on time
        elapsed = time.time() - self.activation_time
        fade_in_duration = 0.3
        fade_out_duration = 0.5
        
        if elapsed < fade_in_duration:
            effect_alpha = elapsed / fade_in_duration
        elif elapsed > self.effect_duration - fade_out_duration:
            effect_alpha = (self.effect_duration - elapsed) / fade_out_duration
        else:
            effect_alpha = 1.0
        
        # Start with original frame
        result = frame.copy()
        
        # Draw clones on top
        for clone in self.clone_positions:
            clone_frame = self._create_clone(frame, clone, effect_alpha)
            # Blend clone with result
            mask = (clone_frame > 0).any(axis=2).astype(np.uint8) * 255
            mask_3ch = cv2.merge([mask, mask, mask])
            result = np.where(mask_3ch > 0, clone_frame, result)
        
        # Add "SHADOW CLONE JUTSU!" text
        self._draw_jutsu_text(result, effect_alpha)
        
        return result
    
    def _create_clone(self, frame, clone_config, effect_alpha):
        """Create a single clone image"""
        h, w = frame.shape[:2]
        
        # Calculate clone size and position
        scale = clone_config['scale']
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        # Resize frame for clone
        clone = cv2.resize(frame, (new_w, new_h))
        
        # Calculate position
        offset_x = int(clone_config['offset_x'] * w)
        offset_y = int(clone_config['offset_y'] * h)
        
        center_x = w // 2 + offset_x
        center_y = h // 2 + offset_y
        
        # Calculate placement coordinates
        x1 = max(0, center_x - new_w // 2)
        y1 = max(0, center_y - new_h // 2)
        x2 = min(w, x1 + new_w)
        y2 = min(h, y1 + new_h)
        
        # Adjust clone size if it goes out of bounds
        clone_x1 = 0 if x1 >= 0 else -(center_x - new_w // 2)
        clone_y1 = 0 if y1 >= 0 else -(center_y - new_h // 2)
        clone_x2 = new_w if x2 <= w else new_w - ((x1 + new_w) - w)
        clone_y2 = new_h if y2 <= h else new_h - ((y1 + new_h) - h)
        
        # Create result frame
        result = np.zeros_like(frame)
        
        if x2 > x1 and y2 > y1 and clone_x2 > clone_x1 and clone_y2 > clone_y1:
            clone_section = clone[clone_y1:clone_y2, clone_x1:clone_x2]
            # Make clones more visible
            alpha = min(0.85, clone_config['alpha'] * effect_alpha)
            result[y1:y2, x1:x2] = (clone_section * alpha + result[y1:y2, x1:x2] * (1 - alpha)).astype(np.uint8)
        
        return result
    
    def _draw_jutsu_text(self, frame, effect_alpha):
        """Draw 'SHADOW CLONE JUTSU!' text on frame"""
        h, w = frame.shape[:2]
        
        # Only show text in first 1.5 seconds
        elapsed = time.time() - self.activation_time
        if elapsed < 1.5:
            text = "SHADOW CLONE JUTSU!"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.5
            thickness = 3
            
            # Get text size
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            text_x = (w - text_size[0]) // 2
            text_y = 60
            
            # Text fade in/out
            if elapsed < 0.3:
                text_alpha = elapsed / 0.3
            elif elapsed > 1.2:
                text_alpha = (1.5 - elapsed) / 0.3
            else:
                text_alpha = 1.0
            
            text_alpha *= effect_alpha
            
            # Draw text with outline
            color = (0, 165, 255)  # Orange color
            outline_color = (0, 0, 0)
            
            # Outline
            cv2.putText(frame, text, (text_x - 2, text_y - 2), font, font_scale, 
                       outline_color, thickness + 2)
            cv2.putText(frame, text, (text_x + 2, text_y + 2), font, font_scale, 
                       outline_color, thickness + 2)
            
            # Main text
            overlay = frame.copy()
            cv2.putText(overlay, text, (text_x, text_y), font, font_scale, 
                       color, thickness)
            cv2.addWeighted(overlay, text_alpha, frame, 1 - text_alpha, 0, frame)
