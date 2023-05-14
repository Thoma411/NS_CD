import time
import loginui
import json
import struct
from loginui import LoginUI
from network import send_message


def on_login(username, password):
    # 构造首部
    head_info = {"head": "01", "type": "01", "subtype": "01",
                 "timestamp": int(time.time())}  # 生成当前时间戳

    # 计算正文长度并填充冗余位
    content = {"username": username, "password": password}
    content_str = json.dumps(content)
    content_len = len(content_str.encode('utf-8'))
    redundant = struct.pack('>4s', b'\x00\x00\x00\x00')

    # 组装message1
    message = head_info
    message["content_len"] = content_len
    message["redundant"] = list(redundant)
    message.update(content)
    # 发送消息
    response = send_message('localhost', 10001, message)


if __name__ == '__main__':
    login_ui = LoginUI(on_login)
    login_ui.run()
