from typing import Any

import runtime_status

import logging

logger = logging.getLogger(__name__)


class Job:
    key: str
    name: str
    type: str
    value: str
    caption: str = None
    background_music: str = None
    on_barrage_received = None

    live_script = None

    parent = None
    is_barrage_action_need_execute_flag = False

    def __init__(self, key, data, live_script, parent=None):
        self.key = key
        self.data = data
        self.live_script = live_script
        self.parent = parent
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
        on_barrage_received_data = data.get("on_barrage_received")
        if on_barrage_received_data is not None:
            from live.OnBarrageReceived import OnBarrageReceived
            on_barrage_received = OnBarrageReceived(on_barrage_received_data, self.live_script)
            self.on_barrage_received = on_barrage_received

    def accept(self, visitor: Any):
        pass

    def before_execute(self):
        runtime_status.current_job = self

    def execute(self):
        self.before_execute()
        self.inner_execute()
        self.after_execute()

    def after_execute(self):
        # 检查当前任务是否执行了弹幕检测的逻辑，则应该清除已存的弹幕列表，并且执行
        job = self.get_barrage_action_need_execute_job(0, self)
        if job is not None:
            if self.live_script.has_barrage():
                logger.info("开始播放on_barrage_received设置的预定话术")
                job.on_barrage_received.execute()
                self.live_script.barrage_manager_clear()

    def inner_execute(self):
        self.send_caption()

    def send_caption(self):
        if self.caption is not None and self.live_script is not None:
            self.live_script.send_caption(self.caption)
        if self.background_music is not None and self.live_script is not None:
            self.live_script.play_background_music(self.background_music)

    def get_barrage_action_need_execute_job(self, index, job):
        if job is not None:
            if job.on_barrage_received is not None:
                action = job.on_barrage_received.action
                deep = job.on_barrage_received.deep
                opportunity = job.on_barrage_received.opportunity
                if action == "play_audio" and opportunity == "after_job_executed":
                    if deep == index or deep == -1:
                        return job
            else:
                return self.get_barrage_action_need_execute_job(index + 1, job.parent)
        return None
