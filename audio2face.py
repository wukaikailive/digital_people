# pip install click --upgrade
import librosa
from flask import Flask, request, jsonify
import os
from pydub import AudioSegment
import requests
import time
import json
import config

usd_file_name = config.audio2face_usd_file_name
usd_absolute_path = os.path.abspath(usd_file_name)
a2f_server_url = config.audio2face_a2f_server_url
a2f_player = config.audio2face_a2f_player
root_path = config.speech_wav_save_path
wav_file_name = config.speech_wav_save_name
stream_live_link_node = config.audio2face_stream_live_link_node

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}


# 获取wav时长
def get_duration(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)  # sr=None 保持原始采样率
        duration = librosa.get_duration(y=y, sr=sr)
        return duration
    except Exception as e:
        print(f"Error with librosa: {e}")
        return None


def get_status():
    pass;


def load_usd():
    data = {
        "file_name": usd_absolute_path
    }
    url = a2f_server_url + '/A2F/USD/Load'
    response = requests.post(url, headers=headers, json=data)
    print(response.content)


def set_root_path(path=root_path):
    data = {
        "a2f_player": a2f_player,
        "dir_path": path
    }
    url = a2f_server_url + '/A2F/Player/SetRootPath'
    response = requests.post(url, headers=headers, json=data)
    print("set_root_path: ", response.content)


def get_current_track(path=root_path):
    data = {
        "a2f_player": a2f_player,
        "dir_path": path
    }
    url = a2f_server_url + '/A2F/Player/GetCurrentTrack'
    response = requests.get(url, headers=headers, json=data)
    print("get_current_track: ", response.content)


def set_track(file_name=wav_file_name):
    data = {
        "a2f_player": a2f_player,
        "file_name": file_name,
        "time_range": [
            0,
            -1
        ]
    }
    url = a2f_server_url + '/A2F/Player/SetTrack'
    requests.post(url, headers=headers, json=data)


def activate_stream_live_link():
    data = {
        "node_path": stream_live_link_node,
        "value": True
    }
    url = a2f_server_url + '/A2F/Exporter/ActivateStreamLivelink'
    response = requests.post(url, headers=headers, json=data)
    print("activate_stream_live_link: ", response.content)


def play():
    data = {
        "a2f_player": a2f_player
    }
    url = a2f_server_url + '/A2F/Player/Play'
    requests.post(url, headers=headers, json=data)


def pause():
    data = {
        "a2f_player": a2f_player
    }
    url = a2f_server_url + '/A2F/Player/Pause'
    requests.post(url, headers=headers, json=data)


def init():
    load_usd()
    set_root_path()
    time.sleep(0.5)
    activate_stream_live_link()
