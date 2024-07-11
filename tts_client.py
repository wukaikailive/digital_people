import os.path
from time import sleep

from paddlespeech.server.bin.paddlespeech_client import TTSClientExecutor
import audio2face
import chat_ollama
import config
import runtime_status

def call_tts_server(inputs):
    ttsclient_executor = TTSClientExecutor()
    output = os.path.join(config.speech_wav_save_path, config.speech_wav_save_name)
    res = ttsclient_executor(
        input=inputs,
        server_ip=config.speech_server_url,
        port=config.speech_server_port,
        spk_id=0,
        speed=1.0,
        volume=1.0,
        sample_rate=0,
        output=output)

    response_dict = res.json()
    print("call_tts_server", response_dict["message"])
    print("Save synthesized audio successfully on %s." % (response_dict['result']['save_path']))
    print("Audio duration: %f s." % (response_dict['result']['duration']))


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
