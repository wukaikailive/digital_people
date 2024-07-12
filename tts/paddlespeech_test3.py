from time import sleep

from paddlespeech.server.bin.paddlespeech_client import TTSClientExecutor
import audio2face
from chatollama import chat_ollama


def call_tts_server(inputs):
    ttsclient_executor = TTSClientExecutor()
    res = ttsclient_executor(
        input=inputs,
        server_ip="127.0.0.1",
        port=8090,
        spk_id=0,
        speed=1.0,
        volume=1.0,
        sample_rate=0,
        output="./output.wav")

    response_dict = res.json()
    print(response_dict["message"])
    print("Save synthesized audio successfully on %s." % (response_dict['result']['save_path']))
    print("Audio duration: %f s." % (response_dict['result']['duration']))

def init_audio2face():
    audio2face.load_usd()
    audio2face.set_root_path()
    sleep(1)
    audio2face.activate_stream_live_link()

if __name__ == '__main__':
    init_audio2face()
    while True:
        inputs = input("请输入内容：")
        gpt_output = chat_ollama.call_ollama(inputs)
        call_tts_server(gpt_output)
        audio2face.set_track()
        audio2face.play()
        sleep(1)
