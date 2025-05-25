# FitDesk - Desktop Fitness Companion

Fitness at your finger tips

![image](https://github.com/user-attachments/assets/06969071-2eed-4195-8121-eac5308d038a)

FitDesk is a Windows application built with Python and Tkinter that helps you stay active while working at your desk. It provides guided exercises with real-time camera tracking, workout history tracking, and customizable settings.

## Features

- **Exercise Library**: Categorized workouts (Upper Body, Lower Body, Full Body)
- **Real-time Tracking**: Camera-based exercise monitoring with rep counting
- **Workout History**: Track your progress with weekly statistics
- **Customizable Interface**: Light/dark mode and adjustable goals
- **Audio Guidance**: Text-to-speech instructions for proper form

## Current Exercise Support

- **Shoulder Shrugs**: Tracks shoulder movements with MediaPipe pose detection
- *More exercises coming soon!*

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/FitDesk.git
   cd FitDesk

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Run the application:
   ```bash
   python app.py

## Requirements
  - Python 3.7+
  - OpenCV 
  - MediaPipe
  - PyTTSx3 
  - Pillow 

## How It Works

  1. Camera Integration: Uses OpenCV to capture webcam feed
  2. Pose Detection: Leverages MediaPipe for body landmark tracking
  3. Exercise Logic: Custom algorithms for each exercise (e.g., shoulder shrug detection)
  4. Tkinter UI: Clean interface with theme support

## Future Improvements

- Add more exercises (bicep curls, squats, etc.)
- Implement exercise GIF demonstrations
- Add user profiles and progress tracking
- Export workout history to CSV
- Mobile companion app integration

## Contributing
Contributions are welcome! Please open an issue or pull request for any:

>New exercises, UI improvements, Bug fixes
