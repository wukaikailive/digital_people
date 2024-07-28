import time

from live.jobs.Job import Job
import logging

logger = logging.getLogger(__name__)


class IntervalJob(Job):
    """
    负责提供等待计时的任务
    """
    # 等待时间 单位s
    value: int = 0

    def convert(self, key: str, data: dict):
        super().convert(key, data)
        self.value = data.get("value", self.value)

    def execute(self):
        super().execute()

    def inner_execute(self):
        duration = self.value
        logger.info(f"开始等待，{duration}秒")
        time.sleep(duration)
        logger.info("结束等待")
