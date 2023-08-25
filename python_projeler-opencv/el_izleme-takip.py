import cv2
import mediapipe as mp

# Mediapipe kütüphanesi için gerekli nesneleri hazırla
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# İşlenecek görüntü dosyaları listesi
IMAGE_FILES = []

# Resim dosyaları için Hands modunu kullanarak
# en fazla n eli algılayan  bir döngü oluştur
with mp_hands.Hands(
    static_image_mode=True,  # Resim modu
    max_num_hands=2,          # En fazla n el
    min_detection_confidence=0.5) as hands:
    
    # IMAGE_FILES listesindeki her bir dosya için işlem yap
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.flip(cv2.imread(file), 1)
        # El algılama işlemini gerçekleştir
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        print('El Handedness (Sağ/Sol):', results.multi_handedness)
        
        # Eğer el bulunamazsa devam et
        if not results.multi_hand_landmarks:
            continue
        
        image_height, image_width, _ = image.shape
        
        annotated_image = image.copy()
        
        # Her bir elin el işaret noktalarını işaretle
        for hand_landmarks in results.multi_hand_landmarks:
            print('El İşaret Noktaları:', hand_landmarks)
            index_finger_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width
            index_finger_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height
            print(
                f'İşaret parmağı ucu koordinatları: (',
                f'{index_finger_tip_x}, {index_finger_tip_y})'
            )
            
            mp_drawing.draw_landmarks(
                annotated_image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        
        cv2.imwrite(
            '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        
        if not success:
            print("Boş kamera çerçevesi alınıyor.")
            continue
        
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        
        image.flags.writeable = False
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x, y = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y
                x1, y1 = hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y

                font = cv2.FONT_HERSHEY_PLAIN
                
                # İşaret ve başparmak açıkken "OLUMSUZ" yazdır, aksi halde "OLUMLU" yazdır
                if y1 > y:
                    cv2.putText(image, "OLUMSUZ", (10, 50), font, 4, (0, 0, 0), 3)
                else:
                    cv2.putText(image, "OLUMLU", (10, 50), font, 4, (0, 0, 0), 3)
                
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        
        cv2.imshow('MediaPipe Hands', image)
        
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
