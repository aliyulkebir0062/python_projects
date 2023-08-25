import cv2
import numpy as np
from mediapipe.python import mediapipe

mp_drawing = mediapipe.solutions.drawing_utils
mp_hands = mediapipe.solutions.hands

hands = mp_hands.Hands()

keyboard = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']]

keyboard_x = 100
keyboard_y = 100
key_width = 50
key_height = 50
key_spacing = 20

cap = cv2.VideoCapture(0)

new_width = 860
new_height = 640

prev_landmarks = []
selected_key = None
last_selected_key = None

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.resize(image, (new_width, new_height))

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, c = image.shape
            landmarks = []
            for landmark in hand_landmarks.landmark:
                x = min(int(landmark.x * w), w - 1)
                y = min(int(landmark.y * h), h - 1)
                landmarks.append((x, y))

            prev_landmarks.append(landmarks)
            if len(prev_landmarks) > 5:
                prev_landmarks.pop(0)

            averaged_landmarks = np.mean(prev_landmarks, axis=0)

            for i, row in enumerate(keyboard):
                for j, key in enumerate(row):
                    x1 = keyboard_x + j * (key_width + key_spacing)
                    y1 = keyboard_y + i * (key_height + key_spacing)
                    x2 = x1 + key_width
                    y2 = y1 + key_height

                    distance = np.linalg.norm(np.array(averaged_landmarks[8]) - np.array([(x1 + x2) // 2, (y1 + y2) // 2]))

                    sensitivity_factor = 0.8
                    if distance < key_width * sensitivity_factor:
                        selected_key = key
                        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(image, key, (x1 + 10, y1 + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.putText(image, key, (x1 + key_width // 2 - 10, y1 + key_height // 2 + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                    else:
                        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        cv2.putText(image, key, (x1 + 10, y1 + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    if selected_key != last_selected_key and selected_key is not None:
        selected_text = selected_key
        print("Seçilen tuş:", selected_key)
        last_selected_key = selected_key

    cv2.imshow('Virtual Keyboard', image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
