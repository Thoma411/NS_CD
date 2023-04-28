'''
Author: Thoma411
Date: 2022-01-03 01:32:33
LastEditTime: 2023-04-28 17:47:19
Description: multithreading S
'''
from socket import *
import threading as th
import sharedMethods as sm  # 自定义c/s共用方法


def sRecv(cSocket, CAddr, MAX_SIZE, s_t=''):
    while True:  # 建立连接后一个客户端的流程
        SmsgRecv = cSocket.recv(MAX_SIZE).decode()
        if not SmsgRecv:
            print(f'[s]({sm.gt(s_t)})Client{CAddr} has no input.')
            break
        print(f'[s]({sm.gt(s_t)})msg:', SmsgRecv, 'recvfrom:', CAddr)
        SmsgModified = SmsgRecv.upper()
        cSocket.send(SmsgModified.encode())  # 给client返回大写msg
    cSocket.close()


def sMain():
    serverPort = 12000
    MAX_SIZE = 1024
    s_t = ''  # 服务端时间
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(3)
    print(f'[s]({sm.gt(s_t)})The server is ready to receive...')

    while True:  # 等待连接
        clientSocket, CAddr = serverSocket.accept()  # 等待连接
        print(f'[s]({sm.gt(s_t)})connected from:', CAddr)

        thr = th.Thread(target=sRecv, args=(
            clientSocket, CAddr, MAX_SIZE))
        thr.start()  # *启用多线程


if __name__ == '__main__':
    sMain()

    '''
    客户端双击运行.py文件时直接叉掉窗口会导致服务端报错([WinError 10054])
    引入多线程后叉掉窗口服务端会报错, 但主线程仍然运行

    TODO:可能会用到 端口复用/线程守护
    '''
