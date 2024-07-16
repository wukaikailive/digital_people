import hashlib
import os
import wave

import tts_client
import logging
logger = logging.getLogger(__name__)

def get_audio_duration(file_path: str) -> float:
    with wave.open(file_path, 'rb') as audio_file:
        num_frames = audio_file.getnframes()
        sample_rate = audio_file.getframerate()
        duration = num_frames / float(sample_rate)
        return duration


def create_audio_cache(value, cache_path):
    h = str_hash(value) + ".wav"
    file_name = cache_path + "/" + h
    if not os.path.isfile(file_name):
        duration = tts_client.call_tts_server(value, cache_path, h)
        logger.debug(f"creating audio finished, duration: {duration}, {value}")
    else:
        logger.debug("audio cache already exists, skip creating audio cache")

def str_hash(value: str) -> str:
    h = int(hashlib.sha1(value.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
    return f"{h}"

if __name__ == "__main__":
    file_path = 'D:/workspace/DigitalPeople/DigitalPeople/output/book/2457135.wav'
    # mp3 和 wav 均可
    duration = get_audio_duration(file_path)
    print(f'duration = {duration}')
