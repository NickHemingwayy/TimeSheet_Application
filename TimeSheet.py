import sys
from datetime import *
from functools import partial
import dataFetch
import calculate
import isAdmin
from PyQt5.Qt import *
import prevEntries
import updateRec

'''Whats up other programmer. Welcome to my super sweet app'''

'''Blue Print for login Class form'''


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login Form')
        self.setFixedSize(500, 200)

        self.layout = QGridLayout()

        self.label_name = QLabel('Username')
        self.label_name.setFont(QFont('Helvetica', 12))
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        self.layout.addWidget(self.label_name, 0, 0)
        self.layout.addWidget(self.lineEdit_username, 0, 1)

        self.button_login = QPushButton('Login')
        self.button_login.setStyleSheet("background-color: purple; color: white;")
        self.layout.addWidget(self.button_login, 2, 0, 1, 2)
        self.button_login.setMaximumHeight(30)
        self.layout.setRowMinimumHeight(2, 75)

        self.setLayout(self.layout)
        self.layout.setContentsMargins(50, 30, 50, 10)


'''BluePrint for Time Sheet form.
        ___ !IMPORTANT Not every widget is initialized here, Some are initialized within the Main() method!___'''


class TimeSheet(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TimeSheet')
        self.resize(1500, 750)

        self.username = QLabel(self)
        self.username.setFont(QFont('Helvetica', 15))

        # Day Labels
        self.sun = QLabel(self)
        self.sun.setFont(QFont('Helvetica', 10))
        self.mon = QLabel(self)
        self.mon.setFont(QFont('Helvetica', 10))
        self.tues = QLabel(self)
        self.tues.setFont(QFont('Helvetica', 10))
        self.wed = QLabel(self)
        self.wed.setFont(QFont('Helvetica', 10))
        self.thur = QLabel(self)
        self.thur.setFont(QFont('Helvetica', 10))
        self.fri = QLabel(self)
        self.fri.setFont(QFont('Helvetica', 10))
        self.sat = QLabel(self)
        self.sat.setFont(QFont('Helvetica', 10))

        self.timeoff = QLabel(self)
        self.timeoff.setFont(QFont('Helvetica', 13))

        self.bottomcalc1 = QLabel('0.00')
        self.bottomcalc1.setFont(QFont('Helvetica', 13))
        self.bottomcalc2 = QLabel('0.00')
        self.bottomcalc2.setFont(QFont('Helvetica', 13))
        self.bottomcalc3 = QLabel('0.00')
        self.bottomcalc3.setFont(QFont('Helvetica', 13))
        self.bottomcalc4 = QLabel('0.00')
        self.bottomcalc4.setFont(QFont('Helvetica', 13))
        self.bottomcalc5 = QLabel('0.00')
        self.bottomcalc5.setFont(QFont('Helvetica', 13))
        self.bottomcalc6 = QLabel('0.00')
        self.bottomcalc6.setFont(QFont('Helvetica', 13))
        self.bottomcalc7 = QLabel('0.00')
        self.bottomcalc7.setFont(QFont('Helvetica', 13))

        self.dateedit = QDateEdit(self, calendarPopup=True)
        self.dateedit.setMinimumHeight(30)
        self.dateedit.setDateTime(QDateTime.currentDateTime())
        self.dateedit.setMaximumWidth(130)

        '''!IMPORTANT! - Widget naming convention is widgetType + ROW#_COLUMN# 
        ex: combo6_3 means this combobox will be drawn in the 6th row under the 3rd combobox Column
            line2_2 means a lineEdit will be drawn in row 2 and 2n'd row of line edits respectively'''

        # defines the first row of Time off inputs

        lineWidth = 50  # width of the Hour input boxes
        for widget in self.children():
            if isinstance(widget, QLineEdit):
                widget.setMaximumWidth(lineWidth)

        self.addRow1 = QPushButton('Add Rows')
        self.addRow2 = QPushButton('Add Row')
        self.addRow1.setMaximumWidth(lineWidth + 20)
        self.addRow2.setMaximumWidth(lineWidth + 20)
        self.addRow1.setStyleSheet('color:black')
        self.addRow2.setStyleSheet('color:black')

        self.submit = QPushButton('Submit', self)
        self.submit.setStyleSheet("background-color: purple; color: white;")
        self.submit.setMinimumWidth(200)

        self.layout = QGridLayout()

        self.addUser = QPushButton('Add User')
        self.addUser.setMaximumWidth(lineWidth + 50)
        self.addUser.setStyleSheet('color:black')

        self.reset = QPushButton('Reset page')
        self.reset.setMaximumWidth(lineWidth + 50)
        self.reset.setStyleSheet('color:black')

        self.viewPrevRecs = QPushButton('Current Clock')
        self.viewPrevRecs.setStyleSheet("background-color: orange; color: black;")
        self.viewPrevRecs.setMaximumWidth(lineWidth + 50)

        self.updateRecords = QPushButton('Update Records')
        self.updateRecords.setMaximumWidth(lineWidth + 50)

        # Week Forward and Back buttons
        self.upWeek = QPushButton(' >')
        self.upWeek.setStyleSheet('font-weight: bold;font-size: 8pt; font-type: Helvetica;')
        self.downWeek = QPushButton('< ')
        self.downWeek.setStyleSheet('font-weight: bold;font-size: 8pt; font-type: Helvetica;')
        self.upWeek.setMaximumWidth(50)
        self.downWeek.setMaximumWidth(50)
        self.layout.addWidget(self.upWeek, 0, 2, Qt.AlignHCenter)
        self.layout.addWidget(self.downWeek, 0, 1, Qt.AlignHCenter)

        # Current Clocked Hours for the Week Progress Bar
        self.weekProgress = QProgressBar()
        self.weekProgress.setMaximum(40)
        self.weekProgress.setValue(30)
        self.weekProgress.setMinimumWidth(50)
        self.weekProgress.setTextVisible(False)
        self.weekProgress.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.weekProgress, 1, 11, 3, 1, Qt.AlignHCenter)
        self.weekProgress.setOrientation(Qt.Vertical)  # Flips the progress bar into verticle position
        self.weekProgress.setStyleSheet('QProgressBar::chunk { background: rgb(161, 214, 213); }')

        self.progLabel = QLabel()
        self.layout.addWidget(self.progLabel, 1, 11,
                              Qt.AlignHCenter)  # Displays number of hours clocked for week to date
        self.progLabel.setFont(QFont('Helvetica', 10))

        self.hoursLabel = QLabel('')
        self.layout.addWidget(self.hoursLabel, 1, 11, 3, 1, Qt.AlignHCenter)
        self.hoursLabel.setFont(QFont('Helvetica', 10))

        self.layout.addWidget(self.sun, 1, 4, Qt.AlignHCenter)
        self.layout.addWidget(self.mon, 1, 5, Qt.AlignHCenter)
        self.layout.addWidget(self.tues, 1, 6, Qt.AlignHCenter)
        self.layout.addWidget(self.wed, 1, 7, Qt.AlignHCenter)
        self.layout.addWidget(self.thur, 1, 8, Qt.AlignHCenter)
        self.layout.addWidget(self.fri, 1, 9, Qt.AlignHCenter)
        self.layout.addWidget(self.sat, 1, 10, Qt.AlignHCenter)

        self.deplabel = QLabel(' Department')
        self.layout.addWidget(self.deplabel, 2, 0, Qt.AlignTop)
        self.deplabel.setStyleSheet("color: grey;")
        self.deplabel.setFont(QFont('Helvetica', 9))

        self.legEntlabel = QLabel(' Legal Entity')
        self.layout.addWidget(self.legEntlabel, 2, 1, Qt.AlignTop)
        self.legEntlabel.setStyleSheet("color: grey;")
        self.legEntlabel.setFont(QFont('Helvetica', 9))

        self.tasklabel = QLabel(' Task')
        self.layout.addWidget(self.tasklabel, 2, 2, Qt.AlignTop)
        self.tasklabel.setStyleSheet("color: grey;")
        self.tasklabel.setFont(QFont('Helvetica', 9))

        self.extralabel = QLabel(' (Customer)')
        self.layout.addWidget(self.extralabel, 2, 3, Qt.AlignTop)
        self.extralabel.setStyleSheet("color: grey;")
        self.extralabel.setFont(QFont('Helvetica', 9))
        self.layout.setSpacing(3)
        self.extralabel.hide()

        self.totalLabel = QLabel('<b>Total</b>')
        self.totalLabel.setFont(QFont('Helvetica', 12))
        self.layout.addWidget(self.totalLabel,20,11,Qt.AlignHCenter)

        self.layout.setContentsMargins(50, 60, 50, 60)
        self.setLayout(self.layout)

def main():  # Login Form is called first and will remain until closed or user has entered the correct credentials
    login = LoginForm()

    def check_password():
        msg = QMessageBox()
        isUser = dataFetch.validateLogin(login.lineEdit_username.text())
        # If user is in databse, load TimeSheet and pass Username to construct form accordingly
        if isUser:
            dbuser = login.lineEdit_username.text().lower()
            login.close()  # Closes login instance (kills Window)
            timeSheet(dbuser)  # Calls timesheet form if username is correct

        else:
            msg.setText('Incorrect Username')  # Message pop up to indicate user
            msg.exec_()

    # Adds the ability to press enter instead of clicking submit
    login.lineEdit_username.returnPressed.connect(check_password)
    login.button_login.clicked.connect(check_password)
    login.show()

'''Runs TimeSheet form after user signs in'''


def timeSheet(dbuser):  # username is passed in from Login form after successful login

    form = TimeSheet()
    adm = isAdmin.AdminForm()
    recUpdate = updateRec.AdminForm()
    username = dbuser
    fullName = dataFetch.getFullName(username)  # Fetches fullname to be displayed in TimeSheet
    form.layout.addWidget(form.username, 0, 0, 1, 2, Qt.AlignTop)
    form.username.setText("Hello, " + fullName)

    # If logged in user is Admin: Two extra buttons are displayed- Add User and Update Records
    def checkAdmin():
        admin = dataFetch.isAdmin(username)
        if admin[0] == 'Yes':
            form.layout.addWidget(form.addUser, 4, 11, Qt.AlignVCenter)
            form.layout.addWidget(form.updateRecords, 6, 11, Qt.AlignVCenter)
            form.username.setText("Admin, " + fullName)
        elif admin[0] == 'No':
            pass
        else:
            pass

    checkAdmin()

    def launchAddUser():  # initiates the Add User form (Only for Admins)
        adm.show()

    form.addUser.clicked.connect(launchAddUser)

    def updateRecs():  # initiates the record update form (Only for Admins)
        recUpdate.show()

    form.updateRecords.clicked.connect(updateRecs)

    # Resets time sheet and any other forms currently open
    def resetPage():
        timeSheet(username)
        form.close()

    form.layout.addWidget(form.reset, 14, 11, Qt.AlignVCenter)
    form.reset.clicked.connect(resetPage)

    # sets all dates for the current week selected
    def setDate():
        global weekdayDate  # global variable is referenced in other places within the program
        weekdayDate = []
        newFormat = []
        getdate = form.dateedit.date()
        formatdate = getdate.toPyDate().weekday()
        appendDate = getdate.toPyDate()

        if formatdate == 6:  # if sunday is Selected (sundays day of the week == 6)
            for i in range(0, 7):
                testdate = appendDate + timedelta(days=i)
                weekdayDate.append(testdate)
        else:
            start = formatdate + 1
            testdate = appendDate - timedelta(days=start)
            for i in range(0, 7):
                weekdayDate.append(testdate + timedelta(i))
        for i in weekdayDate:
            oldFormat = datetime.strptime(str(i), '%Y-%m-%d')
            newFormat.append(str(oldFormat.strftime("%b %d")))

        form.sun.setText('<p><b>' + '&nbsp;Sun' + '<br/>' + newFormat[0] + '</b></p>')
        form.mon.setText('<b>' + '&nbsp;Mon' + '<br/>' + newFormat[1] + '</b>')
        form.tues.setText('<b>' + '&nbsp;Tue' + '<br/>' + newFormat[2] + '</b>')
        form.wed.setText('<b>' + '&nbsp;Wed' + '<br/>' + newFormat[3] + '</b>')
        form.thur.setText('<b>' + '&nbsp;Thu' + '<br/>' + newFormat[4] + '</b>')
        form.fri.setText('<b>' + '&nbsp;Fri' + '<br/>' + newFormat[5] + '</b>')
        form.sat.setText('<b>' + '&nbsp;Sat' + '<br/>' + newFormat[6] + '</b>')
        # Turns the current date Text to a Light Gray
        today = str(datetime.today().strftime("%b %d"))
        for widget in form.children():
            if isinstance(widget, QLabel):
                if today in widget.text():
                    widget.setStyleSheet('color: rgb(161, 214, 213)')
                else:
                    widget.setStyleSheet('color:White')

        # Ensures that 'Current Clock' form displays correct records based on current chosen week
        global prevEnts
        prevEnts = prevEntries.listOfPrevEnts(str(weekdayDate[0]), str(weekdayDate[6]), fullName)
        return weekdayDate

    setDate()
    # adds event listener to dateEdit (Triggers setDate Function when date is changed)
    form.dateedit.dateChanged.connect(setDate)
    form.dateedit.setMaximumDate(datetime.date(datetime.now()))  # Sets Maximum date to todays date
    form.dateedit.setMinimumDate(datetime.date(datetime.now()) - timedelta(days=14))  # Sets Minumum date to todays date  - 2 weeks
    form.layout.addWidget(form.dateedit, 0, 1,1,2, Qt.AlignHCenter)

    # Triggered when '>' button is clicked. Moves current date forward one week
    def forwardWeek():
        setDate()
        currDate = form.dateedit.date()
        futurDate = currDate.toPyDate()
        form.dateedit.setDate(futurDate + timedelta(days=7))
        weekClockedHours()
        statDays()

    form.upWeek.clicked.connect(forwardWeek)

    # Triggered when '<' button is clicked. Moves current date back one week
    def backwardWeek():
        setDate()
        currDate = form.dateedit.date()
        futurDate = currDate.toPyDate()
        form.dateedit.setDate(futurDate - timedelta(days=7))
        weekClockedHours()
        statDays()

    form.downWeek.clicked.connect(backwardWeek)

    form.layout.addWidget(form.viewPrevRecs, 5, 11, Qt.AlignVCenter)

    # Displays current clocked hours form
    def viewPrevEntries():
        prevEnts.show()

    form.viewPrevRecs.clicked.connect(viewPrevEntries)

    # Sets values for current weeks clocked hours widget (Progress bar and number of hours)
    def weekClockedHours():
        global weekHours
        weekHours = dataFetch.getPrevEntries(str(weekdayDate[0]), str(weekdayDate[6]), fullName)
        totalWeekHours = []
        for i in weekHours:
            totalWeekHours.append(i[4])
        form.weekProgress.setValue(int(sum(totalWeekHours)))  # Updates progress bar status
        form.progLabel.setText('\n' + '<b>' + str(sum(totalWeekHours)) + '</b>')
        form.hoursLabel.setText('<b><br/>H<br/>O<br/>U<br/>R<br/>S</b>')  # Vertical placement inside of progress bar

    weekClockedHours()

    '''Initiates and draws first 5 columns'''
    colCount = 0
    row1Lst = []
    row2Lst = []
    row3Lst = []
    row4Lst = []
    row5Lst = []
    for i in range(1, 5):  # Change parameters to change number of columns
        row1Lst.append(QComboBox(objectName='combo1_' + str(i)))
        row2Lst.append(QComboBox(objectName='combo2_' + str(i)))
        row3Lst.append(QComboBox(objectName='combo3_' + str(i)))
        row4Lst.append(QComboBox(objectName='combo4_' + str(i)))
        row5Lst.append(QComboBox(objectName='combo5_' + str(i)))
    for i in range(1, 8):
        row1Lst.append(QLineEdit(objectName='line1_' + str(i)))
        row2Lst.append(QLineEdit(objectName='line2_' + str(i)))
        row3Lst.append(QLineEdit(objectName='line3_' + str(i)))
        row4Lst.append(QLineEdit(objectName='line4_' + str(i)))
        row5Lst.append(QLineEdit(objectName='line5_' + str(i)))
    # draws rows 1 - 5 to sheet
    for i, n, f, t, v in zip(row1Lst, row2Lst, row3Lst, row4Lst, row5Lst):
        form.layout.addWidget(i, 2, colCount, Qt.AlignVCenter)
        form.layout.addWidget(n, 3, colCount, Qt.AlignVCenter)
        form.layout.addWidget(f, 4, colCount, Qt.AlignVCenter)
        form.layout.addWidget(t, 5, colCount, Qt.AlignVCenter)
        form.layout.addWidget(v, 6, colCount, Qt.AlignVCenter)
        colCount += 1
    # sets hint text of Hour Fields
    for i in range(4, 11):
        row1Lst[i].setPlaceholderText('   Hours')

    # input row 1
    def drawAddRow1(rowpos):
        form.layout.addWidget(form.addRow1, rowpos, 0, Qt.AlignCenter)

    drawAddRow1(13)

    # input row 6
    def drawTimeOff(rowpos):
        form.layout.addWidget(form.timeoff, rowpos, 0, Qt.AlignHCenter)
        form.timeoff.setText("Time off -")
        form.timeoff.setMaximumHeight(20)

    drawTimeOff(14)
    # bottom widgets: Submit button, Add time off button and Totals
    rowpos = 20
    form.layout.addWidget(form.submit, rowpos, 2, Qt.AlignHCenter)
    form.layout.addWidget(form.addRow2, rowpos, 0, Qt.AlignCenter)
    form.layout.addWidget(form.bottomcalc1, rowpos, 4, Qt.AlignCenter)
    form.layout.addWidget(form.bottomcalc2, rowpos, 5, Qt.AlignCenter)  # Change Column Position Here
    form.layout.addWidget(form.bottomcalc3, rowpos, 6, Qt.AlignCenter)
    form.layout.addWidget(form.bottomcalc4, rowpos, 7, Qt.AlignCenter)
    form.layout.addWidget(form.bottomcalc5, rowpos, 8, Qt.AlignCenter)
    form.layout.addWidget(form.bottomcalc6, rowpos, 9, Qt.AlignCenter)
    form.layout.addWidget(form.bottomcalc7, rowpos, 10, Qt.AlignCenter)
    form.submit.setMaximumHeight(40)

    '''Draws 5 new Rows When additionalRows() function is called'''
    addRow1Lst = []
    addRow2Lst = []
    addRow3Lst = []
    addRow4Lst = []
    addRow5Lst = []
    for i in range(1, 5):  # initiates widget objects (using object name rather than assigning to variable)
        addRow1Lst.append(QComboBox(objectName='combo7_' + str(i)))
        addRow2Lst.append(QComboBox(objectName='combo8_' + str(i)))
        addRow3Lst.append(QComboBox(objectName='combo9_' + str(i)))
        addRow4Lst.append(QComboBox(objectName='combo10_' + str(i)))
        addRow5Lst.append(QComboBox(objectName='combo11_' + str(i)))
    for i in range(1, 8):
        addRow1Lst.append(QLineEdit(objectName='line7_' + str(i)))
        addRow2Lst.append(QLineEdit(objectName='line8_' + str(i)))
        addRow3Lst.append(QLineEdit(objectName='line9_' + str(i)))
        addRow4Lst.append(QLineEdit(objectName='line10_' + str(i)))
        addRow5Lst.append(QLineEdit(objectName='line11_' + str(i)))

    addedTimeRow = []
    for count in range(12, 17):
        addedTimeRow.append(QComboBox(objectName='combo' + str(count) + '_3'))
        for i in range(1, 8):
            addedTimeRow.append(QLineEdit(objectName='line' + str(count) + '_' + str(i)))

    '''Sets Formatting for QlineEdits'''
    for i in range(4, 11):
        row1Lst[i].setMaximumWidth(50)
        row2Lst[i].setMaximumWidth(50)
        row3Lst[i].setMaximumWidth(50)
        row4Lst[i].setMaximumWidth(50)
        row5Lst[i].setMaximumWidth(50)
        addRow1Lst[i].setMaximumWidth(50)
        addRow2Lst[i].setMaximumWidth(50)
        addRow3Lst[i].setMaximumWidth(50)
        addRow4Lst[i].setMaximumWidth(50)
        addRow5Lst[i].setMaximumWidth(50)
        addedTimeRow[i - 3].setMaximumWidth(50)
        addedTimeRow[(i - 3) + 8].setMaximumWidth(50)
        addedTimeRow[(i - 3) + 16].setMaximumWidth(50)
        addedTimeRow[(i - 3) + 24].setMaximumWidth(50)
        addedTimeRow[(i - 3) + 32].setMaximumWidth(50)

    # Changes the colour of comboboxes to grey and enables text input
    for i in range(0, 4):
        row1Lst[i].setEditable(True)
        row1Lst[i].setStyleSheet('background-color: rgb(100,100,100);')
        row1Lst[i].setSizeAdjustPolicy(QComboBox.AdjustToContents)
        row2Lst[i].setEditable(True)
        row2Lst[i].setStyleSheet('background-color: rgb(100,100,100)')
        row2Lst[i].setSizeAdjustPolicy(QComboBox.AdjustToContents)
        row3Lst[i].setEditable(True)
        row3Lst[i].setStyleSheet('background-color: rgb(100,100,100)')
        row3Lst[i].setSizeAdjustPolicy(QComboBox.AdjustToContents)
        row4Lst[i].setEditable(True)
        row4Lst[i].setStyleSheet('background-color: rgb(100,100,100)')
        row4Lst[i].setSizeAdjustPolicy(QComboBox.AdjustToContents)
        row5Lst[i].setEditable(True)
        row5Lst[i].setStyleSheet('background-color: rgb(100,100,100)')
        row5Lst[i].setSizeAdjustPolicy(QComboBox.AdjustToContents)

        addRow1Lst[i].setEditable(True)
        addRow1Lst[i].setStyleSheet('background-color: rgb(100,100,100);')
        addRow1Lst[i].setSizeAdjustPolicy(QComboBox.AdjustToContents)
        addRow2Lst[i].setEditable(True)
        addRow2Lst[i].setStyleSheet('background-color: rgb(100,100,100)')
        addRow2Lst[i].setSizeAdjustPolicy(QComboBox.AdjustToContents)
        addRow3Lst[i].setEditable(True)
        addRow3Lst[i].setStyleSheet('background-color: rgb(100,100,100)')
        addRow3Lst[i].setSizeAdjustPolicy(QComboBox.AdjustToContents)
        addRow4Lst[i].setEditable(True)
        addRow4Lst[i].setStyleSheet('background-color: rgb(100,100,100)')
        addRow4Lst[i].setSizeAdjustPolicy(QComboBox.AdjustToContents)
        addRow5Lst[i].setEditable(True)
        addRow5Lst[i].setStyleSheet('background-color: rgb(100,100,100)')
        addRow5Lst[i].setSizeAdjustPolicy(QComboBox.AdjustToContents)

    row1Lst[3].hide()  # hides the fourth column of comboboxes until they are needed
    row2Lst[3].hide()
    row3Lst[3].hide()
    row4Lst[3].hide()
    row5Lst[3].hide()
    addRow1Lst[3].hide()
    addRow2Lst[3].hide()
    addRow3Lst[3].hide()
    addRow4Lst[3].hide()
    addRow5Lst[3].hide()

    '''loads values of first column of comboboxes'''

    def loadFirstCombos():
        print(username)
        combo1Val = dataFetch.combo1_1Vals(username)

        row2Lst[0].addItem("")
        row3Lst[0].addItem("")
        row4Lst[0].addItem("")
        row5Lst[0].addItem("")
        for i in combo1Val:
            row1Lst[0].addItem(i)
            row2Lst[0].addItem(i)
            row3Lst[0].addItem(i)
            row4Lst[0].addItem(i)
            row5Lst[0].addItem(i)

    loadFirstCombos()

    # Dynamically loads the next combobox in the row based on the previous comboboxes entry

    def loadNextCombos(cName):  # cName is the object name of the changed combobox
        count = 0
        comboDict = {
            1: row1Lst,
            2: row2Lst,
            3: row3Lst,
            4: row4Lst,
            5: row5Lst,
            7: addRow1Lst,
            8: addRow2Lst,
            9: addRow3Lst,
            10: addRow4Lst,
            11: addRow5Lst
        }

        if len(cName) == 8:
            rowNum = int(cName[-3])
            colNum = int(cName[-1])
        else:  # if row number is into the double digits
            rowNum = int(cName[6:8])
            colNum = int(cName[-1])
        currRowLst = comboDict[rowNum]
        currCombo = currRowLst[colNum - 1]
        nextCombo = currRowLst[colNum]
        nextCombo.clear()

        # sets hint text for comboboxes after their previous combos have been filled
        if currCombo.objectName() == 'combo1_1' and currCombo.currentText() != '':
            nextCombo.lineEdit().setPlaceholderText('Please Select Legal Entity')
        elif currCombo.objectName() == 'combo1_2':
            nextCombo.lineEdit().setPlaceholderText('Please Select a Task')


        # load each comboboxes values according to their column position
        if colNum == 1:
            newComboVals = dataFetch.combo1_2Vals(currCombo.currentText())
        if colNum == 2:
            newComboVals = dataFetch.combo1_3Vals(currCombo.currentText(), currRowLst[colNum - 2].currentText())
        if colNum == 3:
            newComboVals = dataFetch.combo1_4Vals(currCombo.currentText(), currRowLst[colNum - 2].currentText(),
                                                  currRowLst[colNum - 3].currentText())
            # Column 4 is only added if there are options to input a customer
            if len(newComboVals) > 1:
                nextCombo.show()
                form.extralabel.show()
                nextCombo.lineEdit().setPlaceholderText('Select Customer')
                form.layout.addWidget(form.submit, rowpos, 2, 1, 2, Qt.AlignHCenter)
                form.layout.addWidget(form.upWeek, 0, 2, Qt.AlignRight)
                form.layout.addWidget(form.downWeek, 0, 2, Qt.AlignLeft)
                form.layout.addWidget(form.dateedit, 0, 2, Qt.AlignHCenter)
            elif len(newComboVals) <= 1:
                form.layout.addWidget(form.upWeek, 0, 2, Qt.AlignCenter)
                form.layout.addWidget(form.downWeek, 0, 1, Qt.AlignCenter)
                form.layout.addWidget(form.dateedit, 0, 1,1,2, Qt.AlignHCenter)
                nextCombo.hide()
                form.extralabel.hide()
                form.layout.addWidget(form.submit, rowpos, 2, Qt.AlignHCenter)

        nextCombo.addItem("")
        for i in newComboVals:
            nextCombo.addItem(i)
        count += 1

    # connect comboboxes to the load next function passing in their object name to determine row and column positions
    row1Lst[0].currentTextChanged.connect(partial(loadNextCombos, str(row1Lst[0].objectName())))
    row1Lst[1].currentTextChanged.connect(partial(loadNextCombos, str(row1Lst[1].objectName())))
    row1Lst[2].currentTextChanged.connect(partial(loadNextCombos, str(row1Lst[2].objectName())))
    row2Lst[0].currentTextChanged.connect(partial(loadNextCombos, str(row2Lst[0].objectName())))
    row2Lst[1].currentTextChanged.connect(partial(loadNextCombos, str(row2Lst[1].objectName())))
    row2Lst[2].currentTextChanged.connect(partial(loadNextCombos, str(row2Lst[2].objectName())))
    row3Lst[0].currentTextChanged.connect(partial(loadNextCombos, str(row3Lst[0].objectName())))
    row3Lst[1].currentTextChanged.connect(partial(loadNextCombos, str(row3Lst[1].objectName())))
    row3Lst[2].currentTextChanged.connect(partial(loadNextCombos, str(row3Lst[2].objectName())))
    row4Lst[0].currentTextChanged.connect(partial(loadNextCombos, str(row4Lst[0].objectName())))
    row4Lst[1].currentTextChanged.connect(partial(loadNextCombos, str(row4Lst[1].objectName())))
    row4Lst[2].currentTextChanged.connect(partial(loadNextCombos, str(row4Lst[2].objectName())))
    row5Lst[0].currentTextChanged.connect(partial(loadNextCombos, str(row5Lst[0].objectName())))
    row5Lst[1].currentTextChanged.connect(partial(loadNextCombos, str(row5Lst[1].objectName())))
    row5Lst[2].currentTextChanged.connect(partial(loadNextCombos, str(row5Lst[2].objectName())))

    row1Lst[0].lineEdit().setPlaceholderText('Please Select Department')

    '''Adds 5 extra task rows (congrats you're halfway through the code...lol)'''

    def addTaskRows():
        # redraws widget so formatting doesn't look "Wonky" when extra rows are drawn
        form.layout.addWidget(form.addUser, 7, 11, Qt.AlignVCenter)
        form.layout.addWidget(form.viewPrevRecs, 8, 11, Qt.AlignVCenter)
        form.layout.addWidget(form.updateRecords, 9, 11, Qt.AlignVCenter)
        form.layout.addWidget(form.weekProgress, 1, 11, 5, 1, Qt.AlignHCenter)
        form.layout.addWidget(form.progLabel, 2, 11, Qt.AlignHCenter)
        form.layout.addWidget(form.hoursLabel, 2, 11 , 3, 1, Qt.AlignHCenter)
        form.addRow1.hide()
        form.deplabel.hide()
        form.legEntlabel.hide()
        form.tasklabel.hide()
        form.extralabel.hide()
        count = 0
        drawAddRow1(12)
        drawTimeOff(13)
        # adds the 5 extra rows of task widgets to the form
        for i, n, f, t, v in zip(addRow1Lst, addRow2Lst, addRow3Lst, addRow4Lst, addRow5Lst):
            form.layout.addWidget(i, 7, count, Qt.AlignVCenter)
            form.layout.addWidget(n, 8, count, Qt.AlignVCenter)
            form.layout.addWidget(f, 9, count, Qt.AlignVCenter)
            form.layout.addWidget(t, 10, count, Qt.AlignVCenter)
            form.layout.addWidget(v, 11, count, Qt.AlignVCenter)
            count += 1

        # loads first column of added comboboxes
        def loadFirstAddedCombos():
            combo1Val = dataFetch.combo1_1Vals(username)
            addRow1Lst[0].addItem("")
            addRow2Lst[0].addItem("")
            addRow3Lst[0].addItem("")
            addRow4Lst[0].addItem("")
            addRow5Lst[0].addItem("")
            for i in combo1Val:
                addRow1Lst[0].addItem(i)
                addRow2Lst[0].addItem(i)
                addRow3Lst[0].addItem(i)
                addRow4Lst[0].addItem(i)
                addRow5Lst[0].addItem(i)

        loadFirstAddedCombos()

        # Dynamically loads the next combobox in the row based on the previous comboboxes entry
        def loadNextAddedCombos(cName):
            comboDict = {  # Matched row Number to corresponding row List
                1: row1Lst,
                2: row2Lst,
                3: row3Lst,
                4: row4Lst,
                5: row5Lst,
                6: addRow1Lst,
                7: addRow2Lst,
                8: addRow3Lst,
                9: addRow4Lst,
                10: addRow5Lst
            }

            if len(cName) == 8:
                rowNum = int(cName[-3])  # retrieves combobox's row based on object name
                colNum = int(cName[-1])  # retrieves combobox's column based on object name
            else:
                rowNum = int(cName[5:7])
                colNum = int(cName[-1])

            currRowLst = comboDict[rowNum - 1]
            currCombo = currRowLst[colNum - 1]
            nextCombo = currRowLst[colNum]

            if colNum == 1:  # Based on which combo in row is changed, update the next in line
                newComboVals = dataFetch.combo1_2Vals(currCombo.currentText())
            if colNum == 2:
                newComboVals = dataFetch.combo1_3Vals(currCombo.currentText(), currRowLst[colNum - 2].currentText())
            if colNum == 3:
                newComboVals = dataFetch.combo1_4Vals(currCombo.currentText(), currRowLst[colNum - 2].currentText(),
                                                      currRowLst[colNum - 3].currentText())
                if len(newComboVals) > 1:  # only show 4th combo if there are customers for given task
                    nextCombo.show()
                    nextCombo.lineEdit().setPlaceholderText('Select Customer')
                    form.layout.addWidget(form.submit, rowpos, 2, 1, 2, Qt.AlignHCenter)
                    form.layout.addWidget(form.upWeek, 0, 2, Qt.AlignRight)
                    form.layout.addWidget(form.downWeek, 0, 2, Qt.AlignLeft)
                    form.layout.addWidget(form.dateedit, 0, 2, Qt.AlignHCenter)
                elif len(newComboVals) <= 1:
                    nextCombo.hide()
                    form.extralabel.hide()
                    form.layout.addWidget(form.submit, rowpos, 2, Qt.AlignHCenter)
                    form.layout.addWidget(form.upWeek, 0, 2, Qt.AlignCenter)
                    form.layout.addWidget(form.downWeek, 0, 1, Qt.AlignCenter)
                    form.layout.addWidget(form.dateedit, 0, 1, 1, 2, Qt.AlignHCenter)
            nextCombo.clear()
            nextCombo.addItem("")
            for i in newComboVals:  # adds values to next combobox based on the input of the previous one
                nextCombo.addItem(i)

        addRow1Lst[0].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow1Lst[0].objectName())))
        addRow1Lst[1].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow1Lst[1].objectName())))
        addRow1Lst[2].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow1Lst[2].objectName())))
        addRow2Lst[0].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow2Lst[0].objectName())))
        addRow2Lst[1].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow2Lst[1].objectName())))
        addRow2Lst[2].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow2Lst[2].objectName())))
        addRow3Lst[0].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow3Lst[0].objectName())))
        addRow3Lst[1].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow3Lst[1].objectName())))
        addRow3Lst[2].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow3Lst[2].objectName())))
        addRow4Lst[0].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow4Lst[0].objectName())))
        addRow4Lst[1].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow4Lst[1].objectName())))
        addRow4Lst[2].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow4Lst[2].objectName())))
        addRow5Lst[0].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow5Lst[0].objectName())))
        addRow5Lst[1].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow5Lst[1].objectName())))
        addRow5Lst[2].currentTextChanged.connect(partial(loadNextAddedCombos, str(addRow5Lst[2].objectName())))

    form.addRow1.clicked.connect(addTaskRows)
    global rowCount
    rowCount = 0

    def addTimeOff():  # Adds time-off rows one at a time (each click adds one row)
        global rowCount
        if rowCount > 0:
            form.deplabel.hide()
            form.legEntlabel.hide()
            form.tasklabel.hide()
            form.extralabel.hide()
        rowCount += 1
        if rowCount <= 5:
            if rowCount >= 5: form.addRow2.hide()  # hides the add Row Button when max rows are reached
            col = 4
            end = rowCount * 8
            start = end - 8
            form.layout.addWidget(addedTimeRow[start], rowCount + 14, 1, Qt.AlignVCenter)
            TimeOffVal = dataFetch.TimeOff()
            addedTimeRow[start].addItem("")
            for i in TimeOffVal:
                addedTimeRow[start].addItem(i)

            for i in range(start + 1, end):
                form.layout.addWidget(addedTimeRow[i], rowCount + 14, col, Qt.AlignVCenter)
                col += 1
        else:
            pass

    addTimeOff()
    addedTimeRow[0].setEditable(True)  # allows for typing/auto-fill in the comboboxes
    addedTimeRow[0].setStyleSheet('background-color: rgb(100,100,100)')
    addedTimeRow[8].currentTextChanged.connect(addTimeOff)
    addedTimeRow[8].setEditable(True)
    addedTimeRow[8].setStyleSheet('background-color: rgb(100,100,100)')
    addedTimeRow[16].currentTextChanged.connect(addTimeOff)
    addedTimeRow[16].setEditable(True)
    addedTimeRow[16].setStyleSheet('background-color: rgb(100,100,100)')
    addedTimeRow[24].currentTextChanged.connect(addTimeOff)
    addedTimeRow[24].setEditable(True)
    addedTimeRow[24].setStyleSheet('background-color: rgb(100,100,100)')
    addedTimeRow[32].currentTextChanged.connect(addTimeOff)
    addedTimeRow[32].setEditable(True)
    addedTimeRow[32].setStyleSheet('background-color: rgb(100,100,100)')

    addedTimeRow[0].lineEdit().setPlaceholderText('Select Leave Type')

    form.addRow2.clicked.connect(addTimeOff)

    '''Dynamically calculates row totals for each weekday as values are entered'''

    def calc():  # Each column is composed of every Line Edits text found under that date Column
        col1 = [row1Lst[4].text(), row2Lst[4].text(), row3Lst[4].text(), row4Lst[4].text(), row5Lst[4].text(),
                addRow1Lst[4].text(), addRow2Lst[4].text(), addRow3Lst[4].text(),
                addRow4Lst[4].text(), addRow5Lst[4].text(),
                addedTimeRow[1].text(), addedTimeRow[9].text(), addedTimeRow[17].text(), addedTimeRow[25].text(),
                addedTimeRow[33].text()]

        col2 = [row1Lst[5].text(), row2Lst[5].text(), row3Lst[5].text(), row4Lst[5].text(), row5Lst[5].text(),
                addRow1Lst[5].text(), addRow2Lst[5].text(), addRow3Lst[5].text(),
                addRow4Lst[5].text(), addRow5Lst[5].text(),
                addedTimeRow[2].text(), addedTimeRow[10].text(), addedTimeRow[18].text(), addedTimeRow[26].text(),
                addedTimeRow[34].text()]

        col3 = [row1Lst[6].text(), row2Lst[6].text(), row3Lst[6].text(), row4Lst[6].text(), row5Lst[6].text(),
                addRow1Lst[6].text(), addRow2Lst[6].text(), addRow3Lst[6].text(),
                addRow4Lst[6].text(), addRow5Lst[6].text(),
                addedTimeRow[3].text(), addedTimeRow[11].text(), addedTimeRow[19].text(), addedTimeRow[27].text(),
                addedTimeRow[35].text()]

        col4 = [row1Lst[7].text(), row2Lst[7].text(), row3Lst[7].text(), row4Lst[7].text(), row5Lst[7].text(),
                addRow1Lst[7].text(), addRow2Lst[7].text(), addRow3Lst[7].text(),
                addRow4Lst[7].text(), addRow5Lst[7].text(),
                addedTimeRow[4].text(), addedTimeRow[12].text(), addedTimeRow[20].text(), addedTimeRow[28].text(),
                addedTimeRow[36].text()]

        col5 = [row1Lst[8].text(), row2Lst[8].text(), row3Lst[8].text(), row4Lst[8].text(), row5Lst[8].text(),
                addRow1Lst[8].text(), addRow2Lst[8].text(), addRow3Lst[8].text(),
                addRow4Lst[8].text(), addRow5Lst[8].text(),
                addedTimeRow[5].text(), addedTimeRow[13].text(), addedTimeRow[21].text(), addedTimeRow[29].text(),
                addedTimeRow[37].text()]

        col6 = [row1Lst[9].text(), row2Lst[9].text(), row3Lst[9].text(), row4Lst[9].text(), row5Lst[9].text(),
                addRow1Lst[9].text(), addRow2Lst[9].text(), addRow3Lst[9].text(),
                addRow4Lst[9].text(), addRow5Lst[9].text(),
                addedTimeRow[6].text(), addedTimeRow[14].text(), addedTimeRow[22].text(), addedTimeRow[30].text(),
                addedTimeRow[38].text()]

        col7 = [row1Lst[10].text(), row2Lst[10].text(), row3Lst[10].text(), row4Lst[10].text(), row5Lst[10].text(),
                addRow1Lst[10].text(), addRow2Lst[10].text(), addRow3Lst[10].text(),
                addRow4Lst[10].text(), addRow5Lst[10].text(),
                addedTimeRow[7].text(), addedTimeRow[15].text(), addedTimeRow[23].text(), addedTimeRow[31].text(),
                addedTimeRow[39].text()]

        # Sets the bottom totals to the result of the calculation
        form.bottomcalc1.setText(calculate.calc(col1))
        form.bottomcalc2.setText(calculate.calc(col2))
        form.bottomcalc3.setText(calculate.calc(col3))
        form.bottomcalc4.setText(calculate.calc(col4))
        form.bottomcalc5.setText(calculate.calc(col5))
        form.bottomcalc6.setText(calculate.calc(col6))
        form.bottomcalc7.setText(calculate.calc(col7))

    calc()

    # responsible for altering time sheet if a Stat Holiday falls within its current week
    def statDays():
        statDates = dataFetch.checkForStat(str(weekdayDate[0]), str(weekdayDate[6]))
        rowDate = {
            str(weekdayDate[0]): 4,
            str(weekdayDate[1]): 5,
            str(weekdayDate[2]): 6,
            str(weekdayDate[3]): 7,
            str(weekdayDate[4]): 8,
            str(weekdayDate[5]): 9,
            str(weekdayDate[6]): 10
        }
        dateToCalc = {  # relates given date to the bottom calculator text to change
            str(weekdayDate[0]): form.bottomcalc1,
            str(weekdayDate[1]): form.bottomcalc2,
            str(weekdayDate[2]): form.bottomcalc3,
            str(weekdayDate[3]): form.bottomcalc4,
            str(weekdayDate[4]): form.bottomcalc5,
            str(weekdayDate[5]): form.bottomcalc6,
            str(weekdayDate[6]): form.bottomcalc7
        }
        # strtWeek = datetime.strptime(datetime.strftime(weekdayDate[0],'%Y-%m-%d'), '%Y-%m-%d')
        # endWeek = datetime.strptime(datetime.strftime(weekdayDate[6],'%Y-%m-%d'), '%Y-%m-%d')
        # today = datetime.today()
        '''If a stat date falls within the current selected week then 8 hours is autofilled to that day'''
        if len(statDates) > 0:
            for i in statDates:
                # Greys out and locks the column of hour inputs under the stat date
                dateKey = rowDate.get(str(i[0]))
                row1Lst[dateKey].setEnabled(False)
                row1Lst[dateKey].setStyleSheet('background-color: rgb(70,70,70)')
                row2Lst[dateKey].setEnabled(False)
                row2Lst[dateKey].setStyleSheet('background-color: rgb(70,70,70)')
                row3Lst[dateKey].setEnabled(False)
                row3Lst[dateKey].setStyleSheet('background-color: rgb(70,70,70)')
                row4Lst[dateKey].setEnabled(False)
                row4Lst[dateKey].setStyleSheet('background-color: rgb(70,70,70)')
                row5Lst[dateKey].setEnabled(False)
                row5Lst[dateKey].setStyleSheet('background-color: rgb(70,70,70)')
                addRow1Lst[dateKey].setEnabled(False)
                addRow1Lst[dateKey].setStyleSheet('background-color:rgb(70,70,70)')
                addRow2Lst[dateKey].setEnabled(False)
                addRow2Lst[dateKey].setStyleSheet('background-color: rgb(70,70,70)')
                addRow3Lst[dateKey].setEnabled(False)
                addRow3Lst[dateKey].setStyleSheet('background-color: rgb(70,70,70)')
                addRow4Lst[dateKey].setEnabled(False)
                addRow4Lst[dateKey].setStyleSheet('background-color: rgb(70,70,70)')
                addRow5Lst[dateKey].setEnabled(False)
                addRow5Lst[dateKey].setStyleSheet('background-color: rgb(70,70,70)')
                addedTimeRow[dateKey - 3].setEnabled(False)
                # Change color of cell containing the auto filled 8 hours
                addedTimeRow[dateKey - 3].setStyleSheet('background-color: rgb(161, 214, 213); color: black')
                addedTimeRow[dateKey + 5].setEnabled(False)
                addedTimeRow[dateKey + 5].setStyleSheet('background-color: rgb(70,70,70)')
                addedTimeRow[dateKey + 13].setEnabled(False)
                addedTimeRow[dateKey + 13].setStyleSheet('background-color: rgb(70,70,70)')
                addedTimeRow[dateKey + 21].setEnabled(False)
                addedTimeRow[dateKey + 21].setStyleSheet('background-color: rgb(70,70,70)')
                addedTimeRow[dateKey + 29].setEnabled(False)
                addedTimeRow[dateKey + 29].setStyleSheet('background-color: rgb(70,70,70)')

            flat_list = []
            for sublist in weekHours:
                for item in sublist:
                    flat_list.append(item)
            if 'Stat Holiday' not in flat_list:
                # Only auto fill 8 hours if user hasn't submitted a timesheet containing the Stat
                addedTimeRow[0].setCurrentText('Stat Holiday')
                addedTimeRow[dateKey - 3].setText('8')
                addedTimeRow[0].setEnabled(False)
            dateToCalc[str(i[0])].setText('8.00\n(stat)')
        else:
            calc()
            for widget in form.children():  # reset the stat widgets if no longer in week containing Stat
                if isinstance(widget, QLineEdit):
                    widget.setEnabled(True)
                    widget.setStyleSheet('background-color: 25, 25, 25')
                    widget.setText('')
                elif isinstance(widget, QComboBox):
                    widget.setCurrentText('')
                    widget.setEnabled(True)
            for i in range(4, 10):
                addRow1Lst[i].setEnabled(True)
                addRow2Lst[i].setEnabled(True)
                addRow3Lst[i].setEnabled(True)
                addRow4Lst[i].setEnabled(True)
                addRow5Lst[i].setEnabled(True)
                addRow1Lst[i].setStyleSheet('background-color: 25, 25, 25')
                addRow2Lst[i].setStyleSheet('background-color: 25, 25, 25')
                addRow3Lst[i].setStyleSheet('background-color: 25, 25, 25')
                addRow4Lst[i].setStyleSheet('background-color: 25, 25, 25')
                addRow5Lst[i].setStyleSheet('background-color: 25, 25, 25')

            for i in range(1, 8):
                addedTimeRow[i].setEnabled(True)
                addedTimeRow[i+8].setEnabled(True)
                addedTimeRow[i+16].setEnabled(True)
                addedTimeRow[i+24].setEnabled(True)
                addedTimeRow[i+32].setEnabled(True)
                addedTimeRow[i].setStyleSheet('background-color: 25, 25, 25')
                addedTimeRow[i+8].setStyleSheet('background-color: 25, 25, 25')
                addedTimeRow[i+16].setStyleSheet('background-color: 25, 25, 25')
                addedTimeRow[i+24].setStyleSheet('background-color: 25, 25, 25')
                addedTimeRow[i+32].setStyleSheet('background-color: 25, 25, 25')

    statDays()
    if addedTimeRow[0].currentText() != 'Stat Holiday':
        addedTimeRow[0].currentTextChanged.connect(addTimeOff)
    # Connects lineEdits to calc method (for widgets initialized in TimeSheet class)
    for widget in form.children():
        if isinstance(widget, QLineEdit):
            widget.textChanged.connect(calc)

    # Connects lineEdits to calc method (for widgets initialized within main meathod)
    for i in range(4, 11):
        addRow1Lst[i].textChanged.connect(calc)
        addRow2Lst[i].textChanged.connect(calc)
        addRow3Lst[i].textChanged.connect(calc)
        addRow4Lst[i].textChanged.connect(calc)
        addRow5Lst[i].textChanged.connect(calc)
        addedTimeRow[i - 3].textChanged.connect(calc)
        addedTimeRow[(i - 3) + 8].textChanged.connect(calc)
        addedTimeRow[(i - 3) + 16].textChanged.connect(calc)
        addedTimeRow[(i - 3) + 24].textChanged.connect(calc)
        addedTimeRow[(i - 3) + 32].textChanged.connect(calc)
    '''Here the Keys are the corresponding row numbers of the contained widgets
            while the Values are the current values present in each widget'''

    def returnvals(lineeditposX, lineeditposY, lineText, name):
        lineEditDict = {
            '1': [row1Lst[0].currentText(), row1Lst[1].currentText(), row1Lst[2].currentText(),
                  row1Lst[3].currentText()],
            '2': [row2Lst[0].currentText(), row2Lst[1].currentText(), row2Lst[2].currentText(),
                  row2Lst[3].currentText()],
            '3': [row3Lst[0].currentText(), row3Lst[1].currentText(), row3Lst[2].currentText(),
                  row3Lst[3].currentText()],
            '4': [row4Lst[0].currentText(), row4Lst[1].currentText(), row4Lst[2].currentText(),
                  row4Lst[3].currentText()],
            '5': [row5Lst[0].currentText(), row5Lst[1].currentText(), row5Lst[2].currentText(),
                  row5Lst[3].currentText()],
            '6': ['None', 'None'],
            '7': [addRow1Lst[0].currentText(), addRow1Lst[1].currentText(), addRow1Lst[2].currentText(),
                  addRow1Lst[3].currentText()],
            '8': [addRow2Lst[0].currentText(), addRow2Lst[1].currentText(), addRow1Lst[2].currentText(),
                  addRow2Lst[3].currentText()],
            '9': [addRow3Lst[0].currentText(), addRow3Lst[1].currentText(), addRow3Lst[2].currentText(),
                  addRow3Lst[3].currentText()],
            '10': [addRow4Lst[0].currentText(), addRow4Lst[1].currentText(), addRow4Lst[2].currentText(),
                   addRow4Lst[3].currentText()],
            '11': [addRow5Lst[0].currentText(), addRow5Lst[1].currentText(), addRow5Lst[2].currentText(),
                   addRow5Lst[3].currentText()],
            '12': ['None', 'None', addedTimeRow[0].currentText(), 'None'],
            '13': ['None', 'None', addedTimeRow[8].currentText(), 'None'],
            '14': ['None', 'None', addedTimeRow[16].currentText(), 'None'],
            '15': ['None', 'None', addedTimeRow[24].currentText(), 'None'],
            '16': ['None', 'None', addedTimeRow[32].currentText(), 'None']
        }
        # uses the row number of the line edit to find corresponding comboboxes (Same Row)
        valueLst1 = lineEditDict[lineeditposY]
        c1 = valueLst1[0]
        c2 = valueLst1[1]  # c stands for combobox
        c3 = valueLst1[2]
        c4 = valueLst1[3]
        dateDict = {
            '1': str(weekdayDate[0]),  # column 1 = Sunday
            '2': str(weekdayDate[1]),
            '3': str(weekdayDate[2]),
            '4': str(weekdayDate[3]),
            '5': str(weekdayDate[4]),
            '6': str(weekdayDate[5]),
            '7': str(weekdayDate[6])  # column 7 = Saturday
        }
        dateLabel = dateDict[lineeditposX]
        return c1, c2, c3, c4, float(lineText), dateLabel, name

    '''On Submit button press: validate forms inputs and send them to DB'''
    submitLst = []
    filledLineEdit = []
    filledCombo = []
    msg = QMessageBox()

    def submitButton():
        filledCombo.clear()
        filledLineEdit.clear()
        isValid1 = True
        isValid2 = True
        isNum = True

        for widget in form.children():
            if isinstance(widget, QComboBox):  # loops through all Comboboxes
                # Only get combobox values if all 3 in row are filled out
                if widget.currentText() != '' and str(
                        widget.objectName()[-1]) == '3' and widget.currentText() != 'Select Leave Type' \
                        and widget.currentText() != 'Please Select Department' and widget.currentText() != 'Please Select Legal Entity' \
                        and widget.currentText() != 'Please Select a Task':
                    combostr = str(widget.objectName())
                    if len(combostr) == 8:
                        combopos = combostr[5]
                    else:
                        combopos = combostr[5:7]
                    filledCombo.append(combopos)

            elif isinstance(widget, QLineEdit):  # loops through all lineEdits
                if widget.text() != '':
                    if widget.text().replace('.', '', 1).isdigit():
                        isNum = True
                    else:
                        isNum = False
                    lineeditstr = str(widget.objectName())
                    if len(lineeditstr) == 7:
                        lineeditpos = lineeditstr[4]
                    else:
                        lineeditpos = lineeditstr[4:6]  # Row position if in double digits (rows > 9)
                    filledLineEdit.append(lineeditpos)

        if len(filledCombo) > 0 and len(filledLineEdit) > 0:  # Checks if un-empty widgets belong to same row
            for i in filledCombo:
                if i not in filledLineEdit:
                    isValid1 = False
            for i in filledLineEdit:
                if i not in filledCombo:
                    isValid2 = False

            # Only if timeSheet has been filled out correctly
            if isValid1 is True and isValid2 is True and isNum is True:
                ret = QMessageBox.question(form, 'Attention Required', 'Are you sure you want to submit?',
                                           QMessageBox.Yes | QMessageBox.No)
                if ret == QMessageBox.No:
                    pass
                elif ret == QMessageBox.Yes:
                    submitLst.clear()
                    for widget in form.children():
                        if isinstance(widget, QLineEdit):
                            if widget.text() != '':
                                lineeditstr = str(widget.objectName())
                                print(lineeditstr)
                                if len(lineeditstr) == 7:
                                    lineeditposX = lineeditstr[6]
                                    lineeditposY = lineeditstr[4]
                                else:
                                    lineeditposX = lineeditstr[7]
                                    lineeditposY = lineeditstr[4:6]  # row position if in double digits (rows > 9)

                                submitLst.append(returnvals(lineeditposX, lineeditposY, widget.text(), fullName))

                    prevEnter = dataFetch.checkForRec(submitLst)  # checks if similar entries have previously been made
                    if len(prevEnter) != 0:
                        prevDep = 'Department: ' + prevEnter[0][0]
                        prevEnt = 'Legal Entity: ' + prevEnter[0][1]
                        prevTask = 'Task: ' + prevEnter[0][2]
                        prevHour = 'Hours clocked: ' + str(prevEnter[0][3])
                        prevDate = 'Date: ' + str(prevEnter[0][4])
                        preStr = '\n' + prevDep + '\n' + prevEnt + '\n' + prevTask + '\n' + prevHour + '\n' + prevDate[
                                                                                                              0:16] + '\n'

                        ques = QMessageBox.question(form, 'Attention required',
                                                    'You Have Previous Entries For:' + preStr +
                                                    'are you sure you want to submit?\n \n' +
                                                    'PREVIOUS ENTRIES WILL NOT BE OVERWRITTEN',
                                                    QMessageBox.Yes | QMessageBox.No)
                        if ques == QMessageBox.No:
                            pass
                        elif ques == QMessageBox.Yes:
                            dataFetch.pushToDB(submitLst)
                            print('Pushing following record to DB: ' + str(submitLst))
                            msg.setText('TimeSheet Submitted')
                            msg.exec_()
                            timeSheet(username)  # resets timesheet form
                            form.close()
                    else:
                        dataFetch.pushToDB(submitLst)
                        print('Pushing following record to DB: ' + str(submitLst))
                        form.children().clear()
                        msg.setText('TimeSheet Submitted')
                        msg.exec_()
                        timeSheet(username)  # resets timesheet form
                        form.close()

            elif isValid1 is False or isValid2 is False or isNum is False:
                msg.setText('Please verify fields')
                msg.exec_()
        else:
            msg.setText('Please verify fields')
            msg.exec_()

        filledLineEdit.clear()
        filledCombo.clear()

    form.submit.clicked.connect(submitButton)
    form.show()

    '''Loads login form when application is run'''



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    dark_palette = QPalette()

    '''Adds a dark colour palette to form'''
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(130, 130, 130))
    dark_palette.setColor(QPalette.ButtonText, Qt.black)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(161, 214, 213))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)

    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #a1a1a1; border: 1px solid white; }")
    main()
    sys.exit(app.exec_())