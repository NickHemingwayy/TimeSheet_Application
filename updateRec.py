import sys
import dataFetch
from PyQt5.Qt import *
from datetime import *


'''To be constructed in TimeSheet.py'''
class AdminForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Record')
        self.resize(800, 400)
        self.layout = QGridLayout()

        self.title = QLabel('Fill in parameters to find record')
        self.layout.addWidget(self.title,0,0)

        self.empUsername = QLineEdit()
        self.layout.addWidget(self.empUsername,1,0)
        self.empUsername.setPlaceholderText("Employee First and Last name")
        self.empUsername.setMinimumWidth(400)

        self.startDateLabel = QLabel('Start Date:')
        self.layout.addWidget(self.startDateLabel,1,1)

        self.startDate = QDateEdit(self, calendarPopup=True)
        self.startDate.setDateTime(QDateTime.currentDateTime().toPyDateTime() - timedelta(days=14))
        self.layout.addWidget(self.startDate, 1, 2)

        self.endDateLabel = QLabel('End Date:')
        self.layout.addWidget(self.endDateLabel, 1, 3)

        self.endDate = QDateEdit(self, calendarPopup=True)
        self.endDate.setDateTime(QDateTime.currentDateTime())
        self.layout.addWidget(self.endDate, 1, 4)

        self.search = QPushButton('Search')
        self.layout.addWidget(self.search, 1, 5)
        self.search.setStyleSheet("background-color: orange; color: black;")

        self.recordList = QListWidget()
        self.recordList.addItem(' ')
        self.layout.addWidget(self.recordList, 2, 0, 15, 1)  # Fourth and Fifth parameters for # of row/column span
        self.recordList.setMinimumWidth(400)
        self.recordList.setMinimumHeight(100)

        self.depLabel = QLabel('Department')
        self.layout.addWidget(self.depLabel, 2, 1, 1, 5)

        self.entLabel = QLabel('Legal Entity')
        self.layout.addWidget(self.entLabel, 4, 1, 1, 5)

        self.taskLabel = QLabel('Task')
        self.layout.addWidget(self.taskLabel, 6, 1, 1, 5)

        self.custLabel = QLabel('Customer')
        self.layout.addWidget(self.custLabel, 8, 1, 1, 5)

        self.hoursLabel = QLabel('Hours')
        self.layout.addWidget(self.hoursLabel, 10, 1, 1, 5)

        self.dateLabel = QLabel('Date')
        self.layout.addWidget(self.dateLabel, 12, 1, 1, 5)

        self.empLabel = QLabel('Employee')
        self.layout.addWidget(self.empLabel, 14, 1, 1, 5)

        self.combo1 = QComboBox()
        self.combo2 = QComboBox()
        self.combo3 = QComboBox()
        self.combo4 = QComboBox()

        self.layout.addWidget(self.combo1, 3, 1, 1, 5)
        self.layout.addWidget(self.combo2, 5, 1, 1, 5)
        self.layout.addWidget(self.combo3, 7, 1, 1, 5)
        self.layout.addWidget(self.combo4, 9, 1, 1, 5)

        self.combo1.setMinimumWidth(200)
        self.combo2.setMinimumWidth(200)
        self.combo3.setMinimumWidth(200)
        self.combo4.setMinimumWidth(200)

        self.combo1.setEditable(True)
        self.combo2.setEditable(True)
        self.combo3.setEditable(True)
        self.combo4.setEditable(True)

        self.newHours = QLineEdit()
        self.layout.addWidget(self.newHours, 11, 1, 1, 5)

        self.newDate = QDateEdit(self, calendarPopup=True)
        self.layout.addWidget(self.newDate, 13, 1, 1, 5)

        self.newUser = QLineEdit()
        self.layout.addWidget(self.newUser, 15, 1, 1, 5)

        self.edit = QPushButton('Update')
        self.layout.addWidget(self.edit, 16, 1, 1, 3)
        self.edit.setStyleSheet("background-color: purple; color: white;")

        self.delete = QPushButton('Delete Record')
        self.delete.setStyleSheet('background-color: rgb(255,0,0)')
        self.layout.addWidget(self.delete, 16, 4, 1, 2)


        # Record Updating fields are hidden until user selects and entry to avoid unwanted data-entry
        self.depLabel.hide()
        self.entLabel.hide()
        self.taskLabel.hide()

        self.dateLabel.hide()
        self.hoursLabel.hide()
        self.empLabel.hide()
        self.custLabel.hide()
        self.combo1.hide()
        self.combo2.hide()
        self.combo3.hide()
        self.combo4.hide()
        self.newHours.hide()
        self.newDate.hide()
        self.newUser.hide()
        self.edit.hide()
        self.delete.hide()
        self.recordList.hide()

        self.search.clicked.connect(self.fetchRecs)
        self.edit.clicked.connect(self.updateRec)
        self.delete.clicked.connect(self.deleteRec)

        self.combo1.currentTextChanged.connect(self.on_combobox1_change)
        self.combo2.currentTextChanged.connect(self.on_combobox2_change)
        self.combo3.currentTextChanged.connect(self.on_combobox3_change)

        self.setLayout(self.layout)

        self.setStyleSheet("QLabel {font: 10pt Arial}")
        self.layout.setContentsMargins(50, 50, 50, 50)

    def deleteRec(self):
        oldRec = self.recordList.currentItem().text().replace('[', '').replace(']', '').replace('\'', '').split(', ')
        oldRec.append(self.empUsername.text())
        ret = QMessageBox.question(self, '', 'Are you sure you wan to delete?', QMessageBox.Yes | QMessageBox.No)
        msg = QMessageBox()
        if ret == QMessageBox.No:
            pass
        elif ret == QMessageBox.Yes:
            dataFetch.deleteRecord(oldRec)
            msg.setText('Database Updated')
            msg.exec_()

    def on_combobox1_change(self):
        combo1_2Val = dataFetch.combo1_2Vals(self.combo1.currentText())
        self.combo2.clear()
        for i in combo1_2Val:
            self.combo2.addItem(str(i))

    # Refreshes Task combobox each time value is changed
    def on_combobox2_change(self):
        combo1_3Val = dataFetch.combo1_3Vals(self.combo2.currentText(),self.combo1.currentText())
        self.combo3.clear()
        for i in combo1_3Val:
            self.combo3.addItem(str(i))

    def on_combobox3_change(self):
        combo1_4Val = dataFetch.combo1_4Vals(self.combo3.currentText(), self.combo2.currentText(), self.combo1.currentText())
        AllItems = [self.combo4.itemText(i) for i in range(self.combo4.count())]
        for i in combo1_4Val:
            if i not in AllItems:
                self.combo4.addItem(str(i))

    '''Updates records in DB based on which record was selected by the user'''
    def updateRec(self):
        oldRec = self.recordList.currentItem().text().replace('[','').replace(']','').replace('\'','').split(', ')
        oldRec.append(self.empUsername.text())
        print('old Record')
        print(oldRec)
        odf = datetime.strptime(self.newDate.text(),'%m/%d/%Y')
        ndf = odf.strftime('%Y-%m-%d')
        # The new record to be pushed to the db
        newRec = [self.combo1.currentText(), self.combo2.currentText(), self.combo3.currentText(), self.combo4.currentText(), self.newHours.text(), ndf, self.newUser.text().lower()]
        print('new Record')
        print(newRec)
        ret = QMessageBox.question(self, '', 'Are you sure you wan to submit?', QMessageBox.Yes | QMessageBox.No)
        msg = QMessageBox()
        if ret == QMessageBox.No:
            pass
        elif ret == QMessageBox.Yes:
            # Validates that all of the of the update fields are not empty before submitting to DB
            if self.combo1.currentText() == '' or self.combo2.currentText() == '' or self.combo3.currentText() == '' or self.newHours.text() == '' or self.newDate.text() == '' or self.newUser.text() == '':
                msg.setText('Please Verify Fields')
                msg.exec_()
            else:
                dataFetch.updateRecords(oldRec, newRec)
                msg.setText('Database Updated')
                msg.exec_()
                self.close()

    def item_click(self, item):

        # Un-hides the record updating fields when user selects record to be updated
        self.depLabel.show()
        self.entLabel.show()
        self.taskLabel.show()
        self.custLabel.show()
        self.dateLabel.show()
        self.hoursLabel.show()
        self.empLabel.show()
        self.combo1.show()
        self.combo2.show()
        self.combo3.show()
        self.combo4.show()
        self.newHours.show()
        self.newDate.show()
        self.newUser.show()
        self.edit.show()
        self.delete.show()

        strpItem = item.text().split(', ')

        self.combo1.clear()
        self.combo2.clear()
        self.combo3.clear()
        self.combo4.clear()
        self.combo1.addItem(strpItem[0])

        combo1_1Val = dataFetch.updateRecCombo1(self.empUsername.text())
        for i in combo1_1Val:
            self.combo1.addItem(i)
        self.combo2.addItem(strpItem[1])
        self.combo3.addItem(strpItem[2])
        self.combo4.addItem(strpItem[3])
        self.combo2.setCurrentText(strpItem[1])
        self.combo3.setCurrentText(strpItem[2])
        self.combo4.setCurrentText(strpItem[3])

        self.newHours.setText(str(strpItem[4]))
        self.newDate.setDate(QDate.fromString(strpItem[5], 'yyyy-MM-dd'))  # Changes date to correct format for DB
        self.newUser.setText(self.empUsername.text())

    '''Fetches all matching records based on the given parameters by the user'''
    def fetchRecs(self):
        self.recordList.clear()
        self.recordList.show()
        getStartDate = self.startDate.date().toPyDate()
        getEndDate = self.endDate.date().toPyDate()
        print(getStartDate)
        print(getEndDate)
        print(self.empUsername.text())
        global entries
        entries = dataFetch.getPrevEntries(str(getStartDate), str(getEndDate), self.empUsername.text())
        for i in entries:
            ls = list(i)
            ls[5] = str(ls[5])
            self.recordList.addItem(str(ls).replace('[', '').replace(']', '').replace('\'', '').replace('\\r',''))
            self.recordList.itemClicked.connect(self.item_click)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    adm = AdminForm()
    adm.show()
    sys.exit(app.exec_())
