import sys, random
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QStackedLayout, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import QSize, Qt, QTimer, QUrl
from PySide6.QtGui import QMovie, QFontDatabase, QColor
from paths import FONTS_DIR, SOUNDS_DIR
from button import Button
from ghost import Ghost
from settings import Settings
from music_player import MusicPlayer
from pomodoro_timer import PomodoroTimer


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

        # animation end sounds
        self.focus_end_audio = QSoundEffect()
        self.focus_end_audio.setSource(QUrl.fromLocalFile(str(SOUNDS_DIR / "rest_in_peace.wav")))
        self.focus_end_audio.setVolume(0.6)
        self.break_end_audio = QSoundEffect()
        self.break_end_audio.setSource(QUrl.fromLocalFile(str(SOUNDS_DIR / "time_is_up.wav")))
        self.break_end_audio.setVolume(0.6)

        # ghost appearance timer
        self.ghost_timer = QTimer()
        self.ghost_timer.timeout.connect(self.spawn_ghost)


        # UI buttons
        play_btn = Button("play.png", "play_pressed.png", 48, "ui_btn_press.wav", "ui_btn_release.wav")
        pause_btn = Button("pause.png", "pause_pressed.png", 48, "ui_btn_press.wav", "ui_btn_release.wav")
        reset_btn = Button("reset.png", "reset_pressed.png", 48, "ui_btn_press.wav", "ui_btn_release.wav")

        settings_btn = Button("settings.png", "settings_pressed.png", 32, "arrow_press.wav", "arrow_release.wav")
        settings_btn.move(469, 10)
        self.apply_shadow(settings_btn)


        # music player & arrow buttons
        left_arrow = Button("left_arrow.png", "left_arrow_pressed.png", 32, "arrow_press.wav", "arrow_release.wav")
        right_arrow = Button("right_arrow.png", "right_arrow_pressed.png", 32, "arrow_press.wav", "arrow_release.wav")

        self.music_player = MusicPlayer(self.retrieve_font())

        left_arrow.pressed.connect(self.music_player.play_previous)
        right_arrow.pressed.connect(self.music_player.play_next)

        # pomodoro timer
        self.timer = PomodoroTimer(self.retrieve_font(), self.apply_shadow)
        self.timer.focus_ended.connect(lambda: self.music_player.duck_audio_volume(self.focus_end_audio))
        self.timer.break_ended.connect(lambda: self.music_player.duck_audio_volume(self.break_end_audio))
        self.timer.started.connect(self.music_player.play)
        self.timer.paused.connect(self.music_player.pause)
        self.timer.stopped.connect(self.music_player.stop)

        # UI buttons operations
        play_btn.pressed.connect(self.timer.start_timer)
        play_btn.pressed.connect(self.ghost_timer.start)
        self.timer.timeout.connect(self.timer.tick_down)
        pause_btn.pressed.connect(self.timer.pause_timer)
        reset_btn.pressed.connect(self.timer.reset_timer)

        # settings
        settings_btn.pressed.connect(self.open_settings)

        # stack background and animation_timer
        self.scene = QWidget()
        self.scene.setFixedSize(512, 512)
        bg_stack = QStackedLayout(self.scene)
        bg_stack.setStackingMode(QStackedLayout.StackingMode.StackAll)
        bg_stack.addWidget(self.bg_label)
        bg_stack.addWidget(self.timer.label)
        settings_btn.setParent(self.scene)
        settings_btn.show()
        bg_stack.setCurrentWidget(self.timer.label)
        settings_btn.raise_()

        # set horizontal box layout for buttons
        buttons = QWidget()
        buttons_layout = QHBoxLayout(buttons)
        buttons_layout.addWidget(play_btn)
        buttons_layout.addWidget(pause_btn)
        buttons_layout.addWidget(reset_btn)

        # set horizontal box layout for music player
        music_layout = QHBoxLayout(self.music_player)
        music_layout.addWidget(left_arrow)
        music_layout.addWidget(self.music_player.music_label)
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
        app_stack.addWidget(self.music_player)


        self.setCentralWidget(app_layout)

    # get pixel font
    def retrieve_font(self):
        font_path = FONTS_DIR / "pixel_font.ttf"
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        return font_family

    # settings functions
    def open_settings(self):
        self.current_volume = self.music_player.audio_output.volume()
        self.settings_window = Settings(self.timer.focus_mins, self.timer.break_mins, self.current_volume, self.retrieve_font())
        self.settings_window.open()
        self.settings_window.volume_changed.connect(self.live_volume_change)
        self.settings_window.finished.connect(self.apply_settings)

    # get values from settings window and apply them
    def apply_settings(self, result):
        if result == 1:
            new_focus_mins = self.settings_window.focus_spinbox.value()
            new_break_mins = self.settings_window.break_spinbox.value()

            if new_focus_mins == self.timer.focus_mins and new_break_mins == self.timer.break_mins:
                return
            else:
                self.timer.focus_mins = new_focus_mins
                self.timer.break_mins = new_break_mins
                self.timer.reset_timer()
        elif result == 0:
            self.music_player.audio_output.setVolume(self.current_volume)

    # live change of volume from settings window
    def live_volume_change(self):
        self.music_player.audio_output.setVolume(self.settings_window.volume_slider.value() / 100)

    # apply shadow drop effect to widget
    def apply_shadow(self, widget):
        shadow_effect = QGraphicsDropShadowEffect(widget)
        shadow_effect.setColor(QColor(0, 0, 0, 180))
        shadow_effect.setOffset(2, 2)
        shadow_effect.setBlurRadius(6)
        widget.setGraphicsEffect(shadow_effect)

    # ghost appearance functions
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