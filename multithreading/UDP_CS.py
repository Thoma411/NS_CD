'''
Author: Thoma411
Date: 2023-05-03 00:47:08
LastEditTime: 2023-05-03 01:26:41
Description: 
'''
import socket as sk
import threading as th

# 定义全局变量
# lock = threading.Lock()  # 创建互斥锁

# 定义发送消息的线程


def send_message():
    while True:
        try:
            # target_ip = input("请输入目标 IP 地址: ")
            target_ip = '192.168.137.1'
            target_port = int(input("dst Port: "))
            message = input("msg: ").encode('utf-8')

            # 创建 UDP socket
            sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

            # 发送消息
            sock.sendto(message, (target_ip, target_port))
            # print("已向目标地址发送消息:", message)

            # 关闭 socket
            sock.close()
        except Exception as e:
            print("[sendError]:", e)

# 定义接收消息的线程


def receive_message(src_port):
    # 创建 UDP socket
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    #src_port = int(input("请输入本地端口号: "))
    sock.bind(('', src_port))  # 绑定本地 IP 和端口号

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print("recvfrom %s : %s" % (addr, data.decode('utf-8')))
        except Exception as e:
            print("[recvError]:", e)
        # finally:
        #     lock.release()  # 释放锁


# 启动接收消息的线程
src_Port = int(input("src Port: "))
th.Thread(target=receive_message, args=(src_Port,)).start()
# 启动发送消息的线程
th.Thread(target=send_message).start()

'''
每次发送消息前手动指定目标IP&端口，比较麻烦
但是至少能跑
TODO:如何正常结束进程
'''
