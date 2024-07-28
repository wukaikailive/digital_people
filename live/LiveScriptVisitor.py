from live import LiveScriptV1
from live.jobs.AudioJob import AudioJob
from live.jobs.GroupJob import GroupJob
from live.jobs.InteractionJob import InteractionJob
from live.jobs.IntervalJob import IntervalJob
from live.jobs.Job import Job


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
            # 处理弹幕处理逻辑的语音
            if job.on_barrage_received is not None:
                if job.on_barrage_received.action == "play_audio" and job.on_barrage_received.play_audio is not None:
                    self.visit_audio_job(job.on_barrage_received.play_audio)

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
        if data.idle_start_audio is not None:
            self.visit_audio_job(data.idle_start_audio)
        if data.idle_end_audio is not None:
            self.visit_audio_job(data.idle_end_audio)

    def visit_interval_job(self, data: IntervalJob):
        pass
