import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.say(text)
    engine.runAndWait()

def calc_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return angle

def main(max_reps=10):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

    cap = cv2.VideoCapture(0)
    time.sleep(2)  # Allow camera to warm up

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        speak("Camera failed to open. Please check and restart.")
        return

    rep_count = 0
    stage = "up"
    last_rep_time = time.time()
    speak("Start squats. Go down fully and come back up.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from camera.")
            speak("Could not read from camera. Exiting.")
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            def get_coords(index):
                return [lm[index].x * w, lm[index].y * h]

            # Right side
            r_hip = get_coords(mp_pose.PoseLandmark.RIGHT_HIP.value)
            r_knee = get_coords(mp_pose.PoseLandmark.RIGHT_KNEE.value)
            r_ankle = get_coords(mp_pose.PoseLandmark.RIGHT_ANKLE.value)

            # Left side
            l_hip = get_coords(mp_pose.PoseLandmark.LEFT_HIP.value)
            l_knee = get_coords(mp_pose.PoseLandmark.LEFT_KNEE.value)
            l_ankle = get_coords(mp_pose.PoseLandmark.LEFT_ANKLE.value)

            r_angle = calc_angle(r_hip, r_knee, r_ankle)
            l_angle = calc_angle(l_hip, l_knee, l_ankle)
            avg_angle = (r_angle + l_angle) / 2

            current_time = time.time()

            if avg_angle < 85 and stage == "up":
                stage = "down"

            elif avg_angle > 165 and stage == "down":
                if current_time - last_rep_time > 0.6:
                    stage = "up"
                    rep_count += 1
                    speak(f"Repetition {rep_count}")
                    last_rep_time = current_time

            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            cv2.putText(frame, f"Avg Angle: {int(avg_angle)}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)

        cv2.putText(frame, f"Squats: {rep_count}/{max_reps}", (10, h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        cv2.imshow("Squat Tracker", frame)

        if rep_count >= max_reps:
            speak("Workout complete. Great job!")
            time.sleep(2)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            speak("Exercise stopped.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(max_reps=10)
