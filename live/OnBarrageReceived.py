from live.jobs.AudioJob import AudioJob


class OnBarrageReceived:
    action: str
    opportunity: str
    # 解析的任务深度，如果为-1，则所有任务都可能响应此动作，如果为0，代表当前任务（不解析任何子任务），设置为正整数，那么会解析第n层的子任务（如果存在），例如这里设置为1，意为在每本图书执行完毕时，检查是否有弹幕然后执行相应操作
    deep: int = 0
    play_audio: AudioJob

    live_script = None

    def __init__(self, data, live_script):
        self.live_script = live_script
        self.convert(data)

    def convert(self, data, ):
        action = data.get("action")
        if action is not None:
            self.action = action
        else:
            raise Exception(f"设置 OnBarrageReceive 中缺失字段 action")
        if action == "play_audio":
            play_audio = data.get("play_audio")
            if play_audio is None:
                raise Exception(f"设置 OnBarrageReceive 中, 当action为play_audio时，必须填写play_audio字段")
            self.play_audio = AudioJob("play_audio", play_audio, self.live_script)
        opportunity = data.get("opportunity")
        if opportunity is not None:
            self.opportunity = opportunity
        else:
            raise Exception(f"设置 OnBarrageReceive 中缺失字段 opportunity")
        deep = data.get("deep")
        if deep is not None:
            self.deep = deep
        else:
            self.deep = 0

    def execute(self):
        self.play_audio.inner_execute()
