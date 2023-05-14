import json
import socket

# 定义首部格式
header = {
    "head": "int:2",  # 头部，长度为2
    "type": "int:2",  # 大类型标识，长度为2
    "subtype": "int:2",  # 小类型标识，长度为2
    "timestamp": "str:10",  # 时间戳，长度为10
    "length": "int:4",  # 正文长度，长度为4
    "redundancy": "int:4"  # 冗余位，长度为4
}

# 定义第一个报文的类型
message1 = {
    "head": "int:2",  # 头部，长度为2
    "type": "int:2",  # 大类型标识，长度为2
    "subtype": "int:2",  # 小类型标识，长度为2
    "timestamp": "str:10",  # 时间戳，长度为10
    "length": "int:4",  # 正文长度，长度为4
    "redundancy": "int:4",  # 冗余位，长度为4
    "username": "str",
    "password": "str"
}

# 定义第二个报文的类型
message2 = {
    "header": header,
    "name": "str",
    "student_id": "str",
    "chinese_score": "int",
    "math_score": "int",
    "english_score": "int",
}

# 创建TCP/IP套接字并开始监听端口
server_address = ('localhost', 10001)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(1)


while True:
    print("Waiting for a connection...")
    # 等待连接
    connection, client_address = sock.accept()
    try:
        print("Connection from", client_address)
        # 接收数据
        data = connection.recv(1024)
        print("Received:", repr(data))
        # data = b""  # 初始化空的byte字符串
        #
        # # 持续接收数据，直到读取完整个请求
        # while True:
        #     received_data = connection.recv(1024)
        #     if not received_data:
        #         break  # 客户端关闭连接
        #     data += received_data

        # 解析数据
        message = json.loads(data.decode('utf-8'))
        if "username" in message and "password" in message:
            username = message["username"]
            password = message["password"]
            print("Received message 1: username=%s, password=%s" % (username, password))
            # 处理第一个数据报文
        elif "header" in message and "name" in message and "student_id" in message and "chinese_score" in message:
            name = message["name"]
            student_id = message["student_id"]
            chinese_score = message["chinese_score"]
            math_score = message["math_score"] if "math_score" in message else None
            english_score = message["english_score"] if "english_score" in message else None
            print("Received message 2: name=%s, student_id=%s, chinese_score=%d, math_score=%s, english_score=%s"
                  % (name, student_id, chinese_score, math_score, english_score))
            # 处理第二个数据报文
        else:
            print("Unknown message type")

    finally:
        # 关闭连接
        connection.close()