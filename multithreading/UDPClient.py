'''
Author: Thoma4
Date: 2022-01-03 00:55:14
LastEditTime: 2023-04-30 23:36:14
Description: UDP全双工C/S通信 C
'''
from socket import *
import threading as th
import sharedMethods as sm  # 自定义c/s共用方法


def cSend(sk: socket, dstIP: str, dstPort: int, ct: str):
    while True:
        cMsgSend = input(f'{sm.gt(ct)} [c]: ')
        if not cMsgSend:
            print(f'{sm.gt(ct)} [c]invalid input, client closed.')
            break
        sk.sendto(cMsgSend.encode(), (dstIP, dstPort))
    sk.close()  # 疑似仅关闭socket不结束线程导致报错([WinError 10038])


def cRecv(sk: socket, MAX_SIZE: int, ct: str):
    while True:
        cMsgRecv = sk.recvfrom(MAX_SIZE)
        print(f'{sm.gt(ct)} [s]: {str(cMsgRecv[1])}{cMsgRecv[0].decode()}')


def cMain():
    clientSk = socket(AF_INET, SOCK_DGRAM)  # 创建套接字
    # clientPort = sm.U_cPort
    clientPort = int(input('src Port: '))  # 手动设定c端口 用于多开测试
    clientSk.bind(('', clientPort))  # 绑定IP/端口
    # dst_sIP, dst_sPort = sm.U_sIP, sm.U_sPort  # 声明目的IP/端口
    dst_sIP = input('dst IP: ')
    dst_sPort = int(input('dst Port: '))
    MAX_SIZE = sm.U_MAX_SIZE
    # opt_closeServer = sm.U_OPT_CLS
    c_t = ''  # 客户端时间

    tcSend = th.Thread(target=cSend,
                       args=(clientSk, dst_sIP, dst_sPort, c_t))
    tcRecv = th.Thread(target=cRecv, args=(clientSk, MAX_SIZE, c_t))
    tcSend.start()
    tcRecv.start()


if __name__ == '__main__':
    cMain()

'''
多开客户端/服务端时记得手动确定端口
'''
