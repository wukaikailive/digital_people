import hashlib
import unittest
from time import sleep

import config
from live.LiveScriptExecutor import LiveScriptExecutor
from live.LiveScriptParser import LiveScriptParser, LiveScriptV1


class TestUtilMethods(unittest.TestCase):

    def test_executor_init(self):
        parser = LiveScriptParser(config.live_script_file_path)
        live_script_v1 = LiveScriptV1(parser.data)
        live_script_executor = LiveScriptExecutor(live_script_v1)

    def test_executor(self):
        parser = LiveScriptParser(config.live_script_file_path)
        live_script_v1 = LiveScriptV1(parser.data)
        live_script_executor = LiveScriptExecutor(live_script_v1)
        live_script_executor.execute()

    def test_interaction_job(self):
        parser = LiveScriptParser("D:/workspace/DigitalPeople/DigitalPeople/live/book/live-script-book-interaction"
                                  "-job.yaml")
        live_script_v1 = LiveScriptV1(parser.data)
        live_script_executor = LiveScriptExecutor(live_script_v1)
        live_script_executor.execute()

    def test_barrage_job(self):
        parser = LiveScriptParser("D:/workspace/DigitalPeople/DigitalPeople/live/book/live-script-book-test-barrage"
                                  ".yaml")
        live_script_v1 = LiveScriptV1(parser.data)
        live_script_executor = LiveScriptExecutor(live_script_v1)
        live_script_executor.execute()

    def test_bg_image_job(self):
        parser = LiveScriptParser("D:/workspace/DigitalPeople/DigitalPeople/live/book/live-script-book-test-bg-image.yaml")
        live_script_v1 = LiveScriptV1(parser.data)
        live_script_executor = LiveScriptExecutor(live_script_v1)
        live_script_executor.execute()


if __name__ == '__main__':
    unittest.main()
