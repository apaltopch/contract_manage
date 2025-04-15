# Form implementation generated from reading ui file 'admin_window.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AdminWindow(object):
    def setupUi(self, AdminWindow):
        AdminWindow.setObjectName("AdminWindow")
        AdminWindow.resize(680, 415)
        self.centralwidget = QtWidgets.QWidget(parent=AdminWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        # Вкладка пользователей
        self.userTab = QtWidgets.QWidget()
        self.userTab.setObjectName("userTab")
        self.userLayout = QtWidgets.QVBoxLayout(self.userTab)
        self.userLayout.setObjectName("userLayout")
        self.usersTable = QtWidgets.QTableWidget(parent=self.userTab)
        self.usersTable.setObjectName("usersTable")
        self.usersTable.setColumnCount(0)
        self.usersTable.setRowCount(0)
        self.userLayout.addWidget(self.usersTable)
        self.addUserBtn = QtWidgets.QPushButton(parent=self.userTab)
        self.addUserBtn.setObjectName("addUserBtn")
        self.userLayout.addWidget(self.addUserBtn)
        self.exit_btn = QtWidgets.QPushButton(parent=self.userTab)
        self.exit_btn.setStyleSheet("background-color: rgb(223, 0, 0);")
        self.exit_btn.setObjectName("exit_btn")
        self.userLayout.addWidget(self.exit_btn)
        self.tabWidget.addTab(self.userTab, "")

        # Вкладка прав доступа (с добавленной кнопкой сохранения)
        self.accessTab = QtWidgets.QWidget()
        self.accessTab.setObjectName("accessTab")
        self.accessLayout = QtWidgets.QVBoxLayout(self.accessTab)
        self.accessLayout.setObjectName("accessLayout")
        self.accessTable = QtWidgets.QTableWidget(parent=self.accessTab)
        self.accessTable.setObjectName("accessTable")
        self.accessTable.setColumnCount(0)
        self.accessTable.setRowCount(0)
        self.accessLayout.addWidget(self.accessTable)

        # Добавленная кнопка "Сохранить изменения"
        self.saveAccessBtn = QtWidgets.QPushButton(parent=self.accessTab)
        self.saveAccessBtn.setObjectName("saveAccessBtn")
        self.saveAccessBtn.setStyleSheet("background-color: rgb(0, 170, 0);")
        self.accessLayout.addWidget(self.saveAccessBtn)

        self.tabWidget.addTab(self.accessTab, "")

        # Вкладка отчетов
        self.reportTab = QtWidgets.QWidget()
        self.reportTab.setObjectName("reportTab")
        self.reportLayout = QtWidgets.QVBoxLayout(self.reportTab)
        self.reportLayout.setObjectName("reportLayout")
        self.reportTable = QtWidgets.QTableWidget(parent=self.reportTab)
        self.reportTable.setObjectName("reportTable")
        self.reportTable.setColumnCount(0)
        self.reportTable.setRowCount(0)
        self.reportLayout.addWidget(self.reportTable)
        self.tabWidget.addTab(self.reportTab, "")

        self.verticalLayout.addWidget(self.tabWidget)
        AdminWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AdminWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AdminWindow)

    def retranslateUi(self, AdminWindow):
        _translate = QtCore.QCoreApplication.translate
        AdminWindow.setWindowTitle(_translate("AdminWindow", "Панель администратора"))
        self.addUserBtn.setText(_translate("AdminWindow", "Добавить пользователя"))
        self.exit_btn.setText(_translate("AdminWindow", "Выйти"))
        self.saveAccessBtn.setText(_translate("AdminWindow", "Сохранить изменения"))  # Текст для новой кнопки
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.userTab), _translate("AdminWindow", "Пользователи"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.accessTab), _translate("AdminWindow", "Права доступа"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.reportTab), _translate("AdminWindow", "Отчёты"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AdminWindow = QtWidgets.QMainWindow()
    ui = Ui_AdminWindow()
    ui.setupUi(AdminWindow)
    AdminWindow.show()
    sys.exit(app.exec())
