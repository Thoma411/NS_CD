'''
Author: Thoma4
Date: 2022-01-03 00:55:14
LastEditTime: 2023-04-29 00:47:30
Description: UDP全双工C/S通信 C
'''
from socket import *
import threading as th
import sharedMethods as sm  # 自定义c/s共用方法


def cSend(sk, dstIP: str, dstPort: int, ct: str):
    while True:
        cMsgSend = input(f'{sm.gt(ct)} [c]: ')
        sk.sendto(cMsgSend.encode(), (dstIP, dstPort))


def cRecv(sk, MAX_SIZE: int, ct: str):
    while True:
        cMsgRecv = sk.recvfrom(MAX_SIZE)
        print(f'{sm.gt(ct)} [s]: {str(cMsgRecv[1])}{cMsgRecv[0].decode()}')


def cMain():
    clientSocket = socket(AF_INET, SOCK_DGRAM)  # 创建套接字
    clientPort = sm.U_cPort
    clientSocket.bind(('', clientPort))  # 绑定IP/端口
    dest_sIP, dest_sPort = sm.U_sIP, sm.U_sPort  # 声明目的IP/端口
    MAX_SIZE = sm.U_MAX_SIZE
    # opt_closeServer = sm.U_OPT_CLS
    c_t = ''  # 客户端时间

    tcSend = th.Thread(target=cSend,
                       args=(clientSocket, dest_sIP, dest_sPort, c_t))
    tcRecv = th.Thread(target=cRecv, args=(clientSocket, MAX_SIZE, c_t))
    tcSend.start()
    tcRecv.start()


if __name__ == '__main__':
    cMain()
