import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time

def calculate_angle(a, b, c):
    """Returns angle in degrees between three points"""
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180.0 else angle

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'english' in voice.name.lower() and 'female' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

def main():
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    timer_started = False
    start_time = 0

    speak("Get into Tree Pose with your right leg bent. Timer will start once pose is detected.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            # Get key landmark coordinates
            right_hip = [lm[mp_pose.PoseLandmark.RIGHT_HIP].x * w, lm[mp_pose.PoseLandmark.RIGHT_HIP].y * h]
            right_knee = [lm[mp_pose.PoseLandmark.RIGHT_KNEE].x * w, lm[mp_pose.PoseLandmark.RIGHT_KNEE].y * h]
            right_ankle = [lm[mp_pose.PoseLandmark.RIGHT_ANKLE].x * w, lm[mp_pose.PoseLandmark.RIGHT_ANKLE].y * h]
            right_shoulder = [lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w, lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h]

            left_hip = [lm[mp_pose.PoseLandmark.LEFT_HIP].x * w, lm[mp_pose.PoseLandmark.LEFT_HIP].y * h]
            left_knee = [lm[mp_pose.PoseLandmark.LEFT_KNEE].x * w, lm[mp_pose.PoseLandmark.LEFT_KNEE].y * h]
            left_ankle = [lm[mp_pose.PoseLandmark.LEFT_ANKLE].x * w, lm[mp_pose.PoseLandmark.LEFT_ANKLE].y * h]

            # Calculate angles
            right_leg_angle = calculate_angle(right_hip, right_knee, right_ankle)
            left_leg_straight_angle = calculate_angle(left_hip, left_knee, left_ankle)
            right_hip_knee_out_angle = calculate_angle(right_shoulder, right_hip, right_knee)

            # Display angles
            cv2.putText(frame, f'Right Leg Angle: {int(right_leg_angle)}', (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            cv2.putText(frame, f'Left Leg Angle: {int(left_leg_straight_angle)}', (30, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 200, 0), 2)

            # Improved Tree Pose detection logic
            ankle_near_thigh = abs(right_ankle[1] - left_knee[1]) < 80 and abs(right_ankle[0] - left_knee[0]) < 100
            right_knee_out = right_hip_knee_out_angle > 40
            left_leg_straight = left_leg_straight_angle > 160

            if ankle_near_thigh and right_knee_out and left_leg_straight:
                if not timer_started:
                    speak("Pose detected. Starting timer.")
                    timer_started = True
                    start_time = time.time()

                elapsed = int(time.time() - start_time)
                remaining = max(0, 60 - elapsed)

                cv2.putText(frame, f'Time left: {remaining}s', (30, 130),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                if elapsed == 45:
                    speak("Almost there, keep holding.")

                if elapsed >= 60:
                    speak("One minute completed. Great job!")
                    break
            else:
                if timer_started:
                    cv2.putText(frame, "Pose lost. Resetting timer.", (30, 130),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    timer_started = False
                    speak("Pose lost. Please get back into Tree Pose.")

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow("Tree Pose - Right Leg", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
