'''
Author: Thoma4
Date: 2022-01-03 01:09:56
LastEditTime: 2023-04-25 00:32:00
Description: single-thread C
'''
from socket import *
import time as tm

serverName = '192.168.137.1'  # 热点局域网IP
serverPort = 12000
MAX_SIZE = 1024
opt_closeServer = 'shutdown'  # 操作关键词
c_t = ''  # 客户端时间
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))  # 连接server

while True:
    c_t = tm.strftime("%H:%M:%S", tm.localtime())
    CmsgSend = input(f'[c]({c_t})Input lowercase sentence: ')
    if not CmsgSend:  # 输出\n则端开连接
        break
    clientSocket.send(CmsgSend.encode())
    if CmsgSend == opt_closeServer:  # 远程关闭服务端
        c_t = tm.strftime("%H:%M:%S", tm.localtime())
        print(f'[c]({c_t})Server has been shut down.')
        break
    CmsgRecv = clientSocket.recv(MAX_SIZE)
    CmsgModified = CmsgRecv.decode()  # 解码
    c_t = tm.strftime("%H:%M:%S", tm.localtime())
    print(f'[c]({c_t})msg:', CmsgModified, 'recvfrom:', serverName)
clientSocket.close()
