import random
from multiprocessing import Process
from threading import Thread, Timer

import config
import tts_client
from barrage import barrage_server
from live import live_script_util
from live.jobs.Job import Job
from live.jobs.AudioJob import AudioJob

import logging

logger = logging.getLogger(__name__)


class InteractionJob(Job):
    """
    负责处理交互的任务
    """
    # 任务持续时长，单位秒
    duration: int = 1800
    # 空闲时的音频，默认随机播放
    idle_audios: list[AudioJob] = []
    # 空闲时音频播放模式，random、order
    idle_audio_play_mode = "random"
    # 空闲开始时语音
    idle_start_audio: AudioJob = None
    # 空闲结束时语音
    idle_end_audio: AudioJob = None
    # 空闲计时
    idle_timing: int = 120

    __barrage_thread: Process = None
    # __idle_timer: Timer = None
    __idle_audio_thread: Thread = None

    def convert(self, key: str, data: dict):
        super().convert(key, data)
        self.duration = data.get("duration", self.duration)
        self.idle_timing = data.get("idle_timing", self.idle_timing)
        self.idle_audio_play_mode = data.get("idle_audio_play_mode", self.idle_audio_play_mode)
        self.idle_timing = data.get("idle_timing", self.idle_timing)
        idle_audios: dict = data.get("idle_audios")
        self.idle_audios = []
        # 处理 idle_audios
        if idle_audios is not None and len(idle_audios) != 0:
            for key, value in idle_audios.items():
                job = AudioJob(key, value, self.live_script)
                self.idle_audios.append(job)
        idle_start_audio = data.get("idle_start_audio")
        if idle_start_audio is not None:
            self.create_idle_start_audio(idle_start_audio)
        idle_end_audio = data.get("idle_end_audio")
        if idle_end_audio is not None:
            self.create_idle_end_audio(idle_end_audio)

    def execute(self):
        super().execute()

    def inner_execute(self):
        duration = self.duration
        logger.info("开始互动")
        # 启动弹幕服务
        self.on_barrage_listing()
        self.start_timing()
        self.idle_timing_timer()
        self.wait_barrage_finished()
        live_script_util.cancel_idle_timer()
        logger.info("结束互动")

    def on_barrage_listing(self):
        logger.info("启动弹幕服务")
        self.__barrage_thread = Process(target=barrage_server.start)
        self.__barrage_thread.start()
        self.live_script.on_receive_barrage(self.on_receive_barrage)

    @staticmethod
    def on_receive_barrage(msg):
        content = msg['content']
        if content.startswith(config.barrage_trim_start_chr):
            tts_client.start(content.strip(config.barrage_trim_start_chr))

    def off_barrage_listing(self):
        if self.__barrage_thread.is_alive():
            self.__barrage_thread.terminate()

    def start_timing(self):
        logger.info(f"开始互动任务计时，倒计时{self.duration}秒")
        Timer(self.duration, self.timing_finished).start()

    def timing_finished(self):
        logger.info("互动任务计时结束，即将关闭弹幕服务")
        self.off_barrage_listing()

    def idle_timing_timer(self):
        # logger.info(f"开始空闲计时，倒计时{self.idle_timing}秒")
        live_script_util.start_idle_timer(self.idle_timing, self.idle_timing_end)

    def idle_timing_end(self):
        logger.info("空闲计时结束，开始播放预定义话术")
        self.__idle_audio_thread = Thread(target=self.play_idle_audio_thread)
        self.__idle_audio_thread.setDaemon(True)
        self.__idle_audio_thread.start()

    def play_idle_audio_thread(self):
        self.play_idle_start_audio()
        self.play_idle_audio()
        self.idle_timing_timer()

    def play_idle_audio(self):
        if len(self.idle_audios) == 0:
            return
        if self.idle_audio_play_mode == "random":
            # todo 顺序播放未支持
            index = random.randint(0, len(self.idle_audios) - 1)
            audio = self.idle_audios[index]
            audio.inner_execute()

    def wait_barrage_finished(self):
        if self.__barrage_thread.is_alive():
            self.__barrage_thread.join()

    def create_idle_start_audio(self, data):
        self.idle_start_audio = AudioJob("idle_start_audio", data, self.live_script)

    def play_idle_start_audio(self):
        if self.idle_start_audio is not None:
            self.idle_start_audio.inner_execute()

    def create_idle_end_audio(self, data):
        self.idle_end_audio = AudioJob("idle_end_audio", data, self.live_script)

    def play_idle_end_audio(self):
        if self.idle_end_audio is not None:
            self.idle_end_audio.inner_execute()
