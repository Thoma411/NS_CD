'''
Author: Thoma4
Date: 2022-01-03 01:01:46
LastEditTime: 2023-05-11 17:01:20
Description: 
'''
# AS server
import socket as sk
import time as tm
import cryptMethod.messageFormat as mf

AS_PORT = 12000
serverSocket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
MAX_SIZE = 2048
LifeTime2 = '6000'  # 有效期
opt_closeServer = 'shutdown'
s_t = ''  # 服务端时间
serverSocket.bind(('', AS_PORT))
s_t = tm.strftime("%H:%M:%S", tm.localtime())
print(f'[s]({s_t})The server is ready to receive...')

while True:
    recvmsg1, CAddr = serverSocket.recvfrom(MAX_SIZE)  # 收
    msg1 = mf.C2AS.getMsg(recvmsg1.decode())
    msg1.show()
    amsg1 = mf.AS2C(msg1.ID_TGS, 6000)
    sendmsg1=amsg1.concatmsg()
    serverSocket.sendto(sendmsg1.encode(), CAddr)  # 发
