'''
Author: Thoma4
Date: 2022-01-03 01:32:33
LastEditTime: 2023-04-28 17:06:11
Description: single-thread S
'''
from socket import *
import threading as th
import sharedMethods as sm  # 自定义c/s共用方法


def sRecv(cSocket, CAddr, MAX_SIZE, s_t='', opt_cs='shutdown'):
    while True:  # 建立连接后一个客户端的流程
        SmsgRecv = cSocket.recv(MAX_SIZE).decode()
        if not SmsgRecv:
            print(f'[s]({sm.gt(s_t)})Client{CAddr} has no input.')
            break
        print(f'[s]({sm.gt(s_t)})msg:', SmsgRecv, 'recvfrom:', CAddr)
        SmsgModified = SmsgRecv.upper()
        cSocket.send(SmsgModified.encode())  # 给client返回大写msg
        if SmsgRecv == opt_cs:  # 服务端关闭
            break
    cSocket.close()


def sMain():
    serverPort = 12000
    MAX_SIZE = 1024
    opt_closeServer = 'shutdown'
    s_t = ''  # 服务端时间
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(3)
    print(f'[s]({sm.gt(s_t)})The server is ready to receive...')

    while True:  # 等待连接
        serverFlag = True  # 服务端状态(True = 开启)
        clientSocket, CAddr = serverSocket.accept()  # 等待连接
        print(f'[s]({sm.gt(s_t)})connected from:', CAddr)

        while True:  # 建立连接后一个客户端的流程
            SmsgRecv = clientSocket.recv(MAX_SIZE).decode()
            if not SmsgRecv:
                print(f'[s]({sm.gt(s_t)})Client{CAddr} has no input.')
                clientSocket.close()
                break
            print(f'[s]({sm.gt(s_t)})msg:', SmsgRecv, 'recvfrom:', CAddr)
            SmsgModified = SmsgRecv.upper()
            clientSocket.send(SmsgModified.encode())  # 给client返回大写msg
            if SmsgRecv == opt_closeServer:  # 服务端关闭
                clientSocket.close()
                serverFlag = False
                break
        if not serverFlag:
            serverSocket.close()
            print(
                f'[s]({sm.gt(s_t)})Server has been shut down remotely, operator:', CAddr)
            break


if __name__ == '__main__':
    sMain()

    # * 客户端双击运行.py文件时直接叉掉窗口会导致服务端报错([WinError 10054])
