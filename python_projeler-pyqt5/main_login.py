#Gerekli kütüphaneleri içe aktar
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QLabel, QVBoxLayout, QDialog, QPushButton, QLineEdit
from PyQt5.QtCore import QTimer, QTime
import hashlib
import subprocess
from ui_login import Ui_Form

#Şifremi Unuttum (ForgotPasswordDialog) diyaloğu oluştur
class ForgotPasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Şifremi Unuttum")
        layout = QVBoxLayout(self)

        self.security_label = QLabel("Güvenlik Kimliği:")
        self.security_line_edit = QLineEdit()

        self.label = QLabel("Yeni parolanızı girin:")
        self.line_edit = QLineEdit()

        self.submit_button = QPushButton("Gönder")
        self.submit_button.clicked.connect(self.submit_password)

        layout.addWidget(self.security_label)
        layout.addWidget(self.security_line_edit)
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.submit_button)

    def submit_password(self):
        security_id = self.security_line_edit.text()
        new_password = self.line_edit.text()

        if security_id != "1633": 
            QMessageBox.warning(self, "Hata", "Geçersiz güvenlik kimliği!")
            return

        with open("password.txt", "w") as file:
            file.write(new_password)

        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        login_form.password = new_password
        QMessageBox.information(self, "Şifre Sıfırlama", "Yeni parola başarıyla ayarlandı!")
        self.close()


#Kayıt Ol (RegisterDialog) diyaloğu oluştur
class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kayıt Ol")
        layout = QVBoxLayout(self)

        self.username_label = QLabel("Kullanıcı Adı:")
        self.username_line_edit = QLineEdit()

        self.password_label = QLabel("Parola:")
        self.password_line_edit = QLineEdit()
        self.password_line_edit.setEchoMode(QLineEdit.Password)

        self.confirm_password_label = QLabel("Parolayı Onayla:")
        self.confirm_password_line_edit = QLineEdit()
        self.confirm_password_line_edit.setEchoMode(QLineEdit.Password)

        self.submit_button = QPushButton("Kaydol")
        self.submit_button.clicked.connect(self.register)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_line_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_line_edit)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_line_edit)
        layout.addWidget(self.submit_button)

    def register(self):
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()
        confirm_password = self.confirm_password_line_edit.text()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Hata", "Parolalar uyuşmuyor!")
            return

        with open("users.txt", "a") as file:
            file.write(f"{username}:{password}\n")

        QMessageBox.information(self, "Kayıt Başarılı", "Kayıt başarıyla oluşturuldu!")
        self.close()


#Giriş Formu (LoginForm) oluştur
class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_2.clicked.connect(self.show_forgot_password_dialog)
        self.ui.pushButton_3.clicked.connect(self.show_register_dialog)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.load_users()
    #Saat işlemleri
    def update_time(self):
        current_time = QTime.currentTime()
        time_text = current_time.toString("HH:mm:ss")
        self.ui.label_4.setText(time_text)

    def load_users(self):
        self.users = {}
        try:
           with open("users.txt", "r") as file:
              for line in file:
                username, password = line.strip().split(":")
                self.users[username] = password
        except FileNotFoundError:
          self.users = {}

    def login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        if username in self.users and self.users[username] == password:
             QMessageBox.information(self, "Giriş Başarılı", "Giriş başarıyla gerçekleştirildi!")
             subprocess.Popen(["python", "main2.py"])
        else:
           QMessageBox.warning(self, "Giriş Başarısız", "Kullanıcı adı veya parola hatalı!")

    def show_forgot_password_dialog(self):
        dialog = ForgotPasswordDialog()
        dialog.exec_()

    def show_register_dialog(self):
        dialog = RegisterDialog()
        dialog.exec_()

#Ana uygulamayı çalıştır
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()
    sys.exit(app.exec_())
