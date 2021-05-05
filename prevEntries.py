import sys
from PyQt5.Qt import *
import dataFetch


class listOfPrevEnts(QWidget):
    def __init__(self, startDate, endDate, username):
        super().__init__()

        # Initialize Qt widgets
        self.setWindowTitle('This Weeks Entries')
        self.resize(800, 400)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Scroll Area is used in the case of having many records to display.
        scroll = QScrollArea(self)
        layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)

        # table widget will act as a sort of spreadsheet for displaying users previous entries
        self.tableWidget = QTableWidget()

        # set column count
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)

        # Checks if there are any previous entries for the week to date
        preEnts = dataFetch.getPrevEntries(startDate, endDate, username)
        self.tableWidget.setRowCount(len(preEnts)+2)
        font = QFont()
        font.setBold(True)

        self.tableWidget.setStyleSheet('background-color: rgb(100,100,100)')
        # Sets Heading for the spreadsheet
        self.tableWidget.setItem(0, 0, QTableWidgetItem('Department'))
        self.tableWidget.item(0, 0).setFont(font)
        self.tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(0, 1, QTableWidgetItem('Legal Entity'))
        self.tableWidget.item(0, 1).setFont(font)
        self.tableWidget.item(0, 1).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(0, 2, QTableWidgetItem('Task'))
        self.tableWidget.item(0, 2).setFont(font)
        self.tableWidget.item(0, 2).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(0, 3, QTableWidgetItem('Customer'))
        self.tableWidget.item(0, 3).setFont(font)
        self.tableWidget.item(0, 3).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(0, 4, QTableWidgetItem('Hours Worked'))
        self.tableWidget.item(0, 4).setFont(font)
        self.tableWidget.item(0, 4).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(0, 5, QTableWidgetItem('Date Worked'))
        self.tableWidget.item(0, 5).setFont(font)
        self.tableWidget.item(0, 5).setTextAlignment(Qt.AlignCenter)
        count = 1
        hourSum = 0
        # loops through retrieved records from DB and adds them to the table
        for i in preEnts:
            self.tableWidget.setItem(count, 0, QTableWidgetItem(str(i[0])))
            self.tableWidget.setItem(count, 1, QTableWidgetItem(str(i[1])))
            self.tableWidget.setItem(count, 2, QTableWidgetItem(str(i[2])))
            self.tableWidget.setItem(count, 3, QTableWidgetItem(str(i[3])))
            self.tableWidget.setItem(count, 4, QTableWidgetItem(str(i[4])))
            self.tableWidget.setItem(count, 5, QTableWidgetItem(str(i[5])))
            hourSum += float(i[4])
            count += 1
        # Sets the last row of the table to total the Hours column
        self.tableWidget.setItem(count, 0, QTableWidgetItem('Total'))
        self.tableWidget.item(count, 0).setFont(font)
        self.tableWidget.setItem(count, 4, QTableWidgetItem(str(hourSum)))
        self.tableWidget.item(count, 4).setFont(font)
        self.tableWidget.item(count, 4).setForeground(QBrush(QColor(0,0,0)))
        self.tableWidget.item(count, 4).setBackground(QColor(161, 214, 213))

        scrollLayout.addWidget(self.tableWidget)  # Adds Table to scrollable window
        scroll.setWidget(scrollContent)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    adm = listOfPrevEnts('2020-05-29','2020-09-29','nhemingway')
    adm.show()
    sys.exit(app.exec_())