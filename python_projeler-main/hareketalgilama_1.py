import cv2
import winsound
import time

# Uyarı sesinin ayarları
frekans = 600 
süre = 1000  
ses_aralığı = 14  #ses aralığı

output_file = 'kayit.mp4'  
fps = 80  # Video çerçeve hızı
frame_width = 860 
frame_height = 640 

video = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

ret, frame = video.read()
prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
motion_detected = False
last_sound_time = time.time()

while True:
    ret, frame = video.read()
    
    current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    frame_diff = cv2.absdiff(prev_frame, current_frame)
    
    _, threshold = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area > 500:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)
            motion_detected = True  # Hareket algılandı
    
    # Hareket algılandığında videoya kaydet
    if motion_detected:
        current_time = time.time()
        time_difference = current_time - last_sound_time
        if time_difference >= ses_aralığı:
            winsound.Beep(frekans, süre)
            last_sound_time = current_time
        out.write(frame)  # Çerçeveyi videoya kaydet
        motion_detected = False  
    
    cv2.imshow("Hareket Algılama", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    prev_frame = current_frame

out.release()
video.release()
cv2.destroyAllWindows()
