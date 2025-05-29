import cv2
import mediapipe as mp
import numpy as np
import time
import pyttsx3
import sys
import math

def calculate_angle(a, b, c):
    """Calculate angle between three points."""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 170.0 / np.pi)
    if angle > 170.0:
        angle = 360 - angle
    return angle

def main(reps=10):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if "english" in voice.name.lower() and "female" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 175)

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)

    rep_count = 0
    stage = None  # 'up' or 'down'

    engine.say("Let's begin left arm bicep curls. Start with your right arm straight.")
    engine.runAndWait()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates for left arm
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * w,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * h]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h]

            # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)

            # Display angle
            cv2.putText(image, str(int(angle)),
                        tuple(np.multiply(elbow, [1, 1]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                        )

            # Bicep curl counter logic
            if angle > 160:
                stage = "down"
            if angle < 40 and stage == "down":
                stage = "up"
                rep_count += 1
                engine.say(f"Repetition {rep_count}")
                engine.runAndWait()

        except:
            pass

        cv2.putText(image, f"Reps: {rep_count}/{reps}", (10, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
        )

        cv2.imshow("Left Bicep Curl Tracker", image)

        if rep_count >= reps:
            engine.say("Exercise complete. Great job on your left arm!")
            engine.runAndWait()
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        reps = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    except ValueError:
        reps = 10
    main(reps=reps)
