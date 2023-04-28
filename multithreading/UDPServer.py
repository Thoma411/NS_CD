'''
Author: Thoma4
Date: 2022-01-03 01:01:46
LastEditTime: 2023-04-28 23:35:20
Description: sSend()/sRecv()未启用
'''
# UDPserver
from socket import *
import threading as th
import sharedMethods as sm  # 自定义c/s共用方法


def sSend(sk, dstIP, dstPort):
    while True:
        sMsgSend = input('[s]send msg: ')
        sk.sendto(sMsgSend.encode(), (dstIP, dstPort))


def sRecv(sk, MAX_SIZE):
    while True:
        sMsgRecv = sk.recvfrom(MAX_SIZE)
        print(f'\n[s]recv msg: {str(sMsgRecv[1])}{sMsgRecv[0].decode()}')


def sMain():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_DGRAM)  # 创建套接字
    MAX_SIZE = 2048
    opt_closeServer = 'shutdown'
    s_t = ''  # 服务端时间
    serverSocket.bind(('', serverPort))  # 绑定IP/端口
    print(f'[s]({sm.gt(s_t)})The server is ready to receive...')

    while True:
        SmsgRecv, CAddr = serverSocket.recvfrom(MAX_SIZE)
        SmsgModified = SmsgRecv.decode().upper()
        print(f'[s]({sm.gt(s_t)})msg:', SmsgModified, 'recvfrom:', CAddr)
        serverSocket.sendto(SmsgModified.encode(), CAddr)
        if SmsgModified == opt_closeServer.upper():
            print(
                f'[s]({sm.gt(s_t)})Server has been shut down remotely, operator:', CAddr)
            serverSocket.close()
            break

    # dest_IP, dest_Port = '192.168.137.1', 12000
    # tsSend = th.Thread(target=sSend, args=(serverSocket, dest_IP, dest_Port))
    # tsRecv = th.Thread(target=sRecv, args=(serverSocket, MAX_SIZE))
    # tsSend.start()
    # tsRecv.start()


if __name__ == '__main__':
    sMain()
