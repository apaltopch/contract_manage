import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QHeaderView, QTableWidgetItem, QDialog, QLineEdit, \
    QComboBox, QTableWidget
import MySQLdb as mdb
from admin_window import Ui_AdminWindow
from add_user import Ui_Form

try:
    connect = mdb.connect('127.0.0.1', 'root', 'root', 'contract_management')
    cur = connect.cursor()
except mdb.Error as e:
    QMessageBox.critical(None, 'Ошибка', 'Ошибка подключения к бд!')


class AddUser(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.main_window = main_window

        self.ui.add_btn.clicked.connect(self.add_user)
        self.ui.user_rb.setChecked(True)
        self.ui.passw_lineEdit.setEchoMode(QLineEdit.EchoMode.Password)

    def add_user(self):
        username = self.ui.login_lineEdit.text()
        password = self.ui.passw_lineEdit.text()
        fullname = self.ui.fio_lineEdit.text()
        email = self.ui.email_lineEdit.text()

        # Определение роли
        if self.ui.manager_rb.isChecked():
            role = "manager"
        else:
            role = "user"

        if not all([username, password, fullname, email]):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            cur.execute(
                """insert into Users (username, passw, full_name, email, role) VALUES (%s, %s, %s, %s, %s)""",
                (username, password, fullname, email, role,)
            )
            connect.commit()

            QMessageBox.information(self, "Успех", "Пользователь успешно добавлен!")
            self.main_window.load_users()
            self.accept()

        except mdb.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении пользователя: {e}")


class Admin(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_AdminWindow()
        self.ui.setupUi(self)
        self.main_window = main_window

        self.setup_tables()

        self.load_users()
        self.load_access_data()
        self.load_reports()

        self.ui.addUserBtn.clicked.connect(self.show_add_user)
        self.ui.exit_btn.clicked.connect(self.back)

        self.ui.accessTable.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.ui.saveAccessBtn.clicked.connect(self.save_all_access_changes)
        self._changes_made = False
        self.ui.accessTable.cellChanged.connect(self.on_cell_changed)

    def setup_tables(self):
        '''настройка заголовков таблиц'''
        # Таблица пользователей
        self.ui.usersTable.setColumnCount(5)
        self.ui.usersTable.setHorizontalHeaderLabels(["ID", "Логин", "ФИО", "Email", "Роль"])
        self.ui.usersTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Таблица прав доступа
        self.ui.accessTable.setColumnCount(5)
        self.ui.accessTable.setHorizontalHeaderLabels(["Пользователь", "Тип договора", "Доступ"])
        self.ui.accessTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Таблица отчетов
        self.ui.reportTable.setColumnCount(4)
        self.ui.reportTable.setHorizontalHeaderLabels(["Пользователь", "Действие", "Дата", "Объект"])
        self.ui.reportTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def load_users(self):
        '''загружаем пользователей'''
        try:
            cur.execute("SELECT id, username, full_name, email, role FROM Users")
            users = cur.fetchall()

            self.ui.usersTable.setRowCount(len(users))
            for row, user in enumerate(users):
                for col, data in enumerate(user):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.ui.usersTable.setItem(row, col, item)
        except mdb.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки пользователей: {e}")

    def load_access_data(self):
        self._changes_made = True  # Блокируем сохранение во время загрузки
        """загрузка данных о правах доступа"""
        try:
            cur.execute("""
                            SELECT 
                                u.id as user_id,
                                ct.id as type_id,
                                u.username,
                                ct.name as contract_type,
                                CASE 
                                    WHEN EXISTS (
                                        SELECT 1 FROM user_access 
                                        WHERE user_id = u.id AND contract_type_id = ct.id
                                    ) THEN 'Полный доступ'
                                    ELSE 'Ограниченный'
                                END as access_level
                            FROM Users u
                            CROSS JOIN contract_types ct
                            ORDER BY u.username, ct.name
                        """)

            self.ui.accessTable.setRowCount(0)
            for row, (user_id, type_id, username, contract_type, access) in enumerate(cur.fetchall()):
                self.ui.accessTable.insertRow(row)

                # Добавляем элементы в таблицу
                item_user = QTableWidgetItem(username)
                item_user.setData(Qt.ItemDataRole.UserRole, (user_id, type_id))
                self.ui.accessTable.setItem(row, 0, item_user)

                self.ui.accessTable.setItem(row, 1, QTableWidgetItem(contract_type))

                combo = QComboBox()
                combo.addItems(["Ограниченный", "Полный доступ"])
                combo.setCurrentText(access)
                self.ui.accessTable.setCellWidget(row, 2, combo)

        finally:
            self._changes_made = False

    def on_cell_changed(self, row, column):
        if column == 2 and not self._changes_made:
            self.save_single_access(row)

    def save_single_access(self, row):
        try:
            user_item = self.ui.accessTable.item(row, 0)
            user_id, type_id = user_item.data(Qt.ItemDataRole.UserRole)
            combo = self.ui.accessTable.cellWidget(row, 2)
            has_access = 1 if combo.currentText() == "Полный доступ" else 0

            cur.execute("""
                INSERT INTO user_access (user_id, contract_type_id, has_access)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE has_access = VALUES(has_access)
            """, (user_id, type_id, has_access))
            connect.commit()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения: {str(e)}")
            connect.rollback()

    def save_all_access_changes(self):
        try:
            for row in range(self.ui.accessTable.rowCount()):
                self.save_single_access(row)
            QMessageBox.information(self, "Успех", "Все изменения сохранены!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения: {str(e)}")

    def load_reports(self):
        """загрузка отчетов о действиях пользователей"""
        try:
            # собираем информацию о действиях пользователей из разных таблиц
            cur.execute("""
                select u.username, 'Создал договор' as action, c.created_at, c.contract_number
                from contracts c
                join Users u ON c.created_by_id = u.id
                union all
                select u.username, 'Выполнил задачу' as action, t.created_at, t.title
                from contract_tasks t
                join Users u ON t.assigned_to = u.id
                where t.status = 'Завершена'
                order by 3 desc
                limit 50
            """)
            reports = cur.fetchall()

            self.ui.reportTable.setRowCount(len(reports))
            for row, report in enumerate(reports):
                for col, data in enumerate(report):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.ui.reportTable.setItem(row, col, item)
        except mdb.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки отчетов: {e}")

    def show_add_user(self):
        try:
            self.add_user = AddUser(self)
            self.add_user.show()
        except Exception as e:
            QMessageBox.critical(self, 'ошибка', f'ошибка открытия окна {e}')
            print(e)

    def back(self):
        self.close()
        self.main_window.show()



