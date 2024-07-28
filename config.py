"""
数字人项目配置项
"""
# 是否使用分段生成语音的方式
use_audio_split = True
# 是否使用chat_ollama，否则将直接使用ollama
use_chat_ollama = True
# 是否对chat_ollama结果进行过滤，因为chat_ollama如果存在知识库的话，其结果是markdown格式，不方便输出
open_chat_ollama_result_filter = True
# 交流环境，分为直播 live 和一对一 one
communication_env = "live"
communication_env_live = "live"
communication_env_one = "one"
# 是否启用一对一打断流程。如果是在真人一对一交流对话的过程中，如果上一次的响应还没结束，用户再次说话，那么应该停止处理上一次交互。
open_one_immediate_interrupt = False
# 是否启用直播打断流程。如果不启用，则当前数字人会完整走完当次流程，才会恢复响应
open_live_immediate_interrupt = False
# 是否使用文本规范化
use_text_normalization = True

"""
socketio 服务配置
"""
socketio_server = "http://127.0.0.1"
socketio_port = 8082

"""
弹幕配置
"""
# 弹幕服务地址
barrage_server_url = "ws://localhost:9898"
# 监听的弹幕任务，从弹幕服务后端获取
barrage_task_ids = ["1809962513929863168"]
# 弹幕触发的前缀
barrage_trim_start_chr = "#"

"""
直播配置
"""
live_script_file_path = "D:/workspace/DigitalPeople/DigitalPeople/live/book/live-script-book.yaml"

live_background_music_map = {
    "[充满魔法的背景音乐]": "D:/LLM/digtal-people-assets/music/[充满魔法的背景音乐].mp3",
    "[充满魔幻色彩的音乐作背景]": "D:/LLM/digtal-people-assets/music/[充满魔幻色彩的音乐作背景].mp3",
    "[充满未来感的电子音乐作背景]": "D:/LLM/digtal-people-assets/music/[充满未来感的电子音乐作背景].mp3",
    "[启发思考的背景音乐]": "D:/LLM/digtal-people-assets/music/[启发思考的背景音乐].mp3",
    "[轻快的科技感音乐作背景]": "D:/LLM/digtal-people-assets/music/[轻快的科技感音乐作背景].mp3"
}
# 背景乐的音量大小，范围0-1
live_background_music_volume = 0.6


"""
大语言模型配置
"""
# 大语言模型服务地址
chat_server_url = "http://127.0.0.1:11434"
# 使用的大语言模型名称
chat_model_name = "llama3:latest"

"""
chat_ollama配置
"""
# chat_ollama服务地址
chat_ollama_server_url = "http://127.0.0.1:3000"
# 指令id
chat_ollama_instruction_id = 3  # 知心姐姐
# 是否使用指令
chat_ollama_use_instruction = True
# 知识库id
chat_ollama_knowledgebase_id = 1  # 测试
# 是否是否知识库
chat_ollama_use_knowledgebase = False
#
# chat_ollama_family = "llama"
# chat_ollama_family = "chatglm"
chat_ollama_family = "llama"
# chat_ollama_model = "llama:latest"
# chat_ollama_model = "glm4:9b"
chat_ollama_model = "llama3.1:8b"

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
