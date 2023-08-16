import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from ui_muzik import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.baslat.clicked.connect(self.baslat_clicked)
        self.ui.durdur.clicked.connect(self.durdur_clicked)
        self.ui.dosyalar.clicked.connect(self.dosyalar_clicked)

        self.player = QMediaPlayer()
        self.muzik_listesi = {}

    def baslat_clicked(self):
        if self.muzik_listesi:
            secili_muzik = self.ui.muzikListesi.currentItem().text()
            dosya_yolu = self.muzik_listesi.get(secili_muzik)
            if dosya_yolu:
                media = QMediaContent(QUrl.fromLocalFile(dosya_yolu))
                self.player.setMedia(media)
                self.player.play()

    def durdur_clicked(self):
        self.player.stop()

    def dosyalar_clicked(self):
        dosya_diyalogu = QFileDialog()
        dosya_diyalogu.setFileMode(QFileDialog.ExistingFiles)
        dosya_diyalogu.setNameFilter("Müzik Dosyaları (*.mp3 *.wav)")
        if dosya_diyalogu.exec_():
            secilen_dosyalar = dosya_diyalogu.selectedFiles()
            for dosya in secilen_dosyalar:
                dosya_adi = dosya.split("/")[-1]
                self.muzik_listesi[dosya_adi] = dosya
                self.ui.muzikListesi.addItem(dosya_adi)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())