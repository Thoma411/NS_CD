'''
Author: Thoma411
Date: 2022-01-03 01:09:56
LastEditTime: 2023-04-28 17:46:05
Description: multithreading C
'''
from socket import *
import sharedMethods as sm  # 自定义c/s共用方法


def cMain():
    serverName = '192.168.137.1'  # 热点局域网IP
    serverPort = 12000
    MAX_SIZE = 1024
    c_t = ''  # 客户端时间
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))  # 连接server

    while True:
        CmsgSend = input(f'[c]({sm.gt(c_t)})Input lowercase sentence: ')
        if not CmsgSend:  # 输出\n则端开连接
            print(f'[c]({sm.gt(c_t)})disconnected.')
            break
        clientSocket.send(CmsgSend.encode())
        CmsgRecv = clientSocket.recv(MAX_SIZE)
        CmsgModified = CmsgRecv.decode()  # 解码
        print(f'[c]({sm.gt(c_t)})msg:', CmsgModified, 'recvfrom:', serverName)
    clientSocket.close()


if __name__ == '__main__':
    cMain()
