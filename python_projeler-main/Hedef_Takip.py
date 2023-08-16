import cv2

video = cv2.VideoCapture(0)

output_file = "output.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 70.0
frame_size = (640, 480)
video_writer = cv2.VideoWriter(output_file, fourcc, fps, frame_size)

# Hedef takibi için tracker seçimi
tracker = cv2.TrackerKCF_create()

ok, frame = video.read()
bbox = cv2.selectROI("Hedef Takibi", frame,
                     fromCenter=False, showCrosshair=True)

# Hedef takibi başlatma
ok = tracker.init(frame, bbox)

while True:
    ret, frame = video.read()

    if ret:
        # Hedefi takip etme
        ok, bbox = tracker.update(frame)

        if ok:
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        else:
            cv2.putText(frame, "Hedef takibi = olumsuz", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Frame'i videoya yazma
        video_writer.write(frame)

        cv2.imshow("Hedef Takibi", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
video_writer.release()
cv2.destroyAllWindows()
