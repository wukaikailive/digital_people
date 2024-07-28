from typing import Any

from live import LiveScriptV1
from live.jobs.Job import Job

import logging

logger = logging.getLogger(__name__)

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
        self.jobs = LiveScriptV1.convert_jobs_util(data, self.live_script, self)

    def accept(self, visitor: Any):
        return visitor.visit(self)

    def execute(self):
        super().execute()

    def inner_execute(self):
        for job in self.jobs:
            job.execute()
