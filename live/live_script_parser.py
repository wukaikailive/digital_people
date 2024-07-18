import logging
import random
from threading import Timer, Thread
from time import sleep
from typing import Any
from multiprocessing import Process

import yaml

import audio2face
import barrage.barrage_server
import config
import live.live_script_parser
import live.audio_util as audio_util
from barrage import barrage_server
from util.StoppableThread import StoppableThread

logger = logging.getLogger(__name__)


def load_live_script(live_script_file_path):
    data = yaml.load(open(live_script_file_path, 'r', encoding="utf-8"), Loader=yaml.Loader)
    return data


class LiveScriptParser:
    def __init__(self, live_script_file_path):
        self.live_script_file_path = live_script_file_path
        self.data = load_live_script(self.live_script_file_path)
        print(self.data)


class Env:
    """
    环境设置
    """
    # 是否循环
    loop: False
    # 循环次数，开启loop时有效，值为 0 代表无限循环
    loop_times: 0
    # 是否启用日志
    log: True
    # 名称
    name: str

    @staticmethod
    def convert(data: dict):
        env = Env()
        env.loop = dict["loop"] if "loop" in data else False
        env.loop_times = data["loop_times"] if "loop_times" in data else 0
        env.log = data["log"] if "log" in data else False
        env.name = data["name"] if "name" in data else None
        if env.name is None:
            raise Exception("env name is None")
        return env


class Job:
    key: str
    name: str
    type: str
    value: str
    caption: str = None
    background_music: str = None

    live_script = None

    def __init__(self, key, data):
        self.data = data
        self.convert(key, data)

    def convert(self, key: str, data: dict):
        self.key = key
        name = data.get("name")
        if name is not None:
            self.name = name
        else:
            raise Exception(f"任务 {key} 中缺失字段 name")
        _type = data.get("type")
        if _type is not None:
            self.type = _type
        else:
            raise Exception(f"任务 {key} 中缺失字段 type")
        self.value = data.get("value")
        self.caption = data.get("caption")
        self.background_music = data.get("background_music")

    def accept(self, visitor: Any):
        pass

    def execute(self, live_script):
        pass


class GroupJob(Job):
    """
    组任务，包含一系列子任务
    """
    jobs: list[Job] = []

    def convert(self, key: str, data: dict):
        super().convert(key, data)
        data = data['jobs']
        if data is None:
            raise Exception("jobs 字段不存在")
        self.jobs = LiveScriptV1.convert_jobs_util(data)

    def accept(self, visitor: Any):
        return visitor.visit(self)

    def execute(self, live_script):
        #  todo 播放背景音乐
        for job in self.jobs:
            job.execute(live_script)

    def get_audio_audio_name(self, value):
        return audio_util.str_hash(value) + ".wav"


class AudioJob(Job):
    """
    文字转语音并播放的任务
    """
    audio_duration: float = 0
    __env: Env = None

    def execute(self, live_script):
        self.live_script = live_script
        self.__env = live_script.env
        h = audio_util.str_hash(self.value) + '.wav'
        cache_path = self.get_audio_cache_path()
        file_path = cache_path + "/" + h
        audio_util.create_audio_cache(self.value, cache_path)
        self.audio_duration = audio_util.get_audio_duration(file_path)
        logger.info(f"正在播放：{self.value}, 时长：{self.audio_duration}")
        audio2face.set_track(h)
        sleep(0.5)
        audio2face.play()
        sleep(self.audio_duration)
        logger.info(f"播放结束：{self.value}")

    def get_audio_cache_path(self):
        return config.speech_wav_save_path + "/" + self.__env.name


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
    idle_start_audio: AudioJob
    # 空闲结束时语音
    idle_end_audio: AudioJob
    # 空闲计时
    idle_timing: int = 120

    __barrage_thread: Process = None
    __idle_timer: Timer = None
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
                job = AudioJob(key, value)
                self.idle_audios.append(job)
        idle_start_audio = data.get("idle_start_audio")
        if idle_start_audio is not None:
            self.create_idle_start_audio(idle_start_audio)
        idle_end_audio = data.get("idle_end_audio")
        if idle_end_audio is not None:
            self.create_idle_end_audio(idle_end_audio)

    def execute(self, live_script):
        self.live_script = live_script
        duration = self.duration
        logger.info("开始互动")
        # 启动弹幕服务
        self.on_barrage_listing()
        self.start_timing()
        self.idle_timing_timer()
        self.wait_barrage_finished()
        logger.info("结束互动")
        self.on_destroy()
        
    def on_destroy(self):
        if self.__idle_timer.is_alive():
            self.__idle_timer.cancel()
        # todo 停止播放音频

    def on_barrage_listing(self):
        logger.info("启动弹幕服务")
        self.__barrage_thread = Process(target=barrage_server.start)
        self.__barrage_thread.start()

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
        logger.info(f"开始空闲计时，倒计时{self.idle_timing}秒")
        self.__idle_timer = Timer(self.idle_timing, self.idle_timing_end)
        self.__idle_timer.start()

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
            audio.execute(self.live_script)

    def wait_barrage_finished(self):
        if self.__barrage_thread.is_alive():
            self.__barrage_thread.join()

    def create_idle_start_audio(self, data):
        self.idle_start_audio = AudioJob("idle_start_audio", data)

    def play_idle_start_audio(self):
        if self.idle_start_audio is not None:
            self.idle_start_audio.execute(self.live_script)

    def create_idle_end_audio(self, data):
        self.idle_end_audio = AudioJob("idle_end_audio", data)

    def play_idle_end_audio(self):
        if self.idle_end_audio is not None:
            self.idle_end_audio.execute(self.live_script)


class IntervalJob(Job):
    """
    负责提供等待计时的任务
    """
    # 等待时间 单位s
    value: int = 0

    def convert(self, key: str, data: dict):
        super().convert(key, data)
        self.value = data.get("value", self.value)


class LiveScriptV1:
    version: int
    env: Env
    jobs: list[Job]

    def __init__(self, data: dict):
        self.data = data
        self.version = 1
        self.convert()

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

    @staticmethod
    def convert_jobs_util(data: dict):
        jobs: list[Job] = []
        for key, value in data.items():
            job_type: str = value['type']
            if job_type is None:
                raise Exception(f"任务 {key} 中缺失 type 字段")
            module = getattr(live, "live_script_parser")
            name = f"{job_type.capitalize()}Job"
            class_name = getattr(module, name)
            print(type(class_name))
            clazz = class_name(key, value)
            jobs.append(clazz)
        return jobs

    def convert_jobs(self):
        data = self.data['jobs']
        if data is None:
            raise Exception("jobs 字段不存在")
        self.jobs = LiveScriptV1.convert_jobs_util(data)


class LiveScriptVisitor:
    def __init__(self, live_script):
        self.live_script: LiveScriptV1 = live_script

    def visit(self):
        self.visit_version(self.live_script.version)
        self.visit_env(self.live_script.env)
        self.visit_jobs(self.live_script.jobs)

    def __visit_children_jobs(self, data):
        for job in data:
            name = f"visit_{job.type}_job"
            class_name = getattr(self, name)
            class_name(job)

    def visit_version(self, data):
        pass

    def visit_env(self, data):
        pass

    def visit_jobs(self, data: list[Job]):
        self.__visit_children_jobs(data)

    def visit_audio_job(self, data: AudioJob):
        pass

    def visit_group_job(self, data: GroupJob):
        self.__visit_children_jobs(data.jobs)

    def visit_interaction_job(self, data: InteractionJob):
        self.__visit_children_jobs(data.idle_audios)
        self.visit_audio_job(data.idle_start_audio)
        self.visit_audio_job(data.idle_end_audio)
        pass

    def visit_interval_job(self, data: IntervalJob):
        pass


if __name__ == '__main__':
    parser = LiveScriptParser(config.live_script_file_path)
    live_script_v1 = LiveScriptV1(parser.data)
    print(live_script_v1)
