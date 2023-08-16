from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.muzikListesi = QtWidgets.QListWidget(self.centralwidget)
        self.verticalLayout.addWidget(self.muzikListesi)
        self.baslat = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.baslat)
        self.durdur = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.durdur)
        self.dosyalar = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.dosyalar)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Müzik Oynatıcı"))
        self.baslat.setText(_translate("MainWindow", "Başlat"))
        self.durdur.setText(_translate("MainWindow", "Durdur"))
        self.dosyalar.setText(_translate("MainWindow", "Dosyaları Seç"))

