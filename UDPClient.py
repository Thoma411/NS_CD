'''
Author: Thoma4
Date: 2022-01-03 00:55:14
LastEditTime: 2023-04-25 00:26:52
Description: 
'''
from socket import *
import time as tm

serverName = '192.168.137.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
MAX_SIZE = 2048
opt_closeServer = 'shutdown'
c_t = ''  # 客户端时间

while True:
    c_t = tm.strftime("%H:%M:%S", tm.localtime())
    CmsgSend = input(f'[c]({c_t})Input lowercase sentense: ')
    if not CmsgSend:
        break
    clientSocket.sendto(CmsgSend.encode(), (serverName, serverPort))
    CmsgRecv, SAddr = clientSocket.recvfrom(MAX_SIZE)
    CmsgModified = CmsgRecv.decode()
    c_t = tm.strftime("%H:%M:%S", tm.localtime())
    print(f'[c]({c_t})msg:', CmsgModified, 'recvfrom:', SAddr)
    if CmsgSend == opt_closeServer:  # 远程关闭服务端
        c_t = tm.strftime("%H:%M:%S", tm.localtime())
        print(f'[c]({c_t})Server has been shut down.')
        break
clientSocket.close()
# z 172.27.5.45
# s 172.27.77.203
# c 172.27.3.204
# hotpoint 192.168.137.1
