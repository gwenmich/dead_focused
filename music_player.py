from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import QLabel, QWidget
from paths import SOUNDS_DIR

class MusicPlayer(QWidget):

    def __init__(self, font_func):
        super().__init__()

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.5)
        self.player.setAudioOutput(self.audio_output)
        self.is_playing = False

        self.tracks = [
        "soundscape.wav",
        "spooky_jazz.wav",
        "spooky_noise.wav"
        ]
        self.current_index = 0
        self.current_song = self.tracks[self.current_index]

        self.font = font_func
        self.music_label = QLabel()
        self.update_label()

        self.set_current_song()



    def update_label(self):
        self.music_label.setText(" ".join((self.current_song.split(".")[0]).split("_")))
        self.music_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.music_label.setStyleSheet(f"""
                    color: #e8e7df;
                    font-family: "{self.font}";
                    font-size: 16px;
                    background: transparent;
                    """)

    def play(self):
        self.player.play()
        self.is_playing = True

    def pause(self):
        if self.player.isPlaying():
            self.player.pause()
            self.is_playing = False

    def stop(self):
        self.player.stop()
        self.is_playing = False

    def play_next(self):
        self.current_index += 1
        if self.current_index > len(self.tracks) - 1:
            self.current_index = 0
        self.set_current_song()

    def play_previous(self):
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.tracks) - 1
        self.set_current_song()

    def set_current_song(self):
        self.current_song = self.tracks[self.current_index]
        self.player.setSource(QUrl.fromLocalFile(str(SOUNDS_DIR / self.current_song)))
        self.player.setLoops(self.player.Loops.Infinite)
        self.update_label()
        if self.is_playing:
            self.play()







