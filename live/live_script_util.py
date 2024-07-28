import sys
from threading import Timer

import yaml

import runtime_status
import logging

from live.jobs.InteractionJob import InteractionJob
from live.jobs.Job import Job

logger = logging.getLogger(__name__)


def re_start_idle_timer():
    job = runtime_status.current_job
    if job is not None:
        if isinstance(job, InteractionJob):
            logger.info("重新进入空闲计时")
            job.idle_timing_timer()


def start_idle_timer(idle_timing, idle_timing_end):
    logger.info(f"开始空闲计时，倒计时{idle_timing}秒")
    runtime_status.idle_timer = Timer(idle_timing, idle_timing_end)
    runtime_status.idle_timer.start()


def cancel_idle_timer():
    if runtime_status.idle_timer is not None and runtime_status.idle_timer.is_alive():
        logger.info("停止空闲计时")
        runtime_status.idle_timer.cancel()
    # todo 停止播放音频


def load_live_script(live_script_file_path):
    with open(live_script_file_path, 'r', encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.Loader)
    return data


def convert_jobs_util(data: dict, live_script, parent=None):
    jobs: list[Job] = []
    for key, value in data.items():
        job_type: str = value['type']
        if job_type is None:
            raise Exception(f"任务 {key} 中缺失 type 字段")
        name = f"{job_type.capitalize()}Job"
        module = sys.modules["live.jobs." + name]
        class_name = getattr(module, name)
        print(type(class_name))
        clazz = class_name(key, value, live_script, parent)
        # 添加全局
        jobs.append(clazz)
    return jobs
