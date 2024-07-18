import threading
from time import sleep

from paddlespeech.server.bin.paddlespeech_client import TTSClientExecutor, TextClientExecutor
import audio2face
import digital_people
from chatollama import chat_ollama
import config
import runtime_status


def call_text_server(inputs):
    text_client_executor = TextClientExecutor()
    res = text_client_executor(
        input=inputs,
        server_ip=config.speech_server_url,
        port=config.speech_server_port,
    )
    print("规范化后文本为：" + res)
    return res


def call_tts_server(inputs, path=config.speech_wav_save_path, file_name=config.speech_wav_save_name):
    """
    调用语音合成服务，生成语音
    :param inputs:
    :param path:
    :param file_name:
    :return: 语音时间
    """
    ttsclient_executor = TTSClientExecutor()
    output = f"{path}/{file_name}"
    # print(output)
    res = ttsclient_executor(
        input=inputs,
        server_ip=config.speech_server_url,
        port=config.speech_server_port,
        spk_id=174,
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
    if ((config.communication_env == config.communication_env_live and config.open_live_immediate_interrupt)
            or runtime_status.isIdle):
        threading.Thread(target=start_thread, args=(inputs,)).start()
    else:
        print("跳过响应：" + inputs)


def start_thread(inputs):
    # 如果是直播模式，且开启了打断，那么直接正常响应，或者数字人空闲
    runtime_status.isIdle = False
    # runtime_status.isAnswerCreating = True
    try:
        gpt_output = chat_ollama.call_ollama(inputs)
    except Exception as e:
        runtime_status.isIdle = True
        print(e)
        return
        # runtime_status.isAnswerCreating = False
    # runtime_status.isAudioCreating = True
    if config.use_text_normalization:
        gpt_output = call_text_server(gpt_output)
    if config.use_audio_split:
        audio2face.init()
        dispatcher = digital_people.AudioEnginePlayDispatcher(gpt_output)
        dispatcher.start()
    else:
        call_tts_server(gpt_output)
        # runtime_status.isAudioCreating = False
        audio2face.set_track()
        sleep(1)
        # runtime_status.isAudioPlaying = True
        audio2face.play()
        # TODO 设置空闲状态
