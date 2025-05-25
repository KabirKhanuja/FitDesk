# 🏋️‍♂️ FitDesk

**FitDesk** is a Python-based virtual fitness assistant that guides users through physical exercises. It utilizes **MediaPipe**, **OpenCV**, and optionally **Streamlit** for the web interface.

## Features

- Pose detection using MediaPipe
- Virtual exercises with feedback
- Progress tracking (e.g. squat counter)
- Modular structure for adding new exercises

## Project Structure

Web.py # Main app script
assets/ # Icons, images
exercises/ # Exercise logic/scripts

## Installation

1. Clone the repository:

```bash
git clone https://github.com/KabirKhanuja/FitDesk.git
cd FitDesk


```

Install dependencies:

pip install -r requirements.txt
Run the app:

streamlit run Web.py
Screenshots
![image](https://github.com/user-attachments/assets/b1105ba6-7510-4d77-bc83-42cf96add4b3)

## License
© Kabir Khanuja


### `requirements.txt` (Auto-generated version)

If you want a quick version for now, based on your likely stack:

```txt
streamlit
opencv-python
mediapipe
numpy
To auto-generate from your local environment:
```

pip freeze > requirements.txt

Next Steps
 - Add a logo or banner to the top of your README
- Add demo screenshots (can capture the Streamlit UI)
- Consider adding .gitignore to exclude stuff like .DS_Store or __pycache__
- Add new features as separate commits (e.g. squat_counter, pose_feedback, etc.)

