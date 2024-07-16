import logging
from time import sleep
from typing import Any

import yaml

import audio2face
import config
import live.live_script_parser
import live.audio_util as audio_util

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
    # 空闲时音频播放模型，random、order
    idle_audio_play_mode = "random"
    # 空闲计时
    idle_timing: int = 120

    def convert(self, key: str, data: dict):
        super().convert(key, data)
        self.duration = data.get("duration", self.duration)
        self.idle_timing = data.get("idle_timing", self.idle_timing)
        self.idle_audio_play_mode = data.get("idle_audio_play_mode", self.idle_audio_play_mode)
        self.idle_timing = data.get("idle_timing", self.idle_timing)
        # todo idle_audios

    def execute(self, live_script):
        duration = self.duration
        logger.info("开始互动")
        # todo 启动弹幕服务
        logger.info("结束互动")

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
        pass

    def visit_interval_job(self, data: IntervalJob):
        pass


if __name__ == '__main__':
    parser = LiveScriptParser(config.live_script_file_path)
    live_script_v1 = LiveScriptV1(parser.data)
    print(live_script_v1)
