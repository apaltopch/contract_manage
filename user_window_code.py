from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QHeaderView, QTableWidgetItem, QInputDialog
import MySQLdb as mdb
from user import Ui_UserWindow
import sys

try:
    connect = mdb.connect('127.0.0.1', 'root', 'root', 'contract_management')
    cur = connect.cursor()
except mdb.Error as e:
    QMessageBox.critical(None, 'Ошибка', 'Ошибка подключения к бд!')


class User(QMainWindow):
    def __init__(self, main_window, user_id, username):
        super().__init__()
        self.ui = Ui_UserWindow()
        self.ui.setupUi(self)

        self.main_window = main_window
        self.user_id = user_id
        self.username = username

        self.setup_tables()
        self.load_contracts()
        self.load_tasks()

        self.ui.addContractBtn.clicked.connect(self.add_contract)
        self.ui.addTaskBtn.clicked.connect(self.add_task)
        self.ui.searchInput.textChanged.connect(self.search_archive)

    def setup_tables(self):
        """Настройка таблиц"""
        # Таблица договоров
        self.ui.contractsTable.setColumnCount(6)
        self.ui.contractsTable.setHorizontalHeaderLabels([
            "ID", "Номер", "Тип", "Контрагент", "Статус", "Срок"
        ])
        self.ui.contractsTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Таблица задач
        self.ui.tasksTable.setColumnCount(5)
        self.ui.tasksTable.setHorizontalHeaderLabels([
            "ID", "Договор", "Задача", "Статус", "Срок"
        ])
        self.ui.tasksTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Таблица архива
        self.ui.archiveTable.setColumnCount(5)
        self.ui.archiveTable.setHorizontalHeaderLabels([
            "ID", "Тип", "Название", "Дата", "Статус"
        ])
        self.ui.archiveTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def load_contracts(self):
        """Загрузка договоров пользователя"""
        try:
            cur.execute("""
                SELECT c.id, c.contract_number, ct.name, a.name, c.status, c.end_date
                FROM contracts c
                JOIN contract_types ct ON c.type_id = ct.id
                JOIN agents a ON c.agent_id = a.id
                WHERE c.created_by_id = %s OR c.id IN (
                    SELECT contract_id FROM contract_tasks WHERE assigned_to = %s
                )
                ORDER BY c.end_date
            """, (self.user_id, self.user_id))

            self.ui.contractsTable.setRowCount(0)
            for row, contract in enumerate(cur.fetchall()):
                self.ui.contractsTable.insertRow(row)
                for col, data in enumerate(contract):
                    item = QTableWidgetItem(str(data))
                    self.ui.contractsTable.setItem(row, col, item)

        except mdb.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки договоров: {str(e)}")

    def load_tasks(self):
        """Загрузка задач пользователя"""
        try:
            cur.execute("""
                SELECT t.id, c.contract_number, t.title, t.status, t.deadline
                FROM contract_tasks t
                JOIN contracts c ON t.contract_id = c.id
                WHERE t.assigned_to = %s
                ORDER BY t.deadline
            """, (self.user_id,))

            self.ui.tasksTable.setRowCount(0)
            for row, task in enumerate(cur.fetchall()):
                self.ui.tasksTable.insertRow(row)
                for col, data in enumerate(task):
                    item = QTableWidgetItem(str(data))
                    self.ui.tasksTable.setItem(row, col, item)

        except mdb.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки задач: {str(e)}")

    def search_archive(self):
        """Поиск по архиву"""
        search_text = self.ui.searchInput.text().strip()
        try:
            cur.execute("""
                SELECT id, 'Договор' as type, name, created_at, status
                FROM contracts 
                WHERE created_by_id = %s AND name LIKE %s
                UNION
                SELECT id, 'Задача' as type, title, created_at, status
                FROM contract_tasks
                WHERE assigned_to = %s AND title LIKE %s
                ORDER BY created_at DESC
            """, (self.user_id, f"%{search_text}%", self.user_id, f"%{search_text}%"))

            self.ui.archiveTable.setRowCount(0)
            for row, item in enumerate(cur.fetchall()):
                self.ui.archiveTable.insertRow(row)
                for col, data in enumerate(item):
                    self.ui.archiveTable.setItem(row, col, QTableWidgetItem(str(data)))

        except mdb.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка поиска: {str(e)}")

    def add_contract(self):
        """Добавление нового договора"""
        try:
            # Получаем список контрагентов
            cur.execute("SELECT id, name FROM agents")
            agents = cur.fetchall()

            # Получаем список типов договоров
            cur.execute("SELECT id, name FROM contract_types")
            types = cur.fetchall()

            if not agents or not types:
                QMessageBox.warning(self, "Ошибка", "Нет доступных контрагентов или типов договоров")
                return

            # Диалог ввода данных
            number, ok = QInputDialog.getText(self, "Новый договор", "Введите номер договора:")
            if not ok or not number:
                return

            agent_names = [agent[1] for agent in agents]
            agent_name, ok = QInputDialog.getItem(
                self, "Выбор контрагента", "Контрагент:", agent_names, 0, False)
            if not ok:
                return

            type_names = [type[1] for type in types]
            type_name, ok = QInputDialog.getItem(
                self, "Тип договора", "Тип:", type_names, 0, False)
            if not ok:
                return

            # Сохранение в БД
            agent_id = agents[agent_names.index(agent_name)][0]
            type_id = types[type_names.index(type_name)][0]

            cur.execute("""
                INSERT INTO contracts 
                (contract_number, type_id, agent_id, created_by_id, status)
                VALUES (%s, %s, %s, %s, 'Черновик')
            """, (number, type_id, agent_id, self.user_id))
            connect.commit()

            QMessageBox.information(self, "Успех", "Договор добавлен!")
            self.load_contracts()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка создания договора: {str(e)}")
            connect.rollback()

    def add_task(self):
        """Добавление новой задачи"""
        try:
            # Получаем список договоров пользователя
            cur.execute("""
                SELECT id, contract_number 
                FROM contracts 
                WHERE created_by_id = %s OR id IN (
                    SELECT contract_id FROM contract_tasks WHERE assigned_to = %s
                )
            """, (self.user_id, self.user_id))
            contracts = cur.fetchall()

            if not contracts:
                QMessageBox.warning(self, "Ошибка", "Нет доступных договоров")
                return

            # Диалог ввода данных
            title, ok = QInputDialog.getText(self, "Новая задача", "Описание задачи:")
            if not ok or not title:
                return

            contract_numbers = [contract[1] for contract in contracts]
            contract_num, ok = QInputDialog.getItem(
                self, "Выбор договора", "Договор:", contract_numbers, 0, False)
            if not ok:
                return

            deadline, ok = QInputDialog.getText(
                self, "Срок выполнения", "Введите срок (ГГГГ-ММ-ДД):")
            if not ok or not deadline:
                return

            # Сохранение в БД
            contract_id = contracts[contract_numbers.index(contract_num)][0]

            cur.execute("""
                INSERT INTO contract_tasks 
                (contract_id, title, assigned_to, deadline, status)
                VALUES (%s, %s, %s, %s, 'Новая')
            """, (contract_id, title, self.user_id, deadline))
            connect.commit()

            QMessageBox.information(self, "Успех", "Задача добавлена!")
            self.load_tasks()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка создания задачи: {str(e)}")
            connect.rollback()


















