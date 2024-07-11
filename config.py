"""
数字人项目配置项
"""

"""
弹幕配置
"""
# 弹幕服务地址
barrage_server_url = "ws://localhost:9898"
# 监听的弹幕任务，从弹幕服务后端获取
barrage_task_ids = ["1809962513929863168"]

"""
大语言模型配置
"""
# 大语言模型服务地址
chat_server_url = "http://127.0.0.1:11434"
# 使用的大语言模型名称
chat_model_name = "llama3:latest"

"""
audio2face配置
"""
# usd文件地址
audio2face_usd_file_name = "D:/LLM/audio2face/cache/Samples_2023.2/blendshape_solve/claire_solved_arkit.usd"
# audio2face headless服务底支
audio2face_a2f_server_url = 'http://127.0.0.1:8011'
# 播放器节点
audio2face_a2f_player = "/World/audio2face/Player"
# # 语音根目录
# audio2face_root_path = "/barrage"
# # 语音文件名称
# audio2face_wav_file_name = "output.wav"
# 流式服务节点
audio2face_stream_live_link_node = "/World/audio2face/StreamLivelink"

"""
语音配置
"""
# 语音服务地址
speech_server_url = "127.0.0.1"
# 语音服务端口
speech_server_port = 8090

speech_wav_save_path = "D:/workspace/DigitalPeople/DigitalPeople/output"
speech_wav_save_name = "output.wav"
