import os

import pygame


class BackgroundMusicManager:
    music_map: dict = {}
    volume: float = 0.5

    def __init__(self, music_map=None, *args, **kwargs):
        if music_map is None:
            music_map = {}
        self.music_map = music_map
        self.volume = kwargs.get('volume', 0.5)
        pygame.mixer.init()

    def play_music(self, music):
        self.stop()
        self.play(music)

    def play(self, music):
        """
         播放音频，支持简称和路径全称
        :param music:
        :return:
        """
        music_path = self.music_map.get(music)
        if music_path is None:
            music_path = music
        if os.path.isfile(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(self.volume)

    def fadeout(self):
        pygame.mixer.music.fadeout(time=1)

    def stop(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)
