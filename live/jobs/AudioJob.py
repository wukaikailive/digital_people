from time import sleep

import audio2face
import config
from live import audio_util
from live.Env import Env
from live.jobs.Job import Job

import logging

logger = logging.getLogger(__name__)


class AudioJob(Job):
    """
    文字转语音并播放的任务
    """
    audio_duration: float = 0
    __env: Env = None

    def execute(self):
        super().execute()

    def inner_execute(self):
        self.__env = self.live_script.env
        h = audio_util.str_hash(self.value) + '.wav'
        cache_path = self.get_audio_cache_path()
        file_path = cache_path + "/" + h
        audio_util.create_audio_cache(self.value, cache_path)
        self.audio_duration = audio_util.get_audio_duration(file_path)
        logger.info(f"正在播放：{self.value}, 时长：{self.audio_duration}")
        audio2face.set_root_path(cache_path)
        audio2face.set_track(h)
        # sleep(0.5)
        audio2face.play()
        sleep(self.audio_duration)
        logger.info(f"播放结束：{self.value}")

    def get_audio_cache_path(self):
        return config.speech_wav_save_path + "/" + self.__env.name
