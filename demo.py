"""
Hand Gesture Control - Demo Script
Test individual components of the system
"""

import cv2
import time
from hand_tracker import HandTracker
from gesture_recognition import GestureRecognizer
from screen_controller import ScreenController


def test_hand_tracking():
    """Test hand tracking functionality"""
    print("Testing Hand Tracking...")
    print("Show your hand to the camera. Press ESC to exit.")
    
    cap = cv2.VideoCapture(0)
    hand_tracker = HandTracker()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        frame, hands_found = hand_tracker.find_hands(frame)
        
        if hands_found:
            landmarks = hand_tracker.find_position(frame)
            if len(landmarks) > 0:
                fingers = hand_tracker.fingers_up()
                
                # Display finger states
                finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
                for i, (name, state) in enumerate(zip(finger_names, fingers)):
                    color = (0, 255, 0) if state else (0, 0, 255)
                    cv2.putText(frame, f"{name}: {'UP' if state else 'DOWN'}", 
                               (10, 30 + i * 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        cv2.imshow('Hand Tracking Test', frame)
        
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break
    
    cap.release()
    cv2.destroyAllWindows()


def test_gesture_recognition():
    """Test gesture recognition functionality"""
    print("Testing Gesture Recognition...")
    print("Make different gestures with your hand. Press ESC to exit.")
    
    cap = cv2.VideoCapture(0)
    hand_tracker = HandTracker()
    gesture_recognizer = GestureRecognizer()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        frame_height, frame_width = frame.shape[:2]
        
        frame, hands_found = hand_tracker.find_hands(frame)
        
        if hands_found:
            landmarks = hand_tracker.find_position(frame)
            if len(landmarks) > 0:
                fingers = hand_tracker.fingers_up()
                gesture, gesture_data = gesture_recognizer.recognize_gesture(
                    fingers, landmarks, (frame_width, frame_height)
                )
                
                # Display gesture information
                cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                if "position" in gesture_data:
                    pos = gesture_data["position"]
                    cv2.putText(frame, f"Position: ({pos[0]:.2f}, {pos[1]:.2f})", (10, 70),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                
                if "thumb_index_distance" in gesture_data:
                    dist = gesture_data["thumb_index_distance"]
                    cv2.putText(frame, f"Thumb-Index Distance: {dist:.1f}", (10, 110),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        
        cv2.imshow('Gesture Recognition Test', frame)
        
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break
    
    cap.release()
    cv2.destroyAllWindows()


def test_screen_controller():
    """Test screen controller functionality (without camera)"""
    print("Testing Screen Controller...")
    print("This will test mouse movements and clicks.")
    
    controller = ScreenController()
    
    # Test mouse movement
    print("Moving mouse to center of screen...")
    screen_width, screen_height = controller.screen_width, controller.screen_height
    center_x, center_y = screen_width // 2, screen_height // 2
    
    # Simulate gesture data for pointing
    gesture_data = {
        "position": [0.5, 0.5]  # Center of screen (normalized)
    }
    
    controller.execute_gesture_action("pointing", gesture_data)
    time.sleep(1)
    
    print("Mouse moved to center")
    
    # Test different positions
    positions = [
        ([0.25, 0.25], "Top-left quadrant"),
        ([0.75, 0.25], "Top-right quadrant"),
        ([0.75, 0.75], "Bottom-right quadrant"),
        ([0.25, 0.75], "Bottom-left quadrant"),
        ([0.5, 0.5], "Center")
    ]
    
    for pos, description in positions:
        print(f"Moving to {description}...")
        gesture_data["position"] = pos
        controller.execute_gesture_action("pointing", gesture_data)
        time.sleep(0.5)
    
    print("Screen controller test completed!")


def demo_all_gestures():
    """Demo all supported gestures"""
    print("Gesture Demo - All Supported Gestures")
    print("=" * 40)
    
    gestures = [
        ("pointing", "Point with index finger"),
        ("click", "Pinch thumb and index finger"),
        ("drag", "Pinch and move"),
        ("scroll", "Show index and middle fingers"),
        ("zoom", "Show three fingers (index, middle, ring)"),
        ("open_palm", "Show all fingers"),
        ("fist", "Close all fingers")
    ]
    
    for gesture, description in gestures:
        print(f"- {gesture.upper()}: {description}")
    
    print("\nPress SPACE to start demo, ESC to exit")
    
    cap = cv2.VideoCapture(0)
    hand_tracker = HandTracker()
    gesture_recognizer = GestureRecognizer()
    
    demo_started = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        frame_height, frame_width = frame.shape[:2]
        
        if not demo_started:
            cv2.putText(frame, "Press SPACE to start demo", (10, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(frame, "ESC to exit", (10, 100),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        else:
            frame, hands_found = hand_tracker.find_hands(frame)
            
            if hands_found:
                landmarks = hand_tracker.find_position(frame)
                if len(landmarks) > 0:
                    fingers = hand_tracker.fingers_up()
                    gesture, gesture_data = gesture_recognizer.recognize_gesture(
                        fingers, landmarks, (frame_width, frame_height)
                    )
                    
                    # Display current gesture
                    cv2.putText(frame, f"Current Gesture: {gesture.upper()}", (10, 50),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # Display finger states
                    finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
                    finger_display = " | ".join([f"{name}: {'UP' if state else 'DOWN'}" 
                                               for name, state in zip(finger_names, fingers)])
                    cv2.putText(frame, finger_display, (10, frame_height - 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            else:
                cv2.putText(frame, "No hands detected", (10, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.imshow('All Gestures Demo', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key
            break
        elif key == ord(' ') and not demo_started:  # SPACE key
            demo_started = True
            print("Demo started! Make different gestures with your hand.")
    
    cap.release()
    cv2.destroyAllWindows()


def main():
    """Main demo function"""
    print("=" * 50)
    print("    HAND GESTURE CONTROL SYSTEM DEMO")
    print("=" * 50)
    
    while True:
        print("\nSelect a demo:")
        print("1. Test Hand Tracking")
        print("2. Test Gesture Recognition")
        print("3. Test Screen Controller")
        print("4. Demo All Gestures")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            test_hand_tracking()
        elif choice == '2':
            test_gesture_recognition()
        elif choice == '3':
            test_screen_controller()
        elif choice == '4':
            demo_all_gestures()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
