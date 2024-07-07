# pip install click --upgrade
import librosa
from flask import Flask, request, jsonify
import os
from pydub import AudioSegment
import requests
import time
import json

wav_name = "test.wav"
usd_file_name = "D:/LLM/audio2face/cache/Samples_2023.2/blendshape_solve/claire_solved_arkit.usd"
usd_absolute_path = os.path.abspath(usd_file_name)
a2f_server_url = 'http://127.0.0.1:8011'
a2f_player = "/World/audio2face/Player"
root_path = "D:/workspace/DigitalPeople/DigitalPeople/tts"
wav_file_name = "output.wav"
stream_live_link_node = "/World/audio2face/StreamLivelink"

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

def set_root_path():
    data = {
      "a2f_player": a2f_player,
      "dir_path": root_path
    }
    url = a2f_server_url + '/A2F/Player/SetRootPath'
    requests.post(url, headers=headers, json=data)

def get_current_track():
    data = {
      "a2f_player": a2f_player,
      "dir_path": root_path
    }
    url = a2f_server_url + '/A2F/Player/GetCurrentTrack'
    response = requests.get(url, headers=headers, json=data)
    print(response.content)

def set_track():
    data = {
      "a2f_player": a2f_player,
      "file_name": wav_file_name,
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
    print(data)
    url = a2f_server_url + '/A2F/Exporter/ActivateStreamLivelink'
    response = requests.post(url, headers=headers, json=data)
    print(response.request.body)

def play():
    data = {
      "a2f_player": a2f_player
    }
    url = a2f_server_url + '/A2F/Player/Play'
    requests.post(url, headers=headers, json=data)