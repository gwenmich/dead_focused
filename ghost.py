from PySide6.QtCore import QRect, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel
from paths import IMAGES_DIR


class Ghost(QLabel):

    def __init__(self, spritesheet_path, frame_width, frame_height):
        super().__init__()
        self.spritesheet = QPixmap(str(IMAGES_DIR / spritesheet_path))
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.setFixedSize(self.frame_width, self.frame_height)
        self.current_frame = 0
        self.x = 512 + frame_width
        self.y = 300
        self.setStyleSheet("""
            background: transparent;
            """)

        # timer for bobbing animation
        self.animation_timer = QTimer()
        self.animation_timer.start(180)
        self.animation_timer.timeout.connect(self.animate)

        # timer for moving across screen
        self.moving_timer = QTimer()
        self.moving_timer.start(80)
        self.moving_timer.timeout.connect(self.move_forward)


    # get frame from spritesheet
    def get_frame(self, frame_index):
        frame = self.spritesheet.copy(QRect(self.frame_width * frame_index, 0, self.frame_width, self.frame_height))
        return frame

    def animate(self):
        self.setPixmap(self.get_frame(self.current_frame))
        self.current_frame += 1
        if self.current_frame == 8:
            self.current_frame = 0

    def move_forward(self):
        self.x -= 5
        self.move(self.x, self.y)

