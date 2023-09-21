import cv2
from pyzbar.pyzbar import decode
import numpy as np

cap = cv2.VideoCapture()

while True:
    ret, frame = cap.read()

    barcodes = decode(frame)

    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        #Tanınan barkod veya QR kod bilgisini ekrana yazdırır
        print(f'Tür: {barcode_type}, Veri: {barcode_data}')

        # Görüntü üzerinde kodları işaretle
        points = np.array(barcode.polygon, dtype=np.int32)
        if len(points) >= 4:
            cv2.polylines(frame, [points], isClosed=True, color=(0, 255, 0), thickness=2)

    cv2.imshow('Barkod ve QR Kod Tanıma', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
