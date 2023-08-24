"""
Es una tarea dada el 24/08
La computadora al reconocer una mano, abre una ventana nueva mostrando unicamente la mano
"""


import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()



cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB (MediaPipe uses RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Do something with the hand landmarks (landmarks are in normalized coordinates)

            # Convert normalized landmarks to pixel coordinates
            h, w, c = frame.shape
            hand_landmarks = []
            landmark = landmarks.landmark
            x_max, y_max = int(landmark[0].x * w), int(landmark[0].y * h)
            x_min, y_min = int(landmark[0].x * w), int(landmark[0].y * h)
            for lm in landmarks.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                if x<0 or y<0:
                    break
                if x>x_max:
                    x_max = x
                if x<x_min:
                    x_min = x
                if y>y_max:
                    y_max = y
                if y<y_min:
                    y_min=y

            # Draw landmarks on the frame
            if y_min<y_max and x_min < x_max:
                roi = frame[y_min: y_max, x_min: x_max]
                print(f"x:{x_min}: {x_max} --- y = {y_min}:{y_max}")
                cv2.imshow("Mano", roi)

    elif  cv2.getWindowProperty("Mano", cv2.WND_PROP_VISIBLE):
        cv2.destroyWindow("Mano")


    # Display the frame with landmarks
    cv2.imshow("Video", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()