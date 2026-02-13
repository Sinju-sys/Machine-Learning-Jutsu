# Hand Gesture Control System

A machine learning-powered application that allows you to control your computer screen using finger movements and hand gestures. Built with OpenCV and MediaPipe for real-time hand tracking, and pyautogui for screen control.

## Features

- **Real-time Hand Tracking**: Uses MediaPipe for accurate hand landmark detection
- **Gesture Recognition**: Recognizes various hand gestures for different actions
- **Screen Control**: Maps finger movements to mouse actions
- **Customizable Settings**: Configurable sensitivity, gestures, and screen areas
- **Multiple Profiles**: Save and load different gesture profiles
- **Interactive Calibration**: Easy setup for optimal performance

## Supported Gestures

| Gesture | Description | Action |
|---------|-------------|--------|
| **Pointing** | Index finger extended | Move mouse cursor |
| **Click** | Thumb and index finger pinched | Mouse click |
| **Drag** | Thumb and index finger close together while moving | Mouse drag |
| **Scroll** | Index and middle fingers extended | Scroll up/down |
| **Zoom** | Three fingers extended | Zoom in/out (Ctrl +/-) |
| **Open Palm** | All fingers extended | Stop/release all actions |
| **Fist** | All fingers closed | Emergency stop |

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

## File Structure

```
hand_gesture_control/
├── main.py                 # Main application
├── hand_tracker.py         # Hand tracking module
├── gesture_recognition.py  # Gesture recognition logic
├── screen_controller.py    # Screen control interface
├── config.py              # Configuration utility
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── gesture_config.json   # Configuration file (auto-generated)
└── gesture_profiles/     # Custom profiles directory
```

## Troubleshooting

### Common Issues

1. **Camera not working:**
   - Check if camera is connected and working
   - Try changing camera ID in main.py (camera_id=1, 2, etc.)
   - Ensure no other applications are using the camera

2. **Poor gesture recognition:**
   - Ensure good lighting
   - Keep hand steady
   - Adjust detection confidence in config
   - Calibrate screen area

3. **Mouse control not working:**
   - Check if pyautogui is properly installed
   - Disable fail-safe if needed (use with caution)
   - Adjust sensitivity settings

4. **Performance issues:**
   - Lower camera resolution
   - Reduce smoothing frames
   - Close other resource-intensive applications

### Error Messages

- **"Cannot open camera"**: Check camera connection and permissions
- **"No hands detected"**: Ensure hand is visible and well-lit
- **"Import error"**: Install missing dependencies with pip

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

## Safety Features

- **Fail-safe**: Move mouse to screen corner to stop
- **Emergency stop**: Press SPACE to disable control
- **Visual feedback**: See current gesture and status
- **Cooldown periods**: Prevent accidental rapid actions

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

## Contributing

Contributions are welcome! Areas for improvement:
- Additional gesture recognition
- Better performance optimization
- Cross-platform compatibility
- New control features
- Documentation improvements

## License

This project is open-source. Feel free to modify and distribute.

## Acknowledgments

- **MediaPipe**: Google's framework for hand tracking
- **OpenCV**: Computer vision library
- **PyAutoGUI**: Cross-platform GUI automation

## Support

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review configuration options
3. Test with different lighting conditions
4. Adjust sensitivity settings

---

**Note**: This application requires a webcam and works best with good lighting conditions. Always test in a safe environment before using with important applications.
