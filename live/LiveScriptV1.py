import sys

import config
from live import live_script_util
from live.BackgroundMusicManager import BackgroundMusicManager
from live.BarrageManager import BarrageManager
from live.CaptionManager import CaptionManager
from live.Env import Env
from live.SocketioClient import SocketioClient
from live.jobs.Job import Job
from live.live_script_util import convert_jobs_util


class LiveScriptV1:
    version: int
    env: Env
    jobs: list[Job]

    __caption_manager: CaptionManager

    __background_music_manager: BackgroundMusicManager

    __socketio_client: SocketioClient

    __barrage_manager: BarrageManager

    def __init__(self, data: dict):
        self.data = data
        self.version = 1
        self.convert()
        # 检测是否开启弹幕监听
        if self.env.enable_barrage_monitoring:
            self.__barrage_manager = BarrageManager(config.socketio_server, config.socketio_port)
            self.__barrage_manager.connect()
        self.__caption_manager = CaptionManager(config.socketio_server, config.socketio_port)
        self.__caption_manager.connect()
        self.__socketio_client = SocketioClient(config.socketio_server, config.socketio_port)
        self.__socketio_client.connect()
        self.__socketio_client.on("cancel_idle_timer", live_script_util.cancel_idle_timer)
        self.__socketio_client.on("re_start_idle_timer", live_script_util.re_start_idle_timer)
        self.__background_music_manager = (
            BackgroundMusicManager(config.live_background_music_map, volume=config.live_background_music_volume))

    def on_receive_barrage(self, callback):
        self.__socketio_client.on("receive_user_barrage", callback)

    def off_receive_barrage(self):
        # self.__socketio_client
        pass

    def barrage_manager_clear(self):
        self.__barrage_manager.clear()

    def has_barrage(self):
        return self.__barrage_manager.has_barrage()

    def play_background_music(self, music):
        self.__background_music_manager.play_music(music)

    def send_caption(self, msg):
        self.__caption_manager.send(msg)

    def convert(self):
        self.convert_version()
        self.convert_env()
        self.convert_jobs()

    def convert_version(self):
        self.version = self.data['version']
        if self.version is None or self.version != 1:
            raise Exception("version 字段不存在或不为1")

    def convert_env(self):
        data = self.data['env']
        if data is None:
            self.env = Env()
        self.env = Env.convert(data)

    def convert_jobs(self):
        data = self.data['jobs']
        if data is None:
            raise Exception("jobs 字段不存在")
        self.jobs = convert_jobs_util(data, self)
