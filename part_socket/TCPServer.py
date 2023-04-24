'''
Author: Thoma4
Date: 2022-01-03 01:32:33
LastEditTime: 2023-04-25 00:31:33
Description: single-thread S
'''
from socket import *
import time as tm

serverPort = 12000
MAX_SIZE = 1024
opt_closeServer = 'shutdown'
s_t = ''  # 服务端时间
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(3)
print('[s]The server is ready to receive...')

while True:  # 等待连接
    serverFlag = True  # 服务端状态(True = 开启)
    clientSocket, CAddr = serverSocket.accept()  # 等待连接
    s_t = tm.strftime("%H:%M:%S", tm.localtime())
    print(f'[s]({s_t})connected from:', CAddr)
    while True:  # 建立连接后一个客户端的流程
        SmsgRecv = clientSocket.recv(MAX_SIZE).decode()
        if not SmsgRecv:
            s_t = tm.strftime("%H:%M:%S", tm.localtime())
            print(f'[s]({s_t})Client{CAddr} has no input.')
            clientSocket.close()
            break
        s_t = tm.strftime("%H:%M:%S", tm.localtime())
        print(f'[s]({s_t})msg:', SmsgRecv, 'recvfrom:', CAddr)
        SmsgModified = SmsgRecv.upper()
        clientSocket.send(SmsgModified.encode())  # 给client返回大写msg
        if SmsgRecv == opt_closeServer:  # 服务端关闭
            clientSocket.close()
            serverFlag = False
            break
    if not serverFlag:
        serverSocket.close()
        s_t = tm.strftime("%H:%M:%S", tm.localtime())
        print(f'[s]({s_t})Server has been shut down remotely, operator:', CAddr)
        break

# * 客户端双击运行.py文件时直接叉掉窗口会导致服务端报错([WinError 10054])
