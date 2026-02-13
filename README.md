# Hand Gesture Control System

Control your computer with your hands like a wizard, and perform Shadow Clone Jutsu like Naruto! This project gives you two superpowers: gesture-based computer control and ninja jutsu effects. No keyboard, no mouse, no hand seals required (well, except for the jutsu part).

## What Can You Do?

This project has TWO awesome modes:

### Mode 1: Computer Control (Be a Tech Wizard)
Wave your hands and control your computer like you're in a sci-fi movie. Point to move the cursor, pinch to click, and scroll without touching anything. Perfect for looking cool during presentations or controlling Netflix while eating snacks.

### Mode 2: Shadow Clone Jutsu (Be a Ninja)
Cross your hands like Naruto and watch yourself multiply on screen with epic sound effects and visual clones. Great for video calls, content creation, or just feeling like an anime character. Believe it!

## Gestures You Can Use

### Computer Control Gestures

POINTING - Stick out your index finger and move your cursor around like a Jedi using the Force

PINCH TO CLICK - Bring your thumb and index finger together like you're picking up something tiny. That's a click!

DRAG - Keep your thumb and index finger close and move around to drag things across your screen

SCROLL - Hold up two fingers (peace sign style) and move up or down to scroll through pages

ZOOM - Three fingers up to zoom in and out. Great for maps and photos!

OPEN PALM - Show your whole hand to stop everything. It's like saying "STOP!" to your computer

FIST - Close your hand into a fist for an emergency brake. Everything stops immediately!

### Ninja Mode Gesture

SHADOW CLONE SEAL - Cross your hands (one horizontal, one vertical) like Naruto's famous hand seal. Four clones of yourself appear on screen with sound effects and text. There's a cooldown period because even ninjas need to recharge their chakra!

## Installation

### 1. Clone or Download
```bash
git clone <repository-url>
cd hand_gesture_control
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage
1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Position yourself:**
   - Sit comfortably in front of your webcam
   - Ensure good lighting
   - Keep your hand visible in the camera frame

3. **Start controlling:**
   - Point with your index finger to move the cursor
   - Pinch thumb and index finger to click
   - Use different gestures for various actions

### Keyboard Controls
- **ESC**: Exit application
- **SPACE**: Toggle gesture control on/off
- **L**: Toggle landmark display
- **R**: Reset gesture recognizer
- **S**: Take screenshot
- **+/-**: Adjust sensitivity

## Configuration

### Using the Configuration Utility
Run the configuration utility for advanced settings:
```bash
python config.py
```

### Manual Configuration
Edit `gesture_config.json` to customize:

```json
{
    "sensitivity": {
        "mouse_movement": 1.0,
        "click_threshold": 40,
        "drag_threshold": 30
    },
    "timing": {
        "click_cooldown": 0.3,
        "scroll_cooldown": 0.1
    },
    "gestures": {
        "pointing": {"enabled": true},
        "click": {"enabled": true},
        "scroll": {"enabled": true}
    }
}
```

## Calibration

### Screen Area Calibration
1. Run the main application
2. Use the configuration menu to calibrate screen area
3. Position your hand at desired control boundaries
4. Follow on-screen instructions

### Sensitivity Adjustment
- Use **+** and **-** keys during operation
- Or use the configuration utility for precise control
- Test different values to find what works best for you

## What's in the Box

Here's what each file does:

main.py - The wizard mode (computer control)
shadow_clone_demo.py - The ninja mode (Shadow Clone Jutsu)
shadow_clone_effect.py - Makes the clone magic happen
hand_tracker.py - Watches your hands and figures out what they're doing
gesture_recognition.py - Translates hand movements into actions
screen_controller.py - Actually controls your mouse and keyboard
config.py - Lets you customize everything
sound-effect-jutsu.wav - The epic sound when you do the jutsu

Plus some other helper files and folders for configs and profiles.

## When Things Don't Work

### Camera Issues
Can't see anything? Make sure your webcam is plugged in and not being used by another app (like Zoom or Skype). Try closing other programs that might be hogging the camera.

### Gestures Not Recognized
The computer can't see your hand? You probably need better lighting. Sit near a window or turn on more lights. Also, make sure your hand is actually in the camera frame!

### Shadow Clone Jutsu Not Triggering
The seal detection is pretty strict (as it should be for ninja techniques). Make sure:
- Both hands are clearly visible
- You're actually crossing them properly (one horizontal, one vertical)
- Your hands are overlapping in the middle
- You're not moving too fast

### It's Laggy or Slow
Close some other programs. This uses your webcam and does real-time AI stuff, so it needs some computer power. Also, make sure you have good lighting so the camera doesn't have to work as hard.

### The Jutsu Sound Doesn't Play
Make sure the file `sound-effect-jutsu.wav` is in the same folder as the program. If it's missing, the visual effects will still work, but you won't get the epic audio.

## Advanced Usage

### Custom Gesture Profiles
1. Create a new profile:
   ```bash
   python config.py
   ```
2. Select "Create gesture profile"
3. Customize settings for specific use cases

### Integration with Other Applications
The screen controller can be extended to work with specific applications:
- Add custom keyboard shortcuts
- Implement application-specific gestures
- Create context-aware controls

## Safety Stuff

Don't worry, we've got safety features:

- Move your mouse to the corner of the screen to stop everything (fail-safe)
- Press SPACE to turn off gesture control instantly
- You can see what gesture is detected on screen
- Cooldowns prevent you from accidentally clicking a million times
- The Shadow Clone Jutsu has a cooldown so you don't spam it

## Performance Optimization

### For Better Performance:
- Use a good quality webcam
- Ensure adequate lighting
- Keep background simple
- Reduce camera resolution if needed
- Close unnecessary applications

### Hardware Requirements:
- **Webcam**: Any USB webcam (720p or higher recommended)
- **CPU**: Dual-core processor or better
- **RAM**: 4GB or more
- **OS**: Windows 10+, macOS 10.14+, or Linux

## Share Your Awesomeness

Made something cool? Record it and share! Tag your videos with #HandGestureMagic or #ShadowCloneJutsu. Show your friends, teach others, and most importantly - have fun!

## Credits

This project uses some amazing technology:
- MediaPipe by Google (the hand tracking magic)
- OpenCV (computer vision wizardry)
- PyAutoGUI (the thing that actually moves your mouse)
- Pygame (for the epic sound effects)

## Final Words

You now have two superpowers: control technology with your hands like Tony Stark, and perform ninja jutsu like Naruto. Use them wisely, use them often, and definitely use them to impress people.

Remember: Good lighting is your best friend. Seriously, we can't stress this enough. LIGHTING MATTERS.

Now go forth and be awesome!

Believe it!
