'''
Author: Thoma4
Date: 2022-01-03 01:01:46
LastEditTime: 2023-04-25 00:25:55
Description: 
'''
# UDPserver
from socket import *
import time as tm

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
MAX_SIZE = 2048
opt_closeServer = 'shutdown'
s_t = ''  # 服务端时间
serverSocket.bind(('', serverPort))
s_t = tm.strftime("%H:%M:%S", tm.localtime())
print(f'[s]({s_t})The server is ready to receive...')

while True:
    SmsgRecv, CAddr = serverSocket.recvfrom(MAX_SIZE)
    SmsgModified = SmsgRecv.decode().upper()
    s_t = tm.strftime("%H:%M:%S", tm.localtime())
    print(f'[s]({s_t})msg:', SmsgModified, 'recvfrom:', CAddr)
    serverSocket.sendto(SmsgModified.encode(), CAddr)
    if SmsgModified == opt_closeServer.upper():
        s_t = tm.strftime("%H:%M:%S", tm.localtime())
        print(f'[s]({s_t})Server has been shut down remotely, operator:', CAddr)
        serverSocket.close()
        break
