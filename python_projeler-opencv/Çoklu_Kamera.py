import cv2
import winsound
import time
from datetime import datetime

frekans = 600
süre = 1000
ses_aralığı = 14

output_file1 = 'kayit_kamera1.mp4'
output_file2 = 'kayit_kamera2.mp4'
fps = 80
frame_width = 860
frame_height = 640

video1 = cv2.VideoCapture(0)
video2 = cv2.VideoCapture(1)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out1 = cv2.VideoWriter(output_file1, fourcc, fps, (frame_width, frame_height))
out2 = cv2.VideoWriter(output_file2, fourcc, fps, (frame_width, frame_height))

ret1, frame1 = video1.read()
ret2, frame2 = video2.read()

prev_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
prev_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

motion_detected1 = False
motion_detected2 = False

last_sound_time = time.time()

draw_motion_lines = True

active_camera = 1  

while True:
    if active_camera == 1:
        ret, frame = video1.read()
        current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        prev_frame = prev_frame1
        motion_detected = motion_detected1
        out = out1
        window_name = "Hareket Algılama - Kamera 1"
    else:
        ret, frame = video2.read()
        current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        prev_frame = prev_frame2
        motion_detected = motion_detected2
        out = out2
        window_name = "Hareket Algılama - Kamera 2"

    frame_diff = cv2.absdiff(prev_frame, current_frame)

    _, threshold = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 500:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
            motion_detected = True

            if draw_motion_lines:
                cv2.drawContours(frame, [contour], 0, (0, 0, 255), 2)

    if motion_detected:
        current_time = time.time()
        time_difference = current_time - last_sound_time
        if time_difference >= ses_aralığı:
            winsound.Beep(frekans, süre)
            last_sound_time = current_time
        motion_detected = False

        print("Hareket Algılandı - Kamera", active_camera)

    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, current_datetime, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    out.write(frame)

    cv2.imshow(window_name, frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('s'):
        draw_motion_lines = not draw_motion_lines
    elif key == ord('1'):
        active_camera = 1
    elif key == ord('2'):
        active_camera = 2

    if active_camera == 1:
        prev_frame1 = current_frame
        motion_detected1 = motion_detected
    else:
        prev_frame2 = current_frame
        motion_detected2 = motion_detected

out1.release()
out2.release()
video1.release()
video2.release()
cv2.destroyAllWindows()
