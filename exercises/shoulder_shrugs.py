import cv2
import mediapipe as mp
import numpy as np
import time
import pyttsx3
import sys

def main(reps=10):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if "english" in voice.name.lower() and "female" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 175)

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)

    engine.say("Stand straight and keep your shoulders relaxed for calibration.")
    engine.runAndWait()

    start_line = None
    shrugged_line = None
    rep_count = 0
    phase = "start"
    body_detected = False
    start_time = None
    calibrating = False
    calibration_complete = False
    hold_time = None

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
            right_shoulder_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h)
            left_shoulder_y = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h)
            avg_shoulder_y = (right_shoulder_y + left_shoulder_y) // 2
            body_detected = True

            if not calibrating and not calibration_complete:
                engine.say("Hold still to set your resting shoulder position for 5 seconds.")
                engine.runAndWait()
                calibrating = True
                start_time = time.time()

            if calibrating and not calibration_complete:
                cv2.putText(frame, "Hold still to set resting shoulder position...", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                if time.time() - start_time > 5:
                    start_line = avg_shoulder_y - 20 
                    engine.say("Now, shrug your shoulders up and hold for 5 seconds.")
                    engine.runAndWait()
                    start_time = time.time()
                    calibrating = False
                    calibration_complete = "shrugged"

            elif calibration_complete == "shrugged":
                cv2.putText(frame, "Hold shrugged position for 5 seconds...", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                if shrugged_line is None or avg_shoulder_y < shrugged_line:
                    shrugged_line = avg_shoulder_y + 10

                if time.time() - start_time > 5:
                    calibration_complete = True
                    engine.say("Calibration complete. Start shrugging your shoulders.")
                    engine.runAndWait()

        else:
            body_detected = False
            cv2.putText(frame, "Ensure your upper body is in frame!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if start_line and shrugged_line:
            cv2.line(frame, (50, start_line), (w - 50, start_line), (255, 0, 0), 2) 
            cv2.line(frame, (50, shrugged_line), (w - 50, shrugged_line), (0, 255, 0), 2)  

            if phase == "start" and avg_shoulder_y >= start_line - 5:
                phase = "up"

            elif phase == "up" and avg_shoulder_y <= shrugged_line + 5:
                hold_time = time.time()
                phase = "hold"

            elif phase == "hold" and time.time() - hold_time >= 0.5:
                phase = "down"

            elif phase == "down" and avg_shoulder_y >= start_line - 5:
                rep_count += 1
                phase = "start"
                engine.say(f"Repetition {rep_count}")
                engine.runAndWait()

        cv2.putText(frame, f"Reps: {rep_count}/{reps}",
                    (50, h - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if rep_count >= reps:
            engine.say("Exercise completed. Great job!")
            engine.runAndWait()
            break

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))

        cv2.imshow("Shoulder Shrug Tracker", frame)

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
