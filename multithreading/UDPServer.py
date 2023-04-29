'''
Author: Thoma4
Date: 2022-01-03 01:01:46
LastEditTime: 2023-04-29 13:49:57
Description: UDP全双工C/S通信 S
'''
from socket import *
import threading as th
import sharedMethods as sm  # 自定义c/s共用方法


def sSend(sk: socket, dstIP: str, dstPort: int, st: str):
    while True:
        sMsgSend = input(f'{sm.gt(st)} [s]: ')
        sk.sendto(sMsgSend.encode(), (dstIP, dstPort))


def sRecv(sk: socket, MAX_SIZE: int, st: str):
    while True:
        sMsgRecv = sk.recvfrom(MAX_SIZE)
        print(f'{sm.gt(st)} [c]: {str(sMsgRecv[1])}{sMsgRecv[0].decode()}')


def sMain():
    serverSocket = socket(AF_INET, SOCK_DGRAM)  # 创建套接字
    # serverPort = sm.U_sPort
    src_Port = int(input('src Port: '))
    serverSocket.bind(('', src_Port))  # 绑定IP/端口
    # dst_IP, dst_Port = sm.U_cIP, sm.U_cPort  # 声明目的IP/端口
    # serverIP = '192.168.137.1'
    dst_IP = input('dst IP: ')  # *S-S通信 手动输入地址
    dst_Port = int(input('dst Port: '))
    MAX_SIZE = sm.U_MAX_SIZE
    # opt_closeServer = sm.U_OPT_CLS
    s_t = ''  # 服务端时间
    print(f'[s]({sm.gt(s_t)})Server started.')

    tsSend = th.Thread(target=sSend,
                       args=(serverSocket, dst_IP, dst_Port, s_t))
    tsRecv = th.Thread(target=sRecv, args=(serverSocket, MAX_SIZE, s_t))
    tsSend.start()
    tsRecv.start()


if __name__ == '__main__':
    sMain()

'''
收发消息存在显示(换行)问题, 不过并不重要
现已支持服务端-服务端通信
'''
