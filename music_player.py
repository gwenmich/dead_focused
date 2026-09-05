from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, Qt, QTimer
from PySide6.QtWidgets import QLabel, QWidget

from ghost import Ghost
from paths import SOUNDS_DIR

class MusicPlayer(QWidget):

    def __init__(self, font_func, shadow_func):
        super().__init__()

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.5)
        self.player.setAudioOutput(self.audio_output)
        self.is_playing = False

        self.tracks = [
            "haunted_night.mp3",
            "ghost_jazz_club.mp3",
            "ghosts_in_the_wind.mp3",
            "creepy_nightmare.mp3",
            "deathly_silence"
        ]
        self.current_index = 0
        self.current_song = self.tracks[self.current_index]

        self.font = font_func
        self.music_label = QLabel()
        self.label_shadow = shadow_func
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
        self.label_shadow(self.music_label)

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
        if self.current_song == "silence":
            self.player.stop()
            self.music_label.setText("silence")
        else:
            self.player.setSource(QUrl.fromLocalFile(str(SOUNDS_DIR / self.current_song)))
            self.player.setLoops(self.player.Loops.Infinite)
            self.update_label()
            if self.is_playing:
                self.play()

    # lower background volume when sound effect at end of timer plays
    def duck_audio_volume(self, audio):
        self.original_volume = self.audio_output.volume()
        self.fade_to(0.1)
        audio.playingChanged.connect(lambda: self.restore_music_volume(audio))
        audio.play()

    def restore_music_volume(self, audio):
        if not audio.isPlaying():
            self.fade_to(self.original_volume)

    def fade_to(self, target_volume):
        self.fade_target = target_volume
        self.fade_step = 0.02 if target_volume > self.audio_output.volume() else -0.02
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self.fade_step_tick)
        self.fade_timer.start(30)

    def fade_step_tick(self):
        current = self.audio_output.volume()
        new_volume = current + self.fade_step
        if self.fade_step > 0 and new_volume >= self.fade_target:
            self.fade_timer.stop()
            self.audio_output.setVolume(self.fade_target)
        elif self.fade_step < 0 and new_volume <= self.fade_target:
            self.fade_timer.stop()
            self.audio_output.setVolume(self.fade_target)
        else:
            self.audio_output.setVolume(new_volume)






