import cv2
import mediapipe as mp
import numpy as np
import time
import pyttsx3
import sys
import math

def calculate_angle(a, b, c):
    """Calculates the angle between three points (shoulder, elbow, wrist)"""
    a = np.array(a)  # Shoulder
    b = np.array(b)  # Elbow
    c = np.array(c)  # Wrist

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
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

    engine.say("Start your right arm bicep curls when you're ready.")
    engine.runAndWait()

    rep_count = 0
    direction = "down"  # Possible values: 'up' or 'down'
    angle = 0
    went_low = False
    prev_angle = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates for right shoulder, elbow, and wrist
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h]
            elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x * w,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y * h]
            wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x * w,
                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y * h]

            # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)

            # Only proceed if there's meaningful change
            if abs(angle - prev_angle) > 5:
                # Display angle
                cv2.putText(frame, f'Angle: {int(angle)}', 
                            (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

                # Curl logic
                if angle > 160:
                    if direction == "up":
                        if went_low:  # Only count if we passed through low point
                            rep_count += 1
                            direction = "down"
                            went_low = False
                            engine.say(f"Repetition {rep_count}")
                            engine.runAndWait()

                elif angle < 40:
                    if direction == "down":
                        direction = "up"
                        went_low = True  # We passed the deep curl

            prev_angle = angle

        # Display count
        cv2.putText(frame, f'Reps: {rep_count}/{reps}', 
                    (50, h - 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Draw landmarks
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                                      mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))

        cv2.imshow("Right Arm Bicep Curl Tracker", frame)

        if rep_count >= reps:
            engine.say("Exercise completed. Well done!")
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
