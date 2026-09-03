from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QSlider, QWidget, QHBoxLayout
from button import Button

class Settings(QDialog):

    volume_changed = Signal(int)

    def __init__(self, current_focus_mins, current_break_mins, current_volume, font_func):
        super().__init__()
        self.setWindowTitle("Settings")

        self.focus_label = QLabel("Focus duration")
        self.focus_spinbox = self.create_spinbox(current_focus_mins)
        self.break_label = QLabel("Break duration")
        self.break_spinbox = self.create_spinbox(current_break_mins)
        self.volume_label = QLabel("Volume")
        self.volume_slider = self.create_slider(current_volume)
        self.volume_slider.valueChanged.connect(self.volume_changed.emit)

        settings_layout = QVBoxLayout(self)
        settings_layout.addWidget(self.focus_label)
        settings_layout.addWidget(self.focus_spinbox)
        settings_layout.addWidget(self.break_label)
        settings_layout.addWidget(self.break_spinbox)
        settings_layout.addWidget(self.volume_label)
        settings_layout.addWidget(self.volume_slider)

        self.ok_btn = Button("ok_btn.png", "ok_btn_pressed.png", 128, 64, "set_btn_press.wav", "set_btn_release.wav")
        self.cancel_btn = Button("cancel_btn.png", "cancel_btn_pressed.png", 128, 64, "set_btn_press.wav", "set_btn_release.wav")

        self.ok_btn.released.connect(self.accept)
        self.cancel_btn.released.connect(self.reject)

        buttons = QWidget()
        buttons_layout = QHBoxLayout(buttons)
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.ok_btn)

        settings_layout.addWidget(buttons)


        self.setStyleSheet(f"""
            background-color: #879b99;
            font-family: {font_func};
            """)



    def create_spinbox(self, current_mins):
        spinbox = QSpinBox()
        spinbox.setValue(current_mins)
        spinbox.setMinimum(00)
        spinbox.setMaximum(59)
        return spinbox

    def create_slider(self, current_value):
        slider = QSlider(Qt.Orientation.Horizontal)
        volume = int(current_value * 100)
        slider.setValue(volume)
        slider.setMinimum(0)
        slider.setMaximum(100)
        return slider
