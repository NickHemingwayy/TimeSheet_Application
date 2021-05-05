from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QGridLayout
import sys
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(640, 480)
        self.layout = QGridLayout()

        self.setWindowTitle('Create Month End Folders')
        thisMonth = datetime.today().strftime('%Y-%m')
        self.runningForLabel = QLabel('Creating folders for: ' + thisMonth)

        self.testLabel = QLabel('Test')

        self.layout.addWidget(self.testLabel, 1, 1)
        self.layout.addWidget(self.runningForLabel, 0, 0)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(50, 10, 50, 10)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
