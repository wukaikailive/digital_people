class Env:
    """
    环境设置
    """
    # 是否循环
    loop: False
    # 循环次数，开启loop时有效，值为 0 代表无限循环
    loop_times: 0
    # 是否启用日志
    log: True
    # 名称
    name: str

    # 开启弹幕监听，开启此功能，后续才可以使用on_barrage_received字段
    enable_barrage_monitoring: bool = False

    @staticmethod
    def convert(data: dict):
        env = Env()
        env.loop = dict["loop"] if "loop" in data else False
        env.loop_times = data["loop_times"] if "loop_times" in data else 0
        env.log = data["log"] if "log" in data else False
        env.name = data["name"] if "name" in data else None
        if env.name is None:
            raise Exception("env name is None")
        env.enable_barrage_monitoring = data["enable_barrage_monitoring"] if "enable_barrage_monitoring" in data else False
        return env
