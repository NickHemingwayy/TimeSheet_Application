import sys
import dataFetch
from PyQt5.Qt import *


'''To be constructed in TimeSheet.py'''


class AdminForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add User')
        self.setFixedSize(800, 400)
        self.layout = QGridLayout()

        self.label_fName = QLabel('Employee First Name')
        self.label_lName = QLabel('Employee Last Name')
        self.layout.addWidget(self.label_fName, 0, 0)
        self.layout.addWidget(self.label_lName, 1, 0)

        self.lineEdit_fName = QLineEdit()
        self.lineEdit_lName = QLineEdit()
        self.layout.addWidget(self.lineEdit_fName, 0, 1)
        self.layout.addWidget(self.lineEdit_lName, 1, 1)

        self.custUsername = QCheckBox('Custom username')
        self.layout.addWidget(self.custUsername, 2, 0)
        self.custUserHint = QLabel('* Otherwise username will be set to first letter of first name followed by last name')
        self.layout.addWidget(self.custUserHint, 2, 1)
        self.custUserEdit = QLineEdit()
        self.layout.addWidget(self.custUserEdit, 2, 1)

        self.label_Dep = QLabel('Department')
        # Only one ComboBox is shown at the start
        self.comboDep1 = QComboBox()
        self.comboDep1.setMaximumWidth(200)
        self.comboDep2 = QComboBox()
        self.comboDep2.setMaximumWidth(200)
        self.comboDep3 = QComboBox()
        self.comboDep3.setMaximumWidth(200)
        self.comboDep4 = QComboBox()
        self.comboDep4.setMaximumWidth(200)
        self.comboDep5 = QComboBox()
        self.comboDep5.setMaximumWidth(200)

        self.layout.addWidget(self.label_Dep, 3, 0)
        self.layout.addWidget(self.comboDep1, 3, 1)

        self.addDep = QPushButton('Add Department')
        self.addDep.setStyleSheet("background-color: orange;")
        self.layout.addWidget(self.addDep, 8, 1, Qt.AlignLeft)
        self.addDep.setMaximumWidth(150)

        self.isAdmin = QCheckBox('is Admin')
        self.layout.addWidget(self.isAdmin, 9, 1)

        # Adds department ID's to combobox
        depLst = dataFetch.getDep()
        self.comboDep1.addItem('')
        for i in depLst:
            self.comboDep1.addItem(i)

        self.submit = QPushButton('Submit Form')
        self.submit.setStyleSheet("background-color: purple; color: white;")  # part of dark colour palette
        self.submit.setMaximumWidth(500)
        self.layout.addWidget(self.submit, 10, 1)
        self.setLayout(self.layout)

        # Connects event listeners to their corresponding functions
        self.custUsername.clicked.connect(self.customUser)
        self.submit.clicked.connect(self.getVals)
        self.addDep.clicked.connect(self.addDepart)
        self.comboDep1.currentTextChanged.connect(self.addDepart)
        self.setStyleSheet("QLabel {font: 10pt Arial}")
        self.customUser()
        self.layout.setContentsMargins(50, 10, 50, 10)
        self.msg = QMessageBox()

    # Called when user checks the 'Custom username' checkbox
    def customUser(self):
        if self.custUsername.isChecked():
            self.custUserEdit.show()  # Reveals another lineEdit where a custom username can be entered
        else:
            self.custUserEdit.hide()

    # Gets values from form and checks if a similar user is already in DB - Finally the values are pushed to the DB
    def getVals(self):
        self.msg = QMessageBox()
        retLst = []
        fName = self.lineEdit_fName.text().strip().lower()
        lName = self.lineEdit_lName.text().strip().lower()
        if self.custUsername.isChecked():  # Sets username to the text in custom username field if box is checked
            username = self.custUserEdit.text().lower()
        else:  # Otherwise set username to first letter of firstname followed by lastname
            username = fName[0].lower() + lName.lower()
        if self.lineEdit_fName.text() != '' and self.lineEdit_lName.text() != '' and self.comboDep1.currentText() != '' and username != '':
            deps = [self.comboDep1.currentText(), self.comboDep2.currentText(), self.comboDep3.currentText(), self.comboDep4.currentText(), self.comboDep5.currentText()]
            while '' in deps: deps.remove('')  # removes all empty department combo values
            if self.isAdmin.isChecked():
                admState = 'Yes'
            else:
                admState = 'No'
            for i in range(0, len(deps)):  # .title() is used to capitalize first letters of first and last names
                retLst.append([fName.title() + ' ' + lName.title(), username, deps[i], admState])
            ret = QMessageBox.question(self, '', 'Are you sure you wan to submit?', QMessageBox.Yes | QMessageBox.No)
            if ret == QMessageBox.No:
                pass
            elif ret == QMessageBox.Yes:
                userExists = dataFetch.checkUser(username)  # Checks if username exists in DB
                print(userExists)
                if userExists > 0:  # If there are any current users with that username in DB
                    overite = QMessageBox.question(self, '', 'Oops! There is already a user with the username: '+
                                                   username +'. Do you wish to overight?', QMessageBox.Yes | QMessageBox.No)
                    if overite == QMessageBox.Yes:
                        dataFetch.removeUser(username)  # removes user from DB
                        dataFetch.addUser(retLst)  # Adds user with the given credentials
                        self.msg.setText('User ' + username + ' has been overwritten')
                        self.msg.exec_()
                        self.close()
                    else:
                        pass
                else:
                    dataFetch.addUser(retLst)  # Adds user with the given credentials
                    self.msg.setText('User ' + username + ' has been added to database')
                    self.msg.exec_()
                    print(retLst)
                    self.close()
        else:
            self.msg.setText('Please Verify Fields')
            self.msg.exec_()

    global count
    count = 0

    # Adds up to 5 extra department fields based on number of times button is clicked
    def addDepart(self):
        global count
        count += 1
        if count == 1:
            self.layout.addWidget(self.comboDep2, 4, 1)
            depLst = dataFetch.getDep()
            self.comboDep2.addItem("")
            for i in depLst:
                self.comboDep2.addItem(i)
            self.comboDep2.currentTextChanged.connect(self.addDepart)
        elif count == 2:
            self.layout.addWidget(self.comboDep3, 5, 1)
            depLst = dataFetch.getDep()
            self.comboDep3.addItem("")
            for i in depLst:
                self.comboDep3.addItem(i)
            self.comboDep3.currentTextChanged.connect(self.addDepart)
        elif count == 3:
            self.layout.addWidget(self.comboDep4, 6, 1)
            depLst = dataFetch.getDep()
            self.comboDep4.addItem("")
            for i in depLst:
                self.comboDep4.addItem(i)
            self.comboDep4.currentTextChanged.connect(self.addDepart)
        elif count == 4:
            self.addDep.hide() # Hide add Department button once maximum department combobox's have been added
            self.layout.addWidget(self.comboDep5, 7, 1)
            depLst = dataFetch.getDep()
            self.comboDep5.addItem("")
            for i in depLst:
                self.comboDep5.addItem(i)
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    adm = AdminForm()
    adm.show()
    sys.exit(app.exec_())
