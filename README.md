# GestureMacroApp
A Python application that lets you control your PC and create macros based on hand gestures detected via your webcam. Uses MediaPipe for gesture detection and pynput for media key control.

## Features
- Detects gestures like open palm, peace sign, fist, open index finger, and more
- Swipe gestures (open palm left/right) for next/previous track
- Circular gestures (with index finger) for volume control
- Easily extendable with new gesture patterns

## Requirements
- Python 3.8+
- pip
- Webcam

## Installation
1. Clone this repository or copy the files to your project directory.
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage
Run the main controller script:

```bash
python main.py
```

## Notes
- On macOS, you may need to grant accessibility permissions to Python for media key control.
- For best results, use in a well-lit environment with your hand clearly visible to the camera.
- You can adjust the camera resolution in `video_capturer.py`.

