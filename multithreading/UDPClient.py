'''
Author: Thoma4
Date: 2022-01-03 00:55:14
LastEditTime: 2023-04-28 23:35:30
Description: hotspot 192.168.137.1
'''
from socket import *
import threading as th
import sharedMethods as sm  # 自定义c/s共用方法


def cSend(sk, dstIP, dstPort):
    while True:
        cMsgSend = input('[c]send msg: ')
        sk.sendto(cMsgSend.encode(), (dstIP, dstPort))


def cRecv(sk, MAX_SIZE):
    while True:
        cMsgRecv = sk.recvfrom(MAX_SIZE)
        print(f'\n[c]recv msg: {str(cMsgRecv[1])}{cMsgRecv[0].decode()}')


def cMain():
    serverName = '192.168.137.1'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    MAX_SIZE = 2048
    opt_closeServer = 'shutdown'
    c_t = ''  # 客户端时间

    while True:
        CmsgSend = input(f'[c]({sm.gt(c_t)})Input lowercase sentense: ')
        if not CmsgSend:
            break
        clientSocket.sendto(CmsgSend.encode(), (serverName, serverPort))
        CmsgRecv, SAddr = clientSocket.recvfrom(MAX_SIZE)
        CmsgModified = CmsgRecv.decode()
        print(f'[c]({sm.gt(c_t)})msg:', CmsgModified, 'recvfrom:', SAddr)
        if CmsgSend == opt_closeServer:  # 远程关闭服务端
            print(f'[c]({sm.gt(c_t)})Server has been shut down.')
            break
    clientSocket.close()

    # dest_IP, dest_Port = '192.168.137.1', 12000
    # tcSend = th.Thread(target=cSend, args=(clientSocket, dest_IP, dest_Port))
    # tcRecv = th.Thread(target=cRecv, args=(clientSocket, MAX_SIZE))
    # tcSend.start()
    # tcRecv.start()


if __name__ == '__main__':
    cMain()
