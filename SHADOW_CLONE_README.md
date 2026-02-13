# Shadow Clone Jutsu - Hand Gesture Demo

Experience Naruto's iconic Shadow Clone Jutsu in real life! This demo uses computer vision to detect when you make the crossed-hand seal and creates visual clones of yourself on screen.

## 🎯 What It Does

When you cross your hands like Naruto's Shadow Clone hand seal, the system:
- Detects the crossed-hand gesture using your webcam
- Creates 4 clones of your video feed positioned around you
- Displays "SHADOW CLONE JUTSU!" text with effects
- Clones fade in and out smoothly over 3 seconds

## 📋 Requirements

- Python 3.7 or higher
- Webcam
- Required Python packages (see Installation)

## 🚀 Installation

1. **Activate your virtual environment (if using one):**

```bash
# On Windows PowerShell
.\venv\Scripts\Activate.ps1

# On Windows CMD
.\venv\Scripts\activate.bat

# On Linux/Mac
source venv/bin/activate
```

2. **Install required packages:**

```bash
pip install opencv-python mediapipe "numpy<2"
```

**Important:** Use `numpy<2` to avoid compatibility issues with mediapipe and tensorflow.

If you encounter errors, try:

```bash
pip uninstall numpy
pip install "numpy<2"
```

## ▶️ How to Run

Simply run the demo script:

```bash
python shadow_clone_demo.py
```

## 🎮 How to Use

1. **Position yourself** in front of your webcam
2. **Show both hands** to the camera (make sure both are visible)
3. **Cross your hands** like the Shadow Clone seal:
   - Place one hand horizontally
   - Cross the other hand over it vertically
   - Keep fingers extended
   - Hands should overlap in the middle
4. **Watch the magic happen!** Clones will appear around you

### Reference Image
The hand position should look like this:
- One hand horizontal (like making a "stop" gesture)
- Other hand vertical crossing over it
- Fingers pointing in opposite directions
- Similar to making a "+" or cross shape with your hands

## ⌨️ Controls

- **ESC** - Exit the application
- **SPACE** - Manually trigger the effect (useful for testing)

## 📊 On-Screen Information

The demo displays:
- **Hands status** - Shows if hands are detected
- **Seal detected** - Indicates when the crossed-hand seal is recognized
- **Effect active** - Shows when clones are being displayed
- **Cooldown timer** - 4-second cooldown between activations
- **FPS counter** - Performance indicator

## ⚙️ Customization

You can modify the effect in `shadow_clone_demo.py`:

```python
# Change number of clones (default: 4)
shadow_clone = ShadowCloneEffect(num_clones=6, effect_duration=3.0)

# Change effect duration (default: 3.0 seconds)
shadow_clone = ShadowCloneEffect(num_clones=4, effect_duration=5.0)

# Change cooldown between activations (default: 4.0 seconds)
cooldown_duration = 6.0
```

## 🔧 Troubleshooting

### Hands not detected
- Ensure good lighting
- Keep hands within camera frame
- Try adjusting distance from camera

### Seal not triggering
- Make sure both hands are clearly visible
- Cross hands more distinctly
- Keep hands at similar vertical height
- Ensure hands overlap in the middle

### Low FPS / Laggy
- Close other applications
- Reduce camera resolution in code
- Reduce number of clones

### Camera not opening
- Check if another application is using the camera
- Try changing camera ID in code: `cv2.VideoCapture(1)` instead of `0`

## 📁 Files

- `shadow_clone_demo.py` - Main demo application
- `shadow_clone_effect.py` - Clone effect implementation
- `hand_tracker.py` - Hand detection using MediaPipe (existing file)
- `SHADOW_CLONE_README.md` - This file

## 🎨 Technical Details

- Uses MediaPipe for hand landmark detection
- Detects 2 hands simultaneously
- Analyzes hand positions to identify crossed-hand seal
- Creates scaled and positioned clones using OpenCV
- Smooth fade in/out effects with alpha blending

## 💡 Tips

- Practice the hand seal a few times to get the positioning right
- Keep your hands steady when making the seal
- The effect has a cooldown to prevent spam
- Good lighting improves detection accuracy
- Position yourself centered in the frame for best results

## 🎬 Demo Features

- Real-time hand tracking visualization
- Automatic seal detection
- Smooth clone animations
- "SHADOW CLONE JUTSU!" text overlay
- Cooldown system
- Manual trigger option
- FPS monitoring

## 🐛 Known Issues

- May require good lighting conditions
- Hand detection can be sensitive to background
- Performance depends on your computer's capabilities

## 📝 Notes

- This demo does NOT modify your existing hand gesture control code
- All new functionality is in separate files
- Original `main.py` and other files remain unchanged
- Can run alongside your existing gesture control system

---

**Believe it!** 🍥

Enjoy your Shadow Clone Jutsu experience!
