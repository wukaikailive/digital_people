from threading import Timer

import runtime_status
from live.live_script_parser import InteractionJob
import logging

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
