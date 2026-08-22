from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from paths import IMAGES_DIR

class Button(QPushButton):

    def __init__(self, btn_image, pressed_btn_img):
        super().__init__()
        self.btn_img_path = str(IMAGES_DIR / btn_image)
        self.pressed_btn_img_path = str(IMAGES_DIR / pressed_btn_img)
        self.setIcon(QIcon(self.btn_img_path))
        self.setIconSize(QSize(48, 48))
        self.setFixedSize(48, 48)

        self.pressed.connect(self.on_press)
        self.released.connect(self.on_release)

    # show pressed image when pressing button
    def on_press(self):
        self.setIcon(QIcon(self.pressed_btn_img_path))

    # show default image on button release
    def on_release(self):
        self.setIcon(QIcon(self.btn_img_path))
