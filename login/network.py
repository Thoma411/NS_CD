import json
import struct
import socket


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