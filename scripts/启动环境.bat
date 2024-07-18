@echo off
:: 启动audio2face服务
start cmd /C "C:\Users\wukai\AppData\Local\ov\pkg\audio2face-2023.2.0\audio2face_headless.bat"

:: 启动事件中转服务
start cmd /c

:: 启动语音处理服务
call "C:\ProgramData\anaconda3\Scripts\activate.bat" "C:\ProgramData\anaconda3"

call conda activate paddle_speech

call cd D:\LLM\paddlespeech\PaddleSpeech

call paddlespeech_server start --config_file ./paddlespeech/server/conf/application.yaml



exit