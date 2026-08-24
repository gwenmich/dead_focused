import sys, random
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QStackedLayout, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QMovie, QFontDatabase, QColor
from paths import FONTS_DIR
from button import Button
from ghost import Ghost


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

        # animation_timer setup and mode
        self.timer = QTimer()
        self.seconds_remaining = 1500
        self.mode = "study"

        # animation_timer text
        self.timer_label = QLabel("25:00")
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setColor(QColor(0, 0, 0, 180))
        self.shadow_effect.setOffset(2, 2)
        self.shadow_effect.setBlurRadius(6)
        self.timer_label.setGraphicsEffect(self.shadow_effect)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet(f"""
            color: #e8e7df;
            font-family: "{self.retrieve_font()}";
            font-size: 28px;
            font-weight: bold;
            background: transparent;
            padding-top: 50px;
            """)

        # ghost appearance timer
        self.ghost_timer = QTimer()
        self.ghost_timer.timeout.connect(self.spawn_ghost)

        # UI buttons
        play_btn = Button("play.png", "play_pressed.png", 48, "ui_btn_press.wav", "ui_btn_release.wav")
        pause_btn = Button("pause.png", "pause_pressed.png", 48, "ui_btn_press.wav", "ui_btn_release.wav")
        reset_btn = Button("reset.png", "reset_pressed.png", 48, "ui_btn_press.wav", "ui_btn_release.wav")

        # UI buttons operations
        play_btn.pressed.connect(self.start_timer)
        play_btn.pressed.connect(self.ghost_timer.start)
        self.timer.timeout.connect(self.tick_down)
        pause_btn.pressed.connect(self.pause_timer)
        reset_btn.pressed.connect(self.reset_timer)

        # music player
        left_arrow = Button("left_arrow.png", "left_arrow_pressed.png", 32, "arrow_press.wav", "arrow_release.wav")
        right_arrow = Button("right_arrow.png", "right_arrow_pressed.png", 32, "arrow_press.wav", "arrow_release.wav")

        self.music_label = QLabel("music player")
        self.music_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.music_label.setStyleSheet(f"""
            color: #e8e7df;
            font-family: "{self.retrieve_font()}";
            font-size: 16px;
            background: transparent;
            """)


        # stack background and animation_timer
        self.scene = QWidget()
        self.scene.setFixedSize(512, 512)
        bg_stack = QStackedLayout(self.scene)
        bg_stack.setStackingMode(QStackedLayout.StackingMode.StackAll)
        bg_stack.addWidget(self.bg_label)
        bg_stack.addWidget(self.timer_label)
        bg_stack.setCurrentWidget(self.timer_label)

        # set horizontal box layout for buttons
        buttons = QWidget()
        buttons_layout = QHBoxLayout(buttons)
        buttons_layout.addWidget(play_btn)
        buttons_layout.addWidget(pause_btn)
        buttons_layout.addWidget(reset_btn)

        # set horizontal box layout for music player
        music_player = QWidget()
        music_layout = QHBoxLayout(music_player)
        music_layout.addWidget(left_arrow)
        music_layout.addWidget(self.music_label)
        music_layout.addWidget(right_arrow)

        # set vertical box layout as main layout
        app_layout = QWidget()
        app_layout.setStyleSheet("""
            background-color: #176b87;""")
        app_stack = QVBoxLayout(app_layout)
        app_stack.setContentsMargins(0, 0, 0, 0)
        app_stack.setAlignment(Qt.AlignmentFlag.AlignTop)
        app_stack.addWidget(self.scene)
        app_stack.addWidget(buttons)
        app_stack.addWidget(music_player)


        self.setCentralWidget(app_layout)

    # get pixel font
    def retrieve_font(self):
        font_path = FONTS_DIR / "pixel_font.ttf"
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        return font_family

    # TIMER FUNCTIONS
    def start_timer(self):
        if not self.timer.isActive():
            self.timer.start(1000)

    # animation_timer tick down and update text
    def tick_down(self):
        self.seconds_remaining -= 1
        if self.seconds_remaining == 0:
            self.timer.stop()
            if self.mode == "study":
                self.seconds_remaining = 300
                self.mode = "break"
            else:
                self.seconds_remaining = 1500
                self.mode = "study"

        minutes, leftover_secs = divmod(self.seconds_remaining, 60)
        self.timer_label.setText(f"{minutes:02}:{leftover_secs:02}")

    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()

    def reset_timer(self):
        self.timer.stop()
        self.seconds_remaining = 1500
        self.timer_label.setText("25:00")

    def get_random_ghost(self):
        ghosts = [
            ("ghost1_left.png", "left"),
            ("ghost1_right.png", "right"),
            ("ghost2_left.png", "left"),
            ("ghost2_right.png", "right")
        ]
        ghost_file, direction = random.choice(ghosts)
        return Ghost(ghost_file, 128, 128, direction)


    def spawn_ghost(self):
        if self.timer.isActive():
            self.ghost_timer.setInterval(random.randrange(15000, 25000))
            self.ghost = self.get_random_ghost()
            self.ghost.setParent(self.scene)
            self.ghost.show()




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()