import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
import MySQLdb as mdb
from login import Ui_LoginWindow
from admin_window_code import Admin
from user_window_code import User

try:
    connect = mdb.connect('127.0.0.1', 'root', 'root', 'contract_management')
    cur = connect.cursor()
except mdb.Error as e:
    QMessageBox.critical(None, 'Ошибка', 'Ошибка подключения к бд!')


class Auth(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        self.ui.loginButton.clicked.connect(self.login)

    def login(self):
        try:
            username = self.ui.loginInput.text()
            password = self.ui.passwordInput.text()

            if not all([username, password]):
                QMessageBox.warning(self, 'Внимание', 'Заполните все поля!')
                return

            cur.execute("""select id, username, passw, role from Users 
            where username = %s and passw = %s""", (username, password,))

            user = cur.fetchone()

            if user:
                user_id, username, password, role = user
                QMessageBox.information(self, 'Успех', f'Добро пожаловать в систему {username}')
                role = user[3]

                if role == 'manager':
                    self.open_admin_win()

                elif role == 'user':
                    self.open_user_win(user_id, username)

            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверно введен логин или пароль!')
                return

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка авторизации {e}')
            print(e)

    def open_admin_win(self):
        self.close()
        self.admin_win = Admin(self)
        self.admin_win.show()


    def open_user_win(self, user_id, username):
        self.close()
        self.user_win = User(self, user_id=user_id, username = username)
        self.user_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Auth()
    win.show()
    sys.exit(app.exec())

