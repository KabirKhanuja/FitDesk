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

    engine.say("Sit or stand straight for neck tilt calibration.")
    engine.runAndWait()

    left_limit = None
    right_limit = None
    rep_count = 0
    calibrating = False
    calibration_complete = False
    start_time = None
    last_rep_time = 0
    cooldown = 1.0  # seconds before counting next rep
    last_side = None  # track last side to avoid double count

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
            nose_x = int(landmarks[mp_pose.PoseLandmark.NOSE].x * w)
            left_shoulder_x = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w)
            right_shoulder_x = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w)
            center_x = (left_shoulder_x + right_shoulder_x) // 2
            offset = nose_x - center_x

            if not calibrating and not calibration_complete:
                engine.say("Hold your head straight for 5 seconds.")
                engine.runAndWait()
                calibrating = True
                start_time = time.time()

            if calibrating and not calibration_complete:
                cv2.putText(frame, "Hold your head straight...", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                if time.time() - start_time > 5:
                    engine.say("Now tilt your head left and hold for 5 seconds.")
                    engine.runAndWait()
                    left_limit = offset
                    start_time = time.time()
                    calibration_complete = "left"

            elif calibration_complete == "left":
                cv2.putText(frame, "Hold left tilt...", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                if offset < left_limit:
                    left_limit = offset
                if time.time() - start_time > 5:
                    engine.say("Now tilt your head right and hold for 5 seconds.")
                    engine.runAndWait()
                    right_limit = offset
                    start_time = time.time()
                    calibration_complete = "right"

            elif calibration_complete == "right":
                cv2.putText(frame, "Hold right tilt...", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                if offset > right_limit:
                    right_limit = offset
                if time.time() - start_time > 5:
                    engine.say("Calibration complete. Start tilting your neck.")
                    engine.runAndWait()
                    calibration_complete = True

            if calibration_complete is True:
                cv2.line(frame, (center_x + left_limit, 0), (center_x + left_limit, h), (0, 255, 0), 2)
                cv2.line(frame, (center_x + right_limit, 0), (center_x + right_limit, h), (0, 255, 0), 2)

                current_time = time.time()
                # Check left tilt
                if offset < left_limit + 20:
                    if last_side != "left" and (current_time - last_rep_time) > cooldown:
                        rep_count += 1
                        engine.say(f"Repetition {rep_count}")
                        engine.runAndWait()
                        last_rep_time = current_time
                        last_side = "left"
                # Check right tilt
                elif offset > right_limit - 20:
                    if last_side != "right" and (current_time - last_rep_time) > cooldown:
                        rep_count += 1
                        engine.say(f"Repetition {rep_count}")
                        engine.runAndWait()
                        last_rep_time = current_time
                        last_side = "right"
                else:
                    # Head is near center, reset last_side to allow next rep on either side
                    last_side = None

        else:
            cv2.putText(frame, "Ensure your head and shoulders are visible!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(frame, f"Reps: {rep_count}/{reps}", (50, h - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if rep_count >= reps:
            engine.say("Exercise complete. Great job!")
            engine.runAndWait()
            break

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                                  mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))

        cv2.imshow("Neck Tilt Tracker", frame)

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
