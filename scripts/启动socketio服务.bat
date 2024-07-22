:: 启动语音处理服务
call "C:\ProgramData\anaconda3\Scripts\activate.bat" "C:\ProgramData\anaconda3"

call conda activate paddle_speech

call echo %~dp0

call python %~dp0\..\live\socketio_server.py

pause