import cv2
import mediapipe as mp


def count_fingers(hand_landmarks):
    finger_count = 0
    if (
        hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].x
        < hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_IP].x
    ):
        finger_count += 1

    # Other 4 fingers: Check if tip is above (smaller y-coordinate) the PIP joint
    # Index finger
    if (
        hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y
        < hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_PIP].y
    ):
        finger_count += 1
    # Middle finger
    if (
        hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP].y
        < hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ):
        finger_count += 1
    # Ring finger
    if (
        hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP].y
        < hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_PIP].y
    ):
        finger_count += 1
    # Pinky finger
    if (
        hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP].y
        < hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_PIP].y
    ):
        finger_count += 1

    return finger_count


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# For webcam input:
cap = cv2.VideoCapture(0)  # 0 for default webcam

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip the image horizontally for a mirror-like display, and convert the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        finger_count = 0
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
                finger_count = count_fingers(
                    hand_landmarks
                )  # Assuming only one hand for simplicity for now

        cv2.putText(
            image,
            f"Fingers: {finger_count}",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        cv2.imshow("Hand Gesture Recognition", image)
        if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
            break

cap.release()
cv2.destroyAllWindows()
