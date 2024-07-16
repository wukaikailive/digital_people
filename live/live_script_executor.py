import hashlib
import os
import threading
import time

import audio2face
import config
import tts_client
from live import audio_util
from live.live_script_parser import Job, LiveScriptVisitor, AudioJob, LiveScriptV1, Env
import logging
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.DEBUG)

class AudioJobVisitor(LiveScriptVisitor):
    audio_jobs: list[AudioJob] = []
    def __init__(self, data):
        super().__init__(data)

    def visit_audio_job(self, data):
        self.audio_jobs.append(data)


class LiveScriptExecutor:
    """
    直播脚本执行器
    """

    audio_jobs: list[AudioJob] = []

    live_script: LiveScriptV1 = None

    env: Env = None

    cache_path: str = None

    execute_thread: threading.Thread = None

    def __init__(self, live_script):
        self.live_script = live_script
        self.env = self.live_script.env
        self.audio_jobs = self.get_all_audio()
        self.init_audio()
        self.init_audio2face()

    def execute(self):
        while True:
            self.execute_thread = threading.Thread(target=self.execute_inner)
            self.execute_thread.start()
            self.execute_thread.join()
            if not self.live_script.env.loop:
                break

    def execute_inner(self):
        jobs = self.live_script.jobs
        for job in jobs:
            job.execute(self.live_script)

    def init_audio(self):
        self.create_audio_cache_path()
        logger.info("init audio...")
        self.create_audio()

    def init_audio2face(self):
        audio2face.load_usd()
        audio2face.set_root_path(self.cache_path)
        time.sleep(0.5)
        audio2face.activate_stream_live_link()

    def get_all_audio(self):
        visitor = AudioJobVisitor(self.live_script)
        visitor.visit()
        return visitor.audio_jobs

    def create_audio(self):
        logger.info("creating audio...")
        for audio_job in self.audio_jobs:
            value = audio_job.value
            if value is None:
                logger.debug("skip creating audio job, because it's still exists")
                continue
            logger.debug(f"creating audio: {value}")
            audio_util.create_audio_cache(value, self.cache_path)
        logger.info("creating audio done")

    def create_audio_cache_path(self):
        self.cache_path = config.speech_wav_save_path + "/" + self.env.name
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
