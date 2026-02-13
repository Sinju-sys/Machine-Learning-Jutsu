"""
Hand Tracking Module using MediaPipe
Provides functionality to detect and track hand landmarks in real-time
"""

import cv2
import mediapipe as mp
import numpy as np


class HandTracker:
    def __init__(self, max_hands=2, detection_confidence=0.7, tracking_confidence=0.5):
        """
        Initialize the HandTracker
        
        Args:
            max_hands (int): Maximum number of hands to detect
            detection_confidence (float): Confidence threshold for hand detection
            tracking_confidence (float): Confidence threshold for hand tracking
        """
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Hand landmark indices for important points
        self.tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky fingertips
        self.pip_ids = [3, 6, 10, 14, 18]  # Previous joint of fingertips
        
    def find_hands(self, img, draw=True):
        """
        Find hands in the given image
        
        Args:
            img: Input image
            draw (bool): Whether to draw hand landmarks
            
        Returns:
            img: Image with or without hand landmarks drawn
            hands_found: Boolean indicating if hands were found
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        hands_found = False
        if self.results.multi_hand_landmarks:
            hands_found = True
            if draw:
                for hand_landmarks in self.results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
        
        return img, hands_found
    
    def find_position(self, img, hand_no=0, draw=True):
        """
        Find the position of hand landmarks
        
        Args:
            img: Input image
            hand_no (int): Hand index (0 for first hand)
            draw (bool): Whether to draw landmark points
            
        Returns:
            lm_list: List of landmark positions [id, x, y]
        """
        self.lm_list = []
        
        if self.results.multi_hand_landmarks:
            if len(self.results.multi_hand_landmarks) > hand_no:
                my_hand = self.results.multi_hand_landmarks[hand_no]
                
                for id, lm in enumerate(my_hand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lm_list.append([id, cx, cy])
                    
                    if draw:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        
        return self.lm_list
    
    def fingers_up(self):
        """
        Determine which fingers are up
        
        Returns:
            fingers: List of 5 elements (0 or 1) for each finger (thumb, index, middle, ring, pinky)
        """
        fingers = []
        
        if len(self.lm_list) != 0:
            # Thumb - Compare x coordinates (different logic due to thumb orientation)
            if self.lm_list[self.tip_ids[0]][1] < self.lm_list[self.tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            
            # Other four fingers - Compare y coordinates
            for id in range(1, 5):
                if self.lm_list[self.tip_ids[id]][2] < self.lm_list[self.pip_ids[id]][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        else:
            fingers = [0, 0, 0, 0, 0]
        
        return fingers
    
    def find_distance(self, p1, p2, img=None, draw=True, r=15, t=3):
        """
        Find distance between two landmark points
        
        Args:
            p1, p2: Point indices
            img: Input image
            draw (bool): Whether to draw the connection
            r: Circle radius
            t: Line thickness
            
        Returns:
            length: Distance between points
            img: Image with drawing (if draw=True)
            info: [x1, y1, x2, y2, cx, cy] coordinates
        """
        if len(self.lm_list) == 0:
            return 0, img, []
        
        x1, y1 = self.lm_list[p1][1], self.lm_list[p1][2]
        x2, y2 = self.lm_list[p2][1], self.lm_list[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
        if img is not None and draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return length, img, [x1, y1, x2, y2, cx, cy]
    
    def get_hand_center(self):
        """
        Calculate the center point of the hand
        
        Returns:
            center: [x, y] coordinates of hand center
        """
        if len(self.lm_list) == 0:
            return [0, 0]
        
        x_coords = [lm[1] for lm in self.lm_list]
        y_coords = [lm[2] for lm in self.lm_list]
        
        center_x = sum(x_coords) // len(x_coords)
        center_y = sum(y_coords) // len(y_coords)
        
        return [center_x, center_y]
    
    def get_index_finger_tip(self):
        """
        Get the position of the index finger tip
        
        Returns:
            tip_pos: [x, y] coordinates of index finger tip
        """
        if len(self.lm_list) == 0:
            return [0, 0]
        
        return [self.lm_list[8][1], self.lm_list[8][2]]
    
    def get_all_hands_landmarks(self):
        """
        Get landmarks for all detected hands
        
        Returns:
            all_hands: List of landmark lists for each hand
        """
        all_hands = []
        
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                hand_lm_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    hand_lm_list.append([id, lm.x, lm.y, lm.z])
                all_hands.append(hand_lm_list)
        
        return all_hands
    
    def detect_shadow_clone_seal(self, img):
        """
        Detect Shadow Clone Jutsu hand seal (crossed hands with extended fingers)
        
        Returns:
            is_seal: Boolean indicating if the seal is detected
        """
        if not self.results.multi_hand_landmarks:
            return False
        
        if len(self.results.multi_hand_landmarks) < 2:
            return False
        
        h, w, c = img.shape
        
        # Get key landmarks for both hands
        hand1 = self.results.multi_hand_landmarks[0].landmark
        hand2 = self.results.multi_hand_landmarks[1].landmark
        
        # Get wrist and middle finger MCP (base) positions
        h1_wrist = hand1[0]
        h2_wrist = hand2[0]
        h1_index_mcp = hand1[5]  # Index finger base
        h2_index_mcp = hand2[5]
        
        # Convert to pixel coordinates
        h1_wrist_x, h1_wrist_y = h1_wrist.x * w, h1_wrist.y * h
        h2_wrist_x, h2_wrist_y = h2_wrist.x * w, h2_wrist.y * h
        h1_index_x = h1_index_mcp.x * w
        h2_index_x = h2_index_mcp.x * w
        
        # Check if hands are crossed (one hand's wrist is on opposite side of other hand's fingers)
        crossed = (h1_wrist_x < h2_wrist_x and h1_index_x > h2_index_x) or \
                  (h1_wrist_x > h2_wrist_x and h1_index_x < h2_index_x)
        
        # Check if hands are at similar vertical position (overlapping)
        vertical_overlap = abs(h1_wrist_y - h2_wrist_y) < h * 0.15
        
        # Check if hands are close together (forming the seal)
        distance = np.sqrt((h1_wrist_x - h2_wrist_x)**2 + (h1_wrist_y - h2_wrist_y)**2)
        close_together = distance < w * 0.3
        
        return crossed and vertical_overlap and close_together
