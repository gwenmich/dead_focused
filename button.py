from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QSize, QUrl
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtGui import QIcon
from paths import IMAGES_DIR, SOUNDS_DIR

class Button(QPushButton):

    def __init__(self, btn_image, pressed_btn_img, size, press_sound, release_sound):
        super().__init__()
        self.btn_img_path = str(IMAGES_DIR / btn_image)
        self.pressed_btn_img_path = str(IMAGES_DIR / pressed_btn_img)
        self.setIcon(QIcon(self.btn_img_path))
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size, size)

        self.pressed_sound = QSoundEffect()
        self.pressed_sound.setSource(QUrl.fromLocalFile(str(SOUNDS_DIR / press_sound)))
        self.pressed_sound.setVolume(0.5)
        self.released_sound = QSoundEffect()
        self.released_sound.setSource(QUrl.fromLocalFile(str(SOUNDS_DIR / release_sound)))

        self.pressed.connect(self.on_press)
        self.released.connect(self.on_release)

    # show pressed image when pressing button
    def on_press(self):
        self.setIcon(QIcon(self.pressed_btn_img_path))
        self.pressed_sound.play()

    # show default image on button release
    def on_release(self):
        self.setIcon(QIcon(self.btn_img_path))
        self.released_sound.play()
