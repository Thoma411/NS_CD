'''
Author: Thoma411
Date: 2023-05-13 20:22:53
LastEditTime: 2023-05-14 23:15:09
Description: 
'''
import socket as sk
import threading as th
from MsgFieldDef import *

SERVER_HOST = '192.168.137.1'
AS_PORT = 8010
MAX_SIZE = 2048


def handle_C2AS(mt, caddr):  # 处理C2AS报文 mt:str
    Rdm_c2as = str2dict(mt)  # 正文str->dict
    id_c, id_tgs = Rdm_c2as['ID_C'], Rdm_c2as['ID_TGS']
    c_ip = mf.IP2AD(caddr[0])
    k_ctgs = mf.msg_rndKey()  # 生成共享密钥
    Sdm_tktT = initTKT(k_ctgs, id_c, id_tgs, c_ip)  # 初始化tkt_tgs
    Sdm_as2c = initM_AS2C_REP(k_ctgs, id_tgs, Sdm_tktT)  # 生成正文as2c同时加密tkt
    # print(Sdm_as2c['mTKT_T'], len(Sdm_as2c['mTKT_T']))
    Sdh_as2c = initHEAD(EX_CTL, INC_AS2C, len(Sdm_as2c))  # 生成首部
    Ssm_as2c = dict2str(Sdm_as2c)  # dict->str
    Ssh_as2c = dict2str(Sdh_as2c)
    Sbm_as2c = cyDES.DES_encry(Ssm_as2c, DKEY_C)  # 加密正文
    Shm_as2c = cyDES.binascii.hexlify(Sbm_as2c)  # 转16进制
    # print(Shm_as2c, len(Shm_as2c))
    Ssa_as2c = Ssh_as2c + '|' + str(Shm_as2c)  # 拼接str
    return Ssa_as2c  # str+bytes


msg_handles = {  # 消息处理函数字典
    (EX_CTL, INC_C2AS): handle_C2AS
}


def AS_Recv(C_Socket: sk, cAddr):
    while True:
        Rba_msg = C_Socket.recv(MAX_SIZE)  # 收

        # *初步分割
        if not Rba_msg:  # 判空
            print('msg is empty!')
            break
        Rsa_msg = Rba_msg.decode()  # bytes->str
        Rsh_msg, Rsm_msg = Rsa_msg.split('|')  # 分割为首部+正文
        Rdh_msg = str2dict(Rsh_msg)  # 首部转字典(正文在函数中转字典)

        # *匹配报文类型
        if Rdh_msg['LIGAL'] == H_LIGAL:  # 收包合法
            msg_extp = Rdh_msg['EXTYPE']
            msg_intp = Rdh_msg['INTYPE']
            if msg_extp == EX_DAT:
                print('This is a dataMsg.')
            elif msg_extp == EX_CTL:
                # 在消息处理函数字典中匹配
                handler = msg_handles.get((msg_extp, msg_intp))
                if handler:
                    Ssa_msg = handler(Rsm_msg, cAddr)  # 相应函数处理
                    C_Socket.send(Ssa_msg.encode())  # 编码发送
                else:  # 找不到处理函数
                    print('no match func for msg.')
        else:  # 收包非法
            print('illegal package!')
            break

        # print(Rsh_msg, Rsm_msg, cAddr)
        # *发送
        # C_Socket.send(Rsa_msg.encode())
    C_Socket.close()


def AS_Main():
    sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    sock.bind(('', AS_PORT))
    sock.listen(5)
    print('AS_Tserver started...')
    while True:
        cSocket, cAddr = sock.accept()
        print('conn:', cAddr)
        thr = th.Thread(target=AS_Recv, args=(cSocket, cAddr))
        thr.start()
    sock.close()


if __name__ == '__main__':
    AS_Main()
