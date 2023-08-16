import cv2

def zoom_in(image, scale_factor):
    # Görüntüyü yakınlaştırır
    height, width = image.shape[:2]
    new_height, new_width = int(height * scale_factor), int(width * scale_factor)
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    # Yakınlaştırılan görüntüyü ortalamak için yeni pencere açar
    start_x = (new_width - width) // 2
    start_y = (new_height - height) // 2
    end_x = start_x + width
    end_y = start_y + height
    zoomed_image = resized_image[start_y:end_y, start_x:end_x]
    
    return zoomed_image

video = cv2.VideoCapture(0)

# Video kaydetme ayarları
output_file = 'kayit.mp4'
fps = 40  
frame_width = int(video.get(3))
frame_height = int(video.get(4))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

ret, frame = video.read()
prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

recording = False  # Kayıt yapma bayrağı

while True:
    ret, frame = video.read()
    
    current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    frame_diff = cv2.absdiff(prev_frame, current_frame)
    
    _, threshold = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    motion_detected = False  # Hareket algılandı bayrağı
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area > 700:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            motion_detected = True
    
    zoomed_frame = zoom_in(frame, 1.8)  # Yakınlaştırma işlemi
    zoomed_frame = cv2.resize(zoomed_frame, (860, 640))  # Yeni boyutları belirleme

    
    cv2.imshow("Hareket Algılama", frame)
    cv2.imshow("Zoom", zoomed_frame)  
    
    # Hareket algılandıysa ve kayıt yapma bayrağı açıksa çerçeveyi videoya kaydet
    if motion_detected and recording:
        out.write(frame)
        out.write(frame)
        cv2.imshow("Kayit", frame)
    
    key = cv2.waitKey(1)
    
    if key == ord('q'):
        break
    elif key == ord('r'):  # Kayıt yapma aç veya kapat
        recording = not recording
    
    prev_frame = current_frame

video.release()
out.release()
cv2.destroyAllWindows()
