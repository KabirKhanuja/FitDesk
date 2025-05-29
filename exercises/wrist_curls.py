import cv2
import mediapipe as mp
import numpy as np
import time
import pyttsx3

def main(reps=10):
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(0)
    rep_count = 0
    phase = "down"
    hold_time = None

    engine.say("Start wrist curl exercise by curling your wrist up and down.")
    engine.runAndWait()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                wrist_y = int(wrist.y * h)
                index_y = int(index_tip.y * h)
                diff = index_y - wrist_y

                # Visual aid
                cv2.line(frame, (0, wrist_y), (w, wrist_y), (255, 0, 0), 2)
                cv2.line(frame, (0, index_y), (w, index_y), (0, 255, 0), 2)

                if phase == "down" and diff < -30:  # hand moves up
                    phase = "up"
                    hold_time = time.time()

                elif phase == "up" and diff > -10:  # hand moves down
                    if time.time() - hold_time >= 0.5:
                        rep_count += 1
                        engine.say(f"Repetition {rep_count}")
                        engine.runAndWait()
                        phase = "down"

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.putText(frame, f"Reps: {rep_count}/{reps}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if rep_count >= reps:
            engine.say("Wrist curls completed. Great job!")
            engine.runAndWait()
            break

        cv2.imshow("Wrist Curl Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    import sys
    try:
        reps = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    except ValueError:
        reps = 10
    main(reps)

