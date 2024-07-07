from paddlespeech.cli.asr.infer import ASRExecutor
asr = ASRExecutor()
result = asr(audio_file="douyin.mp3")  # 录音文件地址
print(result)