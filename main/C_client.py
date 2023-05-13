'''
Author: Thoma4
Date: 2022-01-03 00:55:14
LastEditTime: 2023-05-13 09:12:05
Description: hotspot 192.168.137.1
'''
import socket as sk
import time as tm
import messageFormat as mf

AS_IP = '192.168.137.1'
TGS_IP = '192.168.137.1'
AS_PORT = 12000
clientSocket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
MAX_SIZE = 2048
c_t = ''  # 客户端时间

while True:
    c_t = tm.strftime("%H:%M:%S", tm.localtime())
    AS_IP = input(f'[c]({c_t})Input serverIP: ')
    if not AS_IP:
        break
    msg1 = mf.C2AS(1, 1)
    sendmsg1 = msg1.concatmsg()
    clientSocket.sendto(sendmsg1.encode(), (AS_IP, AS_PORT))
    recvmsg1, SAddr = clientSocket.recvfrom(MAX_SIZE)
    msg2 = mf.AS2C.getMsg(recvmsg1.decode())
    msg2.show()
    del msg1, sendmsg1, msg2
clientSocket.close()
