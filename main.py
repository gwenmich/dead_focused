import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import QSize
from PySide6.QtGui import QMovie


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dead Focused")
        self.setFixedSize(QSize(512, 700))

        self.background = QMovie("background.gif")
        self.label = QLabel("background")
        self.setCentralWidget(self.label)
        self.label.setScaledContents(True)
        self.label.setFixedSize(QSize(512, 512))
        self.label.setMovie(self.background)
        self.background.start()
        self.label.show()




app = QApplication(sys.argv)

window = MainWindow()
window.show()


app.exec()