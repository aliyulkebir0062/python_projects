import cv2
import numpy as np

video = cv2.VideoCapture('video2.avi')
car_cascade = cv2.CascadeClassifier('haarcascade_car.xml')
backsub = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=300, detectShadows=True)#Arka plan silme işlemi

rois = []  #Seçilen ROI bölgelerini listeleme

while True:
    ret, frames = video.read()
    
    if not ret:
        break

    if frames is None or frames.shape[0] == 0 or frames.shape[1] == 0:
        break

    if len(rois) < 2:  #n ROI seçmek için sınırlama
        #Kullanıcıdan bir alan seçmesini isteyin
        roi_box = cv2.selectROI('Select ROI', frames)
        if roi_box[2] > 0 and roi_box[3] > 0:
            rois.append(roi_box)

    fgmask = backsub.apply(frames)

    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

    for roi_box in rois:
        roi_x, roi_y, roi_width, roi_height = roi_box

        #ROI'yi uygula
        roi = gray[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
        cars = car_cascade.detectMultiScale(roi, 1.1, 4)

        for (x, y, w, h) in cars:
            x += roi_x
            y += roi_y
            plate = frames[y:y+h, x:x+w]
            cv2.rectangle(frames, (x, y), (x+w, y+h), (51, 51, 255), 2)
            cv2.rectangle(frames, (x, y-40), (x+w, y), (51, 51, 255), -2)
            cv2.putText(frames, 'Car', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
            cv2.imshow('car_gray', cv2.resize(plate_gray, (400, 300)))

    lab1 = "Araba Sayisi: " + str(len(rois))
    cv2.putText(frames, lab1, (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (147, 20, 255), 3)
    frames = cv2.resize(frames, (600, 400))
    cv2.imshow('Arac Tespit Sistemi', frames)

    fgmask = cv2.GaussianBlur(fgmask, (5, 5), 0)

    #cv2.imshow('fgmask', fgmask)
    cv2.resizeWindow('Arac Tespit Sistemi', 600, 400)
    
    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
