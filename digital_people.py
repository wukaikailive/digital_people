from time import sleep
import audio2face
import chat_ollama
import tts_client
import barrage.barrage_server as barrage_server


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

