import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time
import sys

def main(reps=10):
    engine = pyttsx3.init()
    for voice in engine.getProperty('voices'):
        if "english" in voice.name.lower() and "female" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 175)

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    rep_count = 0
    phase = "down"  # "up" when knee and elbow are close
    threshold_distance = 70  # pixels

    engine.say("Begin standing cross crunches. Lift your knee to opposite elbow.")
    engine.runAndWait()

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

            def get_coords(landmark):
                return int(lm[landmark].x * w), int(lm[landmark].y * h)

            # Get coordinates
            right_elbow = get_coords(mp_pose.PoseLandmark.RIGHT_ELBOW)
            left_elbow = get_coords(mp_pose.PoseLandmark.LEFT_ELBOW)
            right_knee = get_coords(mp_pose.PoseLandmark.RIGHT_KNEE)
            left_knee = get_coords(mp_pose.PoseLandmark.LEFT_KNEE)

            # Draw circles
            for point in [right_elbow, left_elbow, right_knee, left_knee]:
                cv2.circle(frame, point, 8, (255, 0, 255), -1)

            # Calculate distances
            dist1 = np.linalg.norm(np.array(right_elbow) - np.array(left_knee))
            dist2 = np.linalg.norm(np.array(left_elbow) - np.array(right_knee))

            # Show distances (for debugging)
            cv2.putText(frame, f"R-Elbow/L-Knee: {int(dist1)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
            cv2.putText(frame, f"L-Elbow/R-Knee: {int(dist2)}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

            # Rep detection logic
            if (dist1 < threshold_distance or dist2 < threshold_distance) and phase == "down":
                phase = "up"

            elif (dist1 > threshold_distance and dist2 > threshold_distance) and phase == "up":
                rep_count += 1
                phase = "down"
                engine.say(f"Repetition {rep_count}")
                engine.runAndWait()

        # Display rep count
        cv2.putText(frame, f"Reps: {rep_count}/{reps}", (30, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        # Stop condition
        if rep_count >= reps:
            engine.say("Exercise complete. Well done!")
            engine.runAndWait()
            break

        # Draw pose landmarks
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
        )

        cv2.imshow("Cross Crunch Tracker", frame)
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
