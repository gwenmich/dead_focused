from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import QLabel


class PomodoroTimer(QTimer):

    started = Signal()
    paused = Signal()
    stopped = Signal()
    focus_ended = Signal()
    break_ended = Signal()

    def __init__(self, font_func, shadow_func):
        super().__init__()
        self.focus_mins = 25
        self.break_mins = 5
        self.seconds_remaining = self.focus_mins * 60
        self.mode = "focus"

        # animation_timer text
        self.label = QLabel(f"{self.focus_mins:02}:00")
        shadow_func(self.label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(f"""
            color: #e8e7df;
            font-family: "{font_func}";
            font-size: 28px;
            font-weight: bold;
            background: transparent;
            padding-top: 50px;
            """)

    def start_timer(self):
        if not self.isActive():
            self.start(1000)
            self.started.emit()

    def tick_down(self):
        self.seconds_remaining -= 1
        if self.seconds_remaining == 0:
            self.stop()
            if self.mode == "focus":
                self.focus_ended.emit()
                self.seconds_remaining = self.break_mins * 60
                self.mode = "break"
            else:
                self.break_ended.emit()
                self.seconds_remaining = self.focus_mins * 60
                self.mode = "focus"

        minutes, leftover_secs = divmod(self.seconds_remaining, 60)
        self.label.setText(f"{minutes:02}:{leftover_secs:02}")


    def pause_timer(self):
        self.stop()
        self.paused.emit()

    def reset_timer(self):
        self.stop()
        self.seconds_remaining = self.focus_mins * 60
        self.label.setText(f"{self.focus_mins:02}:00")
        self.stopped.emit()
