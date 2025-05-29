import cv2
import mediapipe as mp
import numpy as np
import time
import pyttsx3
import math

def calculate_angle(a, b, c):
    """Returns the angle between three points in degrees."""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180:
        angle = 360 - angle
    return angle

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    voices = engine.getProperty('voices')
    for voice in voices:
        if "english" in voice.name.lower() and "female" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    timer_started = False
    start_time = 0

    speak("Get into Cobra Pose position. Timer will begin when pose is detected.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Define key points for neck and back angles
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h]
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * w,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * h]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x * w,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y * h]

            nose = [landmarks[mp_pose.PoseLandmark.NOSE].x * w,
                    landmarks[mp_pose.PoseLandmark.NOSE].y * h]
            back_angle = calculate_angle(knee, hip, shoulder)
            neck_angle = calculate_angle(shoulder, hip, nose)

            # Display angles
            cv2.putText(frame, f'Back: {int(back_angle)} deg', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            cv2.putText(frame, f'Neck: {int(neck_angle)} deg', (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 200, 0), 2)

            # Start timer when both angles indicate a cobra pose
            if back_angle > 130 and neck_angle < 70:
                if not timer_started:
                    speak("Pose detected. Starting timer.")
                    timer_started = True
                    start_time = time.time()
                elapsed = int(time.time() - start_time)

                # Timer text
                remaining = max(0, 60 - elapsed)
                cv2.putText(frame, f'Time left: {remaining}s', (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                if elapsed == 45:
                    speak("Almost there, keep holding.")

                if elapsed >= 60:
                    speak("One minute completed. Great job!")
                    break

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow("Cobra Pose Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
