import cv2
import easyocr

reader = easyocr.Reader(['tr']) #Dil Seçimi

cap = cv2.VideoCapture(0)

#Sonuçları kaydetme işlemi
with open('metin_sonuclari.txt', 'w') as file:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        #Metin tespiti
        results = reader.readtext(frame)

        min_probability = 0.5  #olasılık eşiği

        for (bbox, text, prob) in results:
            if prob >= min_probability:
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = tuple(map(int, top_left))
                bottom_right = tuple(map(int, bottom_right))

                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                cv2.putText(frame, f'{text} ({prob:.2f})', (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                file.write(f'{text} ({prob:.2f})\n')

        cv2.imshow('Metin Tespiti', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

file.close()

cap.release()
cv2.destroyAllWindows()
