import os
import shutil
import datetime

klasor_yolu = input("Dosyaların bulunduğu klasörün yolunu girin: ")

video_uzantilari = [".mp4", ".avi", ".mov", ".mkv"]
foto_uzantilari = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

video_klasor = os.path.join(klasor_yolu, "Videolar")
foto_klasor = os.path.join(klasor_yolu, "Fotograflar")
diger_klasor = os.path.join(klasor_yolu, "Diger")

os.makedirs(video_klasor, exist_ok=True)
os.makedirs(foto_klasor, exist_ok=True)
os.makedirs(diger_klasor, exist_ok=True)

def tasima(hedef_klasor, dosya, dosya_yolu):
    hedef = os.path.join(hedef_klasor, dosya)
    if os.path.exists(hedef):
        base, ext = os.path.splitext(dosya)
        sayi = 1
        while os.path.exists(os.path.join(hedef_klasor, f"{base}_{sayi}{ext}")):
            sayi += 1
        hedef = os.path.join(hedef_klasor, f"{base}_{sayi}{ext}")
    shutil.move(dosya_yolu, hedef)

for dosya in os.listdir(klasor_yolu):
    dosya_yolu = os.path.join(klasor_yolu, dosya)

    if os.path.isdir(dosya_yolu):
        continue

    _, uzanti = os.path.splitext(dosya)
    uzanti = uzanti.lower()

    tarih = datetime.datetime.fromtimestamp(os.path.getmtime(dosya_yolu))
    yil_klasor = os.path.join(klasor_yolu, str(tarih.year))
    os.makedirs(yil_klasor, exist_ok=True)

    if uzanti in video_uzantilari:
        hedef_klasor = os.path.join(yil_klasor, "Videolar")
        os.makedirs(hedef_klasor, exist_ok=True)
        tasima(hedef_klasor, dosya, dosya_yolu)
        print(f"{dosya} → {yil_klasor}/Videolar")
    elif uzanti in foto_uzantilari:
        hedef_klasor = os.path.join(yil_klasor, "Fotograflar")
        os.makedirs(hedef_klasor, exist_ok=True)
        tasima(hedef_klasor, dosya, dosya_yolu)
        print(f"{dosya} → {yil_klasor}/Fotograflar")
    else:
        hedef_klasor = os.path.join(yil_klasor, "Diger")
        os.makedirs(hedef_klasor, exist_ok=True)
        tasima(hedef_klasor, dosya, dosya_yolu)
        print(f"{dosya} → {yil_klasor}/Diger")

print("Dosyalar video, fotoğraf ve diğer dosyalar olarak tarihe göre ayrıldı ve isim çakışmaları önlendi!")
