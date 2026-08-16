import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QStackedLayout
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QMovie, QFontDatabase, QFont
from pathlib import Path

# set absolute paths for folders
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dead Focused")
        self.setFixedSize(QSize(512, 700))

        # background gif
        self.background = QMovie("assets/images/background.gif")
        self.bg_label = QLabel()
        self.bg_label.setScaledContents(True)
        self.bg_label.setFixedSize(QSize(512, 512))
        self.bg_label.setMovie(self.background)
        self.background.start()

        # timer text
        self.timer_label = QLabel("25:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet(f"""
            color: #a8ffb0;
            font-family: "{self.retrieve_font()}";
            font-size: 28px;
            font-weight: bold;
            background: transparent;""")

        # stack background and timer
        scene = QWidget()
        scene.setFixedSize(512, 512)
        stack = QStackedLayout(scene)
        stack.setStackingMode(QStackedLayout.StackingMode.StackAll)
        stack.addWidget(self.bg_label)
        stack.addWidget(self.timer_label)
        stack.setCurrentWidget(self.timer_label)

        self.setCentralWidget(scene)

    # get pixel font
    def retrieve_font(self):
        font_path = FONTS_DIR / "pixel_font.ttf"
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        return font_family


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()