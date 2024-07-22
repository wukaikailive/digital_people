@echo off

chcp 65001

start cmd /C "%~dp0/scripts/启动socketio服务.bat"

start cmd /C "%~dp0/scripts/启动audio2face.bat"

start cmd /C "%~dp0/scripts/启动语音合成服务.bat"


pause