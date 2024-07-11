from paddlespeech.server.bin.paddlespeech_client import ASROnlineClientExecutor

asrclient_executor = ASROnlineClientExecutor()
res = asrclient_executor(
    input="./zh.wav",
    server_ip="127.0.0.1",
    port=8090,
    sample_rate=16000,
    lang="zh_cn",
    audio_format="wav")
print(res)