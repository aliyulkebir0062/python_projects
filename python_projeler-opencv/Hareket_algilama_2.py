import cv2
import winsound
import pyttsx3
import time

# Uyarı sesinin ayarları
frekans = 900
süre = 1000
ses_cikarma_suresi = 15  # Ses çıkarma süresi

output_file = 'kayit4.mp4'
fps = 25  # Video çerçeve hızı
frame_width = 860
frame_height = 480

video = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

ret, frame = video.read()
prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
motion_detected = False
start_time = time.time()

#Metin konuşma motorunu başlat
engine = pyttsx3.init()

engine.setProperty('voice', 'tr')  # Türkçe ses kullanımı
engine.setProperty('encoding', 'utf-8')

while True:
    ret, frame = video.read()

    current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame_diff = cv2.absdiff(prev_frame, current_frame)

    _, threshold = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(
        threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            motion_detected = True  # Hareket algılandı

    # Video işlemi ve sesli uyarı
    if motion_detected:
        if time.time() - start_time >= ses_cikarma_suresi:
            winsound.Beep(frekans, süre)
            out.write(frame)
            motion_detected = False
            # print("Hareket algılandı!")
            engine.say("Hareket algılandı!") 
            engine.runAndWait()
            start_time = time.time()

    cv2.imshow("Hareket Algılama", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    prev_frame = current_frame

out.release()
video.release()
cv2.destroyAllWindows()
