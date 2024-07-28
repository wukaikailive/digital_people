import os.path
import threading
from datetime import datetime
from time import sleep
import audio2face
import runtime_status
from chatollama import chat_ollama
import config
import tts_client
import barrage.barrage_server as barrage_server
import tts.recursively_split_by_character as recursively_split_by_character
import pydash
from threading import Timer
import traceback

from live import live_script_util
from live.SocketioClient import SocketioClient


class PlayingPOJO(object):
    text: str = None
    index: int = None
    audio_ready: bool = False
    playing: bool = False
    finished: bool = False
    duration: float = 0

    def __init__(self, text: str, index: int, playing: bool, finished: bool, duration: float):
        self.text = text
        self.index = index
        self.playing = playing
        self.finished = finished
        self.duration = duration


class AudioEnginePlayDispatcher:
    texts = []
    status = []
    # pool: Pool = None
    id: str
    socketio_client: SocketioClient = None

    def __init__(self, text, socketio_client = None):
        self.status = []
        self.text = text
        self.socketio_client = socketio_client
        self.texts = recursively_split_by_character.split_text(text)
        # self.pool = Pool(len(self.texts) + 1)
        self.id = self.general_id()
        self.root_path = f"{config.speech_wav_save_path}/{self.id}"
        self.create_root_path()

    def create_root_path(self):
        if not (os.path.exists(self.root_path)):
            os.mkdir(self.root_path)

    def start(self):
        threads = []
        try:
            # 开启语音合成任务
            for index, text in enumerate(self.texts):
                self.status.append(PlayingPOJO(text, index, False, False, 0))
            (thread := threading.Thread(target=self.tts_threads)).start()
            threads.append(thread)
            # 轮询播放语音
            (thread := threading.Thread(target=self.play)).start()
            threads.append(thread)
            # 等待所有异步任务完成
            for thread in threads:
                thread.join()
        except Exception as e:
            print("遇到错误")
            traceback.print_exc()
            # exit()
        finally:
            runtime_status.isAudioPlaying = False
            runtime_status.isSpeaking = False
            runtime_status.isIdle = True
            self.re_start_idle_timer()
            print("处理完成")

    def re_start_idle_timer(self):
        if self.socketio_client is None:
            live_script_util.re_start_idle_timer()
        else:
            self.socketio_client.send_data("re_start_idle_timer", {})

    def tts_threads(self):
        for index, text in enumerate(self.texts):
            self.call_tts_server(text, index)
            print(f"{index}-语音生成完成-{text}")

    def call_tts_server(self, text, index):
        duration = tts_client.call_tts_server(text, self.root_path, self.get_file_name(index))
        self.status[index].duration = duration
        self.status[index].audio_ready = True

    def general_id(self):
        now = datetime.now()  # 获得当前时间
        id = now.strftime("%Y_%m_%d_%H_%M_%S")
        return id

    def exec_audio2face(self, index):
        audio2face.pause()
        audio2face.set_root_path(self.root_path)
        file_name = self.get_file_name(index)
        audio2face.set_track(file_name)
        # sleep(1)
        audio2face.play()

    def play(self):
        playing_stat = None
        size = len(self.texts)
        while True:
            index = None
            finished_stat = self.get_finished()
            # 如果没有已完成的语音，说明整个语音列表都还没开始播放，此时播放第一条
            if finished_stat is None or size == 1:
                index = 0
            else:
                index = finished_stat.index + 1
            # 越界，则退出循环
            if self.is_last(index - 1):
                break
            # 如果是最后一条语音，且已完成，则退出循环
            if self.is_last(index):
                stat = self.status[index]
                if stat.finished:
                    break
            # 获取正在播放的语音
            local_playing_stat = self.get_playing()
            # 如果刚好有正在播放的语音，则跳过
            if local_playing_stat is not None:
                continue
            else:
                # 否则开始播放
                playing_stat = self.status[index]
                if (not playing_stat.audio_ready) or playing_stat.finished or playing_stat.playing:
                    continue
                playing_stat.playing = True
                # 调用audio2face推送到UE播放
                self.exec_audio2face(index)
                # 设置定时器，定时器结束后设置当前语音为播放完成
                print(f"{index}-正在播放-{playing_stat.text}")
                Timer(playing_stat.duration, self.set_finished, (index,)).start()
            # 定期检查一次
            sleep(0.1)

    def set_finished(self, index):
        stat = self.status[index]
        stat.finished = True
        stat.playing = False
        print(f"{index}-播放结束-{stat.text}")

    def get_playing(self):
        return pydash.find_last(self.status, lambda x: x.playing)

    def get_finished(self):
        return pydash.find_last(self.status, lambda x: x.finished)

    def has_playing(self):
        stat = self.get_playing()
        return stat is not None

    def get_next(self, current_index):
        index = current_index
        index += 1
        if not self.is_last(index):
            return self.status[index]
        return None

    @staticmethod
    def is_first(index):
        return index == 0

    def is_last(self, index):
        return index == len(self.texts) - 1

    @staticmethod
    def get_file_name(index):
        return f"{index}.wav"


def start(inputs):
    """
    开始数字人流程
    :param inputs: 问题文本
    :return: 无
    """
    gpt_output = chat_ollama.call_ollama(inputs)
    tts_client.call_tts_server(gpt_output)
    audio2face.set_track()
    sleep(1)
    audio2face.play()


if __name__ == '__main__':
    audio2face.init()
    barrage_server.start()
