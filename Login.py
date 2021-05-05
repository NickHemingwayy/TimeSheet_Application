import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox, QComboBox)
import dataFetch
import TimeSheet
class LoginForm(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Login Form')
		self.resize(500, 120)

		layout = QGridLayout()

		label_name = QLabel('<font size="4"> Username </font>')
		self.lineEdit_username = QLineEdit()
		self.lineEdit_username.setPlaceholderText('Please enter your username')
		layout.addWidget(label_name, 0, 0)
		layout.addWidget(self.lineEdit_username, 0, 1)



		button_login = QPushButton('Login')
		button_login.clicked.connect(self.check_password)
		layout.addWidget(button_login, 2, 0, 1, 2)
		layout.setRowMinimumHeight(2, 75)

		self.setLayout(layout)

	def check_password(self):
		msg = QMessageBox()
		dbuser = dataFetch.validateLogin(self.lineEdit_username.text())
		if self.lineEdit_username.text() == dbuser:
			print("User Found")
			msg.setText('Success')
			msg.exec_()
			loginapp.quit()

		else:
			msg.setText('Incorrect Username')
			msg.exec_()

if __name__ == '__main__':
	loginapp = QApplication(sys.argv)

	login = LoginForm()
	login.show()
	sys.exit(loginapp.exec_())