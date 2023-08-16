import cv2
import os

video = cv2.VideoCapture('istock.mp4')
car_cascade = cv2.CascadeClassifier('haarcascade_car.xml')
backsub = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=50, detectShadows=True)

rois = []

save_dir = 'algilanan_arabalar'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

new_width = 800
new_height = 600

while True:
    ret, frames = video.read()

    if not ret:
        break

    if frames is None or frames.shape[0] == 0 or frames.shape[1] == 0:
        break

    if len(rois) < 2:
        roi_box = cv2.selectROI('Select ROI', frames)
        if roi_box[2] > 0 and roi_box[3] > 0:
            rois.append(roi_box)

    fgmask = backsub.apply(frames)

    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

    for roi_box in rois:
        roi_x, roi_y, roi_width, roi_height = roi_box

        roi = gray[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
        cars = car_cascade.detectMultiScale(roi, 1.7, 3)

        for (x, y, w, h) in cars:
            x += roi_x
            y += roi_y
            plate = frames[y:y+h, x:x+w]
            cv2.rectangle(frames, (x, y), (x+w, y+h), (51, 51, 255), 2)
            cv2.rectangle(frames, (x, y-40), (x+w, y), (51, 51, 255), -2)
            cv2.putText(frames, 'Car', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            resized_plate = cv2.resize(plate, (new_width, new_height))
            cv2.imshow('car', resized_plate)

            # Tespit edilen aracın fotoğrafını kaydet
            save_path = os.path.join(save_dir, f'car_{x}_{y}.jpg')
            cv2.imwrite(save_path, resized_plate)

    lab1 = "Araba Sayisi: " + str(len(rois))
    cv2.putText(frames, lab1, (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (147, 20, 255), 3)
    resized_frames = cv2.resize(frames, (new_width, new_height))
    cv2.imshow('Arac Tespit Sistemi', resized_frames)

    fgmask = cv2.GaussianBlur(fgmask, (5, 5), 0)

    cv2.imshow('fgmask', fgmask)
    cv2.resizeWindow('Arac Tespit Sistemi', new_width, new_height)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
