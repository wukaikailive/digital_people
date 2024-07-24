"""
运行时状态
"""
import multiprocessing
import threading

# 是否正在说话
isSpeaking = False

# 是否正在生成语音
isAudioCreating = False

# 是否正在播放语音
isAudioPlaying = False

# 是否正在生成回答
isAnswerCreating = False

#是否空闲
isIdle = True

# 互动计时器
idle_timer = None

# 当前执行的任务
current_job = None

