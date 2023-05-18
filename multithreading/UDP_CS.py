'''
Author: Thoma411
Date: 2023-05-03 00:47:08
LastEditTime: 2023-05-07 23:34:41
Description: 
'''
import socket as sk
import threading as th
import sharedMethods as sm

# 定义全局变量
# lock = threading.Lock()  # 创建互斥锁

# 定义发送消息的线程


def send_message():
    while True:
        try:
            # target_ip = input("dst IP: ")
            target_ip = '192.168.137.1'
            target_port = int(input("dst Port: "))
            message = input("msg: ").encode(sm.U_EDCODE)
            sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)  # 创建 UDP socket
            sock.sendto(message, (target_ip, target_port))  # 发送消息
            # print("send msg:", message)
            sock.close()
        except Exception as e:
            print("[sendError]:", e)

# 定义接收消息的线程


def receive_message(src_port):
    # 创建 UDP socket
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    #src_port = int(input("src Port: "))
    sock.bind(('', src_port))  # 绑定本地 IP 和端口号

    while True:
        try:
            data, addr = sock.recvfrom(sm.U_MAX_SIZE)
            dData = data.decode(sm.U_EDCODE)
            MATCH_FLAG = False
            for dkey, dvalue in sm.U_MATCH_LIST.items():
                if dData == dkey:
                    print(dvalue)
                    MATCH_FLAG = True
            if not MATCH_FLAG:
                print("recvfrom %s : %s" % (addr, dData))
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

TODO:db连接：手动实现

AS模块
->
TGS模块
->
把数据发到V由V处理（add加解密）
->
V发回处理后的数据

认证报文
ID字段:IP(+Port)
TS/LT:time时间戳/时间范围

控制报文
'''
