'''
Author: Thoma411
Date: 2023-05-13 20:22:53
LastEditTime: 2023-05-25 13:01:20
Description: 
'''
import socket as sk
import threading as th
from MsgFieldDef import *

AS_PORT = 8010
MAX_SIZE = 2048
MAX_LISTEN = 16

PRT_LOG = True  # 是否打印输出
PKEY_AS, SKEY_AS = myRSA.RSA_initKey('a', DEF_LEN_RSA_K)  # *生成AS的公私钥


def handle_C2AS_CTF(m_text, m_sig, cAddr):  # 处理C2AS_CTF报文
    # *获取认证报文并认证
    Rdm_c2as_ctf = str2dict(m_text)  # 正文str->dict
    pk_c = Rdm_c2as_ctf['PK_C']  # 获取PK_C
    verFlag = myRSA.RSA_verf(m_text, m_sig, pk_c)
    print(verFlag)
    # *生成认证回复报文(K_c)
    if verFlag:
        k_c = msg_rndKey(initType='i')  # 生成纯数字密钥
        cpK_c = myRSA.RSA_encry(int(k_c), pk_c)  # RSA加密K_c
        Sdm_as2c_ctf = initM_AS2C_KC(cpK_c)  # 生成K_c报文
        Sdh_as2c_ctf = initHEAD(EX_CTL, INC_AS2C_KC, len(Sdm_as2c_ctf))
        Ssm_as2c_ctf = dict2str(Sdm_as2c_ctf)  # 正文dict->str
        Ssh_as2c_ctf = dict2str(Sdh_as2c_ctf)  # 首部dict->str
        Ssa_as2c_ctf = Ssh_as2c_ctf + '|' + Ssm_as2c_ctf
        if PRT_LOG:
            print('k_c', k_c)
            print('Ssa_as2c_ctf:\n', Ssa_as2c_ctf)
        return Ssa_as2c_ctf, k_c
    # *生成认证回复报文(ctf)
    # Sdm_as2c_ctf = initM_AS2C_CTF(DID_AS, PKEY_AS)
    # Sdh_as2c_ctf = initHEAD(EX_CTL, INC_AS2C_CTF, len(Sdm_as2c_ctf))
    # return pk_c


def handle_C2AS(mt, k_c, caddr):  # 处理C2AS报文 mt:str
    Rdm_c2as = str2dict(mt)  # 正文str->dict
    id_c, id_tgs = Rdm_c2as['ID_C'], Rdm_c2as['ID_TGS']
    c_ip = IP2AD(caddr[0])  # IP字符串->6位str
    k_ctgs = msg_rndKey()  # *生成共享密钥(str类型)
    Sdm_tktT = initTKT(k_ctgs, id_c, id_tgs, c_ip, PRT_LOG)  # 初始化tkt_tgs
    Sdm_as2c = initM_AS2C_REP(k_ctgs, id_tgs, Sdm_tktT)  # 生成正文as2c同时加密tkt
    Sdh_as2c = initHEAD(EX_CTL, INC_AS2C, len(Sdm_as2c))  # 生成首部
    Ssm_as2c = dict2str(Sdm_as2c)  # dict->str
    Ssh_as2c = dict2str(Sdh_as2c)
    Sbm_as2c = myDES.DES_encry(Ssm_as2c, k_c)  # *加密正文(Sbm_as2c已是str)
    Ssa_as2c = Ssh_as2c + '|' + str(Sbm_as2c)  # 拼接str
    if PRT_LOG:
        print('AS->C:\n', Ssa_as2c)
    return Ssa_as2c  # str+str


def AS_Recv(C_Socket: sk, cAddr):
    K_C, AS_PKEY_C = None, None
    while True:
        Rba_msg = C_Socket.recv(MAX_SIZE)  # 收

        # *初步分割
        if not Rba_msg:  # 判空
            break
        Rsa_msg = Rba_msg.decode()  # bytes->str
        if PRT_LOG:
            print('C->AS:\n', Rsa_msg)

        if Rsa_msg.count('|') == 1:  # 按分隔符数量划分
            Rsh_msg, Rsm_msg = Rsa_msg.split('|')  # 分割为首部+正文
        elif Rsa_msg.count('|') == 2:
            Rsh_msg, Rsm_msg, Rsc_msg = Rsa_msg.split('|')  # 分割为首部+正文+Rsc

        Rdh_msg = str2dict(Rsh_msg)  # 首部转字典(正文在函数中转字典)

        # *匹配报文类型
        if Rdh_msg['LIGAL'] == H_LIGAL:  # 收包合法
            msg_extp = Rdh_msg['EXTYPE']
            msg_intp = Rdh_msg['INTYPE']

            # *数据报文
            if msg_extp == EX_DAT:
                print('This is a dataMsg.')

            # *控制报文
            elif msg_extp == EX_CTL:
                if msg_intp == INC_C2AS_CTF:
                    Ssa_msg, K_C = handle_C2AS_CTF(
                        Rsm_msg, Rsc_msg, cAddr)  # *处理CTF报文
                    C_Socket.send(Ssa_msg.encode())
                elif msg_intp == INC_C2AS:
                    Ssa_msg = handle_C2AS(Rsm_msg, K_C, cAddr)  # 处理C2AS正文
                    C_Socket.send(Ssa_msg.encode())  # 编码发送
                else:  # 找不到处理函数
                    print('no match func for msg.')
        else:  # 收包非法
            print('illegal package!')
            break
    C_Socket.close()


def AS_Main():
    ASsock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    ASsock.bind(('', AS_PORT))
    ASsock.listen(MAX_LISTEN)
    print('AS_Tserver started...')
    while True:
        cSocket, cAddr = ASsock.accept()
        print('conn:', cAddr)
        thr = th.Thread(target=AS_Recv, args=(cSocket, cAddr))
        thr.start()
    ASsock.close()


if __name__ == '__main__':
    AS_Main()
