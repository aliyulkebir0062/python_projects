import cv2
import os
import pygame

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

alert_sound = 'sesdosyası.mp3'
video_capture = cv2.VideoCapture(0)

eye_aspect_ratio_threshold = 0.60
consecutive_frames_threshold = 20

consecutive_frames = 0
sleepy_state = False

pygame.init()

record = False
output_filename = 'kayit.mp4'
frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 30.0
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

            eye_aspect_ratio = (ew / float(w) + eh / float(h)) / 2.0

            if eye_aspect_ratio < eye_aspect_ratio_threshold:
                consecutive_frames += 1
            else:
                consecutive_frames = 0

            if consecutive_frames >= consecutive_frames_threshold:
                sleepy_state = True
                cv2.putText(frame, "uykulu surucu", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                if os.path.exists(alert_sound):
                    pygame.mixer.music.load(alert_sound)
                    pygame.mixer.music.play()

    cv2.imshow('Görüntü', frame)


    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        if record:
            record = False
            video_writer.release()
            print("Kayıt durduruldu.")
        else:
            record = True
            video_writer = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))
            print("Kayıt başladı.")

    if record:
        video_writer.write(frame)

video_capture.release()
cv2.destroyAllWindows()

pygame.quit()
