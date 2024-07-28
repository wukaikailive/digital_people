import config
from live.LiveScriptV1 import LiveScriptV1
from live.live_script_util import load_live_script
import logging

logger = logging.getLogger(__name__)


class LiveScriptParser:
    def __init__(self, live_script_file_path):
        self.live_script_file_path = live_script_file_path
        self.data = load_live_script(self.live_script_file_path)
        print(self.data)


if __name__ == '__main__':
    parser = LiveScriptParser(config.live_script_file_path)
    live_script_v1 = LiveScriptV1(parser.data)
    print(live_script_v1)
