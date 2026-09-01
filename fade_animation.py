from PySide6.QtCore import QTimer, QRect
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel
from paths import IMAGES_DIR


class FadeAnimation(QLabel):

    def __init__(self):
        super().__init__()
        self.spritesheet = QPixmap(str(IMAGES_DIR / "fading_ghost.png"))
        self.frame_width = 512
        self.frame_height = 512
        self.setFixedSize(self.frame_width, self.frame_height)
        self.current_frame = 0

        self.setStyleSheet("""
            background: transparent;
            """)

        self.animation_timer = QTimer()
        self.animation_timer.start(180)
        self.animation_timer.timeout.connect(self.animate)


    def get_frame(self, frame_index):
        frame = self.spritesheet.copy(QRect(self.frame_width * frame_index, 0, self.frame_width, self.frame_height))
        return frame

    def animate(self):
        self.setPixmap(self.get_frame(self.current_frame))
        self.current_frame += 1
        if self.current_frame == 28:
            self.animation_timer.stop()
            self.deleteLater()