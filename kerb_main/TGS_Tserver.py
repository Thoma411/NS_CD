'''
Author: Thoma411
Date: 2023-05-13 20:22:53
LastEditTime: 2023-05-21 16:20:32
Description: 
'''
import socket as sk
import threading as th
from MsgFieldDef import *

SERVER_HOST = '192.168.137.1'
TGS_PORT = 8020
MAX_SIZE = 2048
MAX_LISTEN = 16

PRT_LOG = False  # 是否打印输出


def handle_C2TGS(mt, caddr):  # 处理C2TGS报文 mt:str
    Rdm_c2tgs = str2dict(mt)  # 正文str->dict
    # print(Rdm_c2tgs)
    id_v, tkt_tgs, atc_c = Rdm_c2tgs['ID_V'], Rdm_c2tgs['mTKT_T'], Rdm_c2tgs['mATC_C']

    c_ip = IP2AD(caddr[0])  # IP字符串->6位str

    # *解密Ticket_TGS, 获得K_C_TGS
    Rsm_tktT = cbDES.DES_decry(tkt_tgs, DKEY_TGS)  # *解密为str
    Rdm_tktT = str2dict(Rsm_tktT)  # str->dict
    if PRT_LOG:
        print('Ticket_TGS:\n', Rdm_tktT)
    k_ctgs = Rdm_tktT['K_SHARE']  # 取得k_ctgs共享密钥

    # *解密Authenticator_C, 获得ID_C
    Rsm_ATCC = cbDES.DES_decry(atc_c, k_ctgs)  # 解密为str
    Rdm_ATCC = str2dict(Rsm_ATCC)  # str->dict
    if PRT_LOG:
        print('Rdm_ATCC:\n', Rdm_ATCC)
    id_c = Rdm_ATCC['ID_C']

    # *生成Ticket_V 正文 首部
    k_cv = msg_rndKey()  # *生成共享密钥(str类型)
    Sdm_tktV = initTKT(k_cv, id_c, id_v, c_ip, PRT_LOG)  # 初始化tkt_v
    Sdm_tgs2c = initM_TGS2C_REP(k_cv, id_v, Sdm_tktV)  # 生成正文tgs2c同时加密tkt
    Sdh_tgs2c = initHEAD(EX_CTL, INC_TGS2C, len(Sdm_tgs2c))  # 生成首部
    Ssm_tgs2c = dict2str(Sdm_tgs2c)  # dict->str
    Ssh_tgs2c = dict2str(Sdh_tgs2c)
    Sbm_tgs2c = cbDES.DES_encry(Ssm_tgs2c, k_ctgs)  # *加密正文
    Ssa_tgs2c = Ssh_tgs2c + '|' + str(Sbm_tgs2c)  # 拼接str
    if PRT_LOG:
        print('TGS->C:\n', Ssa_tgs2c)
    return Ssa_tgs2c  # str+str


msg_handles = {  # 消息处理函数字典
    (EX_CTL, INC_C2TGS): handle_C2TGS
}


def TGS_Recv(C_Socket: sk, cAddr):
    while True:
        Rba_msg = C_Socket.recv(MAX_SIZE)  # 收

        # *初步分割
        if not Rba_msg:  # 判空
            # print('msg is empty!')
            break
        Rsa_msg = Rba_msg.decode()  # bytes->str
        if PRT_LOG:
            print('C->TGS:\n', Rsa_msg)
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


def TGS_Main():
    TGSsock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    TGSsock.bind(('', TGS_PORT))
    TGSsock.listen(MAX_LISTEN)
    print('TGS_Tserver started...')
    while True:
        cSocket, cAddr = TGSsock.accept()
        print('conn:', cAddr)
        thr = th.Thread(target=TGS_Recv, args=(cSocket, cAddr))
        thr.start()
    TGSsock.close()


if __name__ == '__main__':
    TGS_Main()
