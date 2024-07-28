import argparse
import logging

import config

if __name__ == '__main__':
    """
    参考：https://github.com/rsocket/rsocket-py
    > First Run
    pip3 install rsocket
    pip3 install aiohttp

    python websocket.py -t taskId1 -t taskId2
    """
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--uri', default=config.barrage_server_url, type=str, help="WebSocket Server Uri")
    parser.add_argument('-t', action='append', required=True, help="taskIds")
    args = parser.parse_args()

    uri = args.uri
    subscribe_payload_json["data"]["taskIds"] = args.t
    print(subscribe_payload_json)
    audio2face.init()
    asyncio.run(main(uri))