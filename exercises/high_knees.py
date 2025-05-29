import cv2
import mediapipe as mp
import numpy as np
import time
import pyttsx3
import threading

# Thread-safe TTS
def speak(text):
    def run():
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        voices = engine.getProperty('voices')
        for voice in voices:
            if "english" in voice.name.lower() and "female" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()

def main(reps_goal=20):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    rep_count = 0
    phase = "down"
    last_knee_up_time = time.time()

    speak("Start high knees when ready")

    def get_landmark_y(landmarks, index):
        return landmarks[index].y if index < len(landmarks) else 0

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

            # Get vertical positions
            left_hip_y = get_landmark_y(lm, mp_pose.PoseLandmark.LEFT_HIP.value)
            left_knee_y = get_landmark_y(lm, mp_pose.PoseLandmark.LEFT_KNEE.value)

            right_hip_y = get_landmark_y(lm, mp_pose.PoseLandmark.RIGHT_HIP.value)
            right_knee_y = get_landmark_y(lm, mp_pose.PoseLandmark.RIGHT_KNEE.value)

            avg_hip_y = (left_hip_y + right_hip_y) / 2

            # Check if either knee is lifted above hip
            knee_up = left_knee_y < avg_hip_y - 0.05 or right_knee_y < avg_hip_y - 0.05

            current_time = time.time()
            if knee_up and phase == "down" and (current_time - last_knee_up_time > 0.4):
                rep_count += 1
                speak(f"{rep_count}")
                last_knee_up_time = current_time
                phase = "up"
            elif not knee_up and phase == "up":
                phase = "down"

            # Draw pose
            mp.solutions.drawing_utils.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Show rep count
        cv2.putText(frame, f"Reps: {rep_count}/{reps_goal}", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 5)

        cv2.imshow("High Knees Counter", frame)

        if rep_count >= reps_goal:
            speak("Workout complete! Well done.")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(reps_goal=20)
