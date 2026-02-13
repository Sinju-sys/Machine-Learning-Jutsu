"""
Shadow Clone Jutsu Demo
Demonstrates the shadow clone effect when the hand seal is detected
"""

import cv2
import time
import pygame
import os
from hand_tracker import HandTracker
from shadow_clone_effect import ShadowCloneEffect


def main():
    print("=" * 50)
    print("    SHADOW CLONE JUTSU - DEMO")
    print("=" * 50)
    print("\nInstructions:")
    print("1. Show both hands to the camera")
    print("2. Cross your hands like Naruto's Shadow Clone seal")
    print("3. Watch the clones appear!")
    print("\nControls:")
    print("- ESC: Exit")
    print("- SPACE: Manual trigger effect")
    print("\n")
    
    # Initialize pygame mixer for sound
    pygame.mixer.init()
    sound_file = "sound-effect-jutsu.wav"
    jutsu_sound = None
    
    if os.path.exists(sound_file):
        try:
            jutsu_sound = pygame.mixer.Sound(sound_file)
            print(f"Sound effect loaded: {sound_file}")
        except Exception as e:
            print(f"Warning: Could not load sound file: {e}")
    else:
        print(f"Warning: Sound file not found: {sound_file}")
    
    # Initialize components
    hand_tracker = HandTracker(max_hands=2, detection_confidence=0.7)
    shadow_clone = ShadowCloneEffect(num_clones=4, effect_duration=3.0)
    
    # Camera setup
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("Error: Cannot open camera")
        return
    
    print("Camera initialized. Starting detection...")
    
    # State tracking
    seal_detected_last_frame = False
    cooldown_time = 0
    cooldown_duration = 4.0  # Cooldown between activations
    
    # FPS tracking
    fps_counter = 0
    fps_start_time = time.time()
    current_fps = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error reading frame")
                break
            
            # Flip for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect hands
            frame, hands_found = hand_tracker.find_hands(frame, draw=True)
            
            # Check for shadow clone seal
            current_time = time.time()
            seal_detected = False
            
            if hands_found and current_time > cooldown_time:
                seal_detected = shadow_clone.detect_shadow_clone_seal(hand_tracker, frame)
                
                # Activate effect on seal detection (edge trigger)
                if seal_detected and not seal_detected_last_frame:
                    print("SHADOW CLONE JUTSU ACTIVATED!")
                    shadow_clone.activate()
                    cooldown_time = current_time + cooldown_duration
                    
                    # Play sound effect
                    if jutsu_sound:
                        try:
                            jutsu_sound.play()
                        except Exception as e:
                            print(f"Error playing sound: {e}")
            
            seal_detected_last_frame = seal_detected
            
            # Update and apply effect
            shadow_clone.update()
            
            if shadow_clone.is_active:
                frame = shadow_clone.apply_effect(frame)
            
            # Draw UI
            _draw_ui(frame, hands_found, seal_detected, shadow_clone.is_active, 
                    current_fps, cooldown_time, current_time)
            
            # Update FPS
            fps_counter += 1
            if current_time - fps_start_time >= 1.0:
                current_fps = fps_counter / (current_time - fps_start_time)
                fps_counter = 0
                fps_start_time = current_time
            
            # Show frame
            cv2.imshow('Shadow Clone Jutsu', frame)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == ord(' '):  # Space - manual trigger
                if current_time > cooldown_time:
                    print("Manual activation!")
                    shadow_clone.activate()
                    cooldown_time = current_time + cooldown_duration
                    
                    # Play sound effect
                    if jutsu_sound:
                        try:
                            jutsu_sound.play()
                        except Exception as e:
                            print(f"Error playing sound: {e}")
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        pygame.mixer.quit()
        print("Demo ended")


def _draw_ui(frame, hands_found, seal_detected, effect_active, fps, cooldown_time, current_time):
    """Draw UI elements on frame"""
    h, w = frame.shape[:2]
    
    # Status
    status_color = (0, 255, 0) if hands_found else (0, 0, 255)
    hands_text = f"Hands: {2 if seal_detected else ('Detected' if hands_found else 'Not Found')}"
    cv2.putText(frame, hands_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
               0.7, status_color, 2)
    
    # Seal detection
    if seal_detected:
        cv2.putText(frame, "SEAL DETECTED!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.8, (0, 255, 255), 2)
    
    # Effect status
    if effect_active:
        cv2.putText(frame, "EFFECT ACTIVE", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (0, 165, 255), 2)
    
    # Cooldown indicator
    if current_time < cooldown_time:
        remaining = cooldown_time - current_time
        cv2.putText(frame, f"Cooldown: {remaining:.1f}s", (10, h - 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 255), 2)
    else:
        cv2.putText(frame, "Ready!", (10, h - 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Instructions
    cv2.putText(frame, "Cross your hands to activate", (10, h - 40), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    cv2.putText(frame, "ESC: Exit | SPACE: Manual trigger", (10, h - 15), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    # FPS
    cv2.putText(frame, f"FPS: {fps:.1f}", (w - 100, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


if __name__ == "__main__":
    main()
