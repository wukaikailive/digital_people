from live.LiveScriptVisitor import LiveScriptVisitor
from live.jobs.AudioJob import AudioJob


class AudioJobVisitor(LiveScriptVisitor):
    audio_jobs: list[AudioJob] = []

    def __init__(self, data):
        super().__init__(data)

    def visit_audio_job(self, data):
        self.audio_jobs.append(data)