notlar = []

def not_ekle():
    baslik = input("Not başlığını girin: ")
    icerik = input("Not içeriğini girin: ")
    notlar.append({"başlık": baslik, "içerik": icerik})
    print("Not eklendi!")

def notlari_goruntule():
    if not notlar:
        print("Henüz not bulunmamaktadır.")
    else:
        for index, not_bilgisi in enumerate(notlar):
            print(f"{index + 1}. Not")
            print(f"Başlık: {not_bilgisi['başlık']}")
            print(f"İçerik: {not_bilgisi['içerik']}")
            print("-" * 20)

def not_sil():
    notlari_goruntule()
    if not notlar:
        return

    secim = int(input("Silmek istediğiniz notun numarasını girin (0 çıkış için): "))
    if secim == 0:
        return
    elif 1 <= secim <= len(notlar):
        silinecek_not = notlar.pop(secim - 1)
        print(f"{silinecek_not['başlık']} başlıklı not silindi.")
    else:
        print("Geçersiz seçim!")

def notlari_kaydet():
    with open("notlar.txt", "w") as dosya:
        for not_bilgisi in notlar:
            dosya.write(f"{not_bilgisi['başlık']}|{not_bilgisi['içerik']}\n")
    print("Notlar dosyaya kaydedildi.")

def notlari_yukle():
    try:
        with open("notlar.txt", "r") as dosya:
            for satir in dosya:
                baslik, icerik = satir.strip().split("|")
                notlar.append({"başlık": baslik, "içerik": icerik})
        print("Notlar dosyadan yüklendi.")
    except FileNotFoundError:
        print("Kayıtlı not dosyası bulunamadı.")

def ana_menu_goster():
    print("Not Defteri Uygulaması")
    print("-" * 20)
    print("1. Not Ekle")
    print("2. Notları Görüntüle")
    print("3. Not Sil")
    print("4. Notları Kaydet")
    print("0. Çıkış")
    print("-" * 20)

def main():
    notlari_yukle()

    while True:
        ana_menu_goster()
        secim = input("Seçiminizi yapın: ")

        if secim == "1":
            not_ekle()
        elif secim == "2":
            notlari_goruntule()
        elif secim == "3":
            not_sil()
        elif secim == "4":
            notlari_kaydet()
        elif secim == "0":
            print("Not defteri uygulamasından çıkılıyor...")
            break
        else:
            print("Geçersiz seçim! Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
