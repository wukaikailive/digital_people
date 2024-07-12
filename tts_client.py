import os.path
from time import sleep

from paddlespeech.server.bin.paddlespeech_client import TTSClientExecutor
import audio2face
import chat_ollama
import config
import runtime_status


def call_tts_server(inputs, path=config.speech_wav_save_path, file_name=config.speech_wav_save_name):
    """
    调用语音合成服务，生成语音
    :param inputs:
    :return: 语音时间
    """
    ttsclient_executor = TTSClientExecutor()
    output = f"{path}/{file_name}"
    # print(output)
    res = ttsclient_executor(
        input=inputs,
        server_ip=config.speech_server_url,
        port=config.speech_server_port,
        spk_id=0,
        speed=1.0,
        volume=3.0,
        sample_rate=0,
        output=output)

    response_dict = res.json()
    # print(response_dict['result'])
    print("call_tts_server", response_dict["message"])
    print("Save synthesized audio successfully on %s." % (response_dict['result']['save_path']))
    print("Audio duration: %f s." % (response_dict['result']['duration']))
    return response_dict['result']['duration']


def init_audio2face():
    audio2face.load_usd()
    audio2face.set_root_path()
    sleep(1)
    audio2face.activate_stream_live_link()


def start(inputs):
    runtime_status.isAnswerCreating = True
    gpt_output = chat_ollama.call_ollama(inputs)
    runtime_status.isAnswerCreating = False
    runtime_status.isAudioCreating = True
    call_tts_server(gpt_output)
    runtime_status.isAudioCreating = False
    audio2face.set_track()
    sleep(1)
    runtime_status.isAudioPlaying = True
    audio2face.play()
