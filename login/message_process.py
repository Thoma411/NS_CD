import time
import json
import socket
import struct
from server import *


def send_message(host, port, message):
    message_str = json.dumps(message)

    # 连接到服务器并发送数据
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (host, port)  # 将服务器IP地址和端口号设置为实际情况
        sock.connect(server_address)
        sock.sendall(message_str.encode())
        print("Sent message:", message)
        response = sock.recv(1024)
        print("Received response:", response)
        return response
    except Exception as e:
        print("Error:", e)
    finally:
        sock.close()


def admin_on_login(username, password):  # 管理员登录消息处理
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
    response = send_message(SERVER_HOST, SERVER_PORT, message)
    response1 = response.decode()
    if response1 == "01":
        return 1
    else:
        pass


def stu_on_login(username, password):  # 学生登录消息处理
    # 构造首部
    head_info = {"head": "01", "type": "01", "subtype": "02",
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
    response = send_message(SERVER_HOST, SERVER_PORT, message)
    response1 = response.decode()
    print("学生登录的回复：")
    print(response1)
    if response1 == "01":
        return 1
    else:
        pass


# 学生成绩的消息处理
def query_student_score(student_id):
    # 构建请求消息并发送
    message = {
        "student_id": student_id
    }
    response = send_message(SERVER_HOST, SERVER_PORT, message)
    response1 = response.decode()
    response_dict = json.loads(response1)
    # 接收响应消息并进行解析
    if response_dict.get("error"):
        raise Exception("查询学生成绩失败：{}".format(response_dict["error"]))
    else:
        name = response_dict.get("name")
        gender = response_dict.get("gender")
        age = response_dict.get("age")
        chinese_score = response_dict.get("chinese_score")
        math_score = response_dict.get("math_score")
        english_score = response_dict.get("english_score")
        return {
            "name": name,
            "gender": gender,
            "age": age,
            "chinese_score": chinese_score,
            "math_score": math_score,
            "english_score": english_score
        }
