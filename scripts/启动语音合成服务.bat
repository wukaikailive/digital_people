@echo off
:: 启动语音处理服务
call "C:\ProgramData\anaconda3\Scripts\activate.bat" "C:\ProgramData\anaconda3"

call conda activate paddle_speech

call cd D:\LLM\paddlespeech\PaddleSpeech

call paddlespeech_server start --config_file ./paddlespeech/server/conf/application.yaml

exit