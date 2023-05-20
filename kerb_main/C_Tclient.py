'''
Author: Thoma411
Date: 2023-05-13 20:18:23
LastEditTime: 2023-05-20 08:43:38
Description:
'''
import socket as sk
from MsgFieldDef import *

ID_C = 13  # !每个C的ID需不同
C_IP = '192.168.137.60'  # !IP需提前声明

AS_IP, AS_PORT = '192.168.137.1', 8010
TGS_IP, TGS_PORT = '192.168.137.51', 8020
V_IP, V_PORT = '192.168.137.60', 8030
MAX_SIZE = 2048


def Chandle_AS2C(mt):  # 处理AS2C控制报文
    Rsm_as2c = cbDES.DES_decry(mt, DKEY_C)  # *bytes直接解密为str
    Rdm_as2c = str2dict(Rsm_as2c)  # str->dict
    k_ctgs = Rdm_as2c['K_C_TGS']  # 获取共享密钥k_ctgs
    Ticket_TGS = Rdm_as2c['mTKT_T']  # 获取Ticket_TGS
    return k_ctgs, Ticket_TGS


def Chandle_TGS2C(mt, k_ctgs):  # 处理TGS2C控制报文
    Rsm_tgs2c = cbDES.DES_decry(mt, k_ctgs)  # *bytes直接解密为str
    Rdm_tgs2c = str2dict(Rsm_tgs2c)  # str->dict
    # print(Rdm_tgs2c)
    k_cv = Rdm_tgs2c['K_C_V']  # 获取共享密钥k_cv
    Ticket_V = Rdm_tgs2c['mTKT_V']  # 获取Ticket_V
    return k_cv, Ticket_V


def Chandle_V2C(mt, k_cv):  # 处理V2C控制报文
    Rsm_v2c = cbDES.DES_decry(mt, k_cv)  # *bytes直接解密为str
    Rdm_v2c = str2dict(Rsm_v2c)  # str->dicts
    ts_5 = Rdm_v2c['TS_5']  # 获取ts_5
    return ts_5


Dmsg_handles = {  # 数据报文处理函数字典
    # TODO:预留存放数据报文处理函数
}


def C_Recv(Dst_socket: sk, k_share=None):  # C的接收方法
    '''报文在此分割为首部+正文, 正文在函数字典对应的方法处理'''
    Rba_msg = Dst_socket.recv(MAX_SIZE)  # 收

    # *初步分割
    Rsa_msg = Rba_msg.decode()  # bytes->str
    Rsh_msg, Rsm_msg = Rsa_msg.split('|')  # 分割为首部+正文
    Rdh_msg = str2dict(Rsh_msg)  # 首部转字典(正文在函数中转字典)

    # *匹配报文类型
    TMP_KEY, TMP_TKT, TMP_TS = None, None, None  # 临时变量, 将返回值传出if-else
    retFlag: int = 0  # 根据该值决定返回值

    if Rdh_msg['LIGAL'] == H_LIGAL:  # *收包合法
        msg_extp = Rdh_msg['EXTYPE']
        msg_intp = Rdh_msg['INTYPE']

        # *控制报文
        if msg_extp == EX_CTL:
            if msg_intp == INC_AS2C_CTF:
                # TODO:处理CTF报文
                pass
            elif msg_intp == INC_AS2C:
                k_ctgs, tkt_tgs = Chandle_AS2C(Rsm_msg)  # 处理AS2C正文
                TMP_KEY = k_ctgs  # 将k_ctgs,tkt_tgs传出if-else
                TMP_TKT = tkt_tgs
                retFlag = 2
            elif msg_intp == INC_TGS2C:
                k_cv, tkt_v = Chandle_TGS2C(Rsm_msg, k_share)  # 处理TGS2C正文
                TMP_KEY = k_cv  # 将k_cv,tkt_v传出if-else
                TMP_TKT = tkt_v
                retFlag = 4
            elif msg_intp == INC_V2C:
                ts_5 = Chandle_V2C(Rsm_msg, k_share)  # 处理V2C正文
                TMP_TS = ts_5  # 将ts_5传出if-else
                retFlag = 6
            else:
                print('no match func for control msg.')
        # *数据报文
        elif msg_extp == EX_DAT:
            Dhandler = Dmsg_handles.get((msg_extp, msg_intp))
            if Dhandler:
                pass  # TODO:合并后数据报文处理方法
            else:
                print('no match func for data msg.')
                pass
    else:  # 收包非法
        print('illegal package!')

    # *根据retFlag决定返回值
    if retFlag == 2:  # 返回step2的共享密钥/票据
        return TMP_KEY, TMP_TKT
    elif retFlag == 4:  # 返回step4的共享密钥/票据
        return TMP_KEY, TMP_TKT
    elif retFlag == 6:  # 返回step6 V生成的时间戳
        return TMP_TS
    else:
        pass


# def create_C2AS_CTF():  # 生成C2AS_CTF报文
    '''
    变量说明:
    S/R - 发送/接收
    d/s/b/h - 字典/字符串/比特/16进制比特
    h/m/c/a - 首部/正文/签名/拼接整体
    '''
#     Sdm_c2as_ctf = initM_C2AS_CTF(ID_C, PKEY_C)  # 生成正文
#     Sdc_c2as_ctf = initSIGN(SKEY_C, ID_C, PKEY_C)  # 生成签名
#     Sdh_c2as_ctf = initHEAD(EX_CTL, INC_C2AS_CTF,
#                             len(Sdm_c2as_ctf + Sdc_c2as_ctf))  # 生成首部
#     Ssm_c2as_ctf = dict2str(Sdm_c2as_ctf)  # 正文dict->str
#     Ssc_c2as_ctf = dict2str(Sdc_c2as_ctf)  # 签名dict->str
#     Ssh_c2as_ctf = dict2str(Sdh_c2as_ctf)  # 首部dict->str
#     Ssa_c2as_ctf = Ssh_c2as_ctf + '|' + Ssm_c2as_ctf + '|'+Ssc_c2as_ctf  # 拼接
#     Sba_c2as_ctf = Ssa_c2as_ctf.encode()  # str->bytes
#     return Sba_c2as_ctf


def create_C2AS():  # 生成C2AS报文
    Sdm_c2as = initM_C2AS_REQ(ID_C, DID_TGS)  # 生成正文
    Sdh_c2as = initHEAD(EX_CTL, INC_C2AS, len(Sdm_c2as))  # 生成首部
    Ssm_c2as = dict2str(Sdm_c2as)  # 正文dict->str
    Ssh_c2as = dict2str(Sdh_c2as)  # 首部dict->str
    Ssa_c2as = Ssh_c2as + '|' + Ssm_c2as  # 拼接
    Sba_c2as = Ssa_c2as.encode()  # str->bytes
    return Sba_c2as


def create_C2TGS(c_ip, tkt_tgs, k_ctgs):  # 生成C2TGS报文
    Sdm_ATCC = initATC(ID_C, c_ip)  # 生成Authenticator_C
    Sdm_c2tgs = initM_C2TGS_REQ(
        DID_V, tkt_tgs, Sdm_ATCC, k_ctgs)  # 生成正文并用k_ctgs加密ATC_C
    Sdh_c2tgs = initHEAD(EX_CTL, INC_C2TGS, len(Sdm_c2tgs))  # 生成首部
    Ssm_c2tgs = dict2str(Sdm_c2tgs)  # 正文dict->str
    Ssh_c2tgs = dict2str(Sdh_c2tgs)  # 首部dict->str
    Ssa_c2tgs = Ssh_c2tgs + '|' + Ssm_c2tgs  # 拼接
    Sba_c2tgs = Ssa_c2tgs.encode()  # str->bytes
    return Sba_c2tgs


def create_C2V(c_ip, tkt_v, k_cv):  # 生成C2V报文
    Sdm_ATCC = initATC(ID_C, c_ip)  # 生成Authenticator_C
    Sdm_c2v = initM_C2V_REQ(tkt_v, Sdm_ATCC, k_cv)  # 生成正文并用k_cv加密ATC_C
    Sdh_c2v = initHEAD(EX_CTL, INC_C2V, len(Sdm_c2v))  # 生成首部
    Ssm_c2v = dict2str(Sdm_c2v)  # 正文dict->str
    Ssh_c2v = dict2str(Sdh_c2v)  # 首部dict->str
    Ssa_c2v = Ssh_c2v + '|' + Ssm_c2v  # 拼接
    Sba_c2v = Ssa_c2v.encode()  # str->bytes
    return Sba_c2v


def C_Send(Dst_socket: sk, dst_flag: int,
           caddr_ip, tkt=None, k_share=None):
    # *生成报文
    Sba_msg = None
    if dst_flag == 0:
        # Sba_msg = create_C2AS_CTF()  # *生成C2AS_CTF报文
        pass
    elif dst_flag == 1:
        Sba_msg = create_C2AS()  # *生成C2AS报文
    elif dst_flag == 2:
        Sba_msg = create_C2TGS(caddr_ip, tkt, k_share)  # *生成C2TGS报文
    elif dst_flag == 3:
        Sba_msg = create_C2V(caddr_ip, tkt, k_share)  # *生成C2V报文
    # *发送
    Dst_socket.send(Sba_msg)
    pass


def C_Main():
    client_ip = IP2AD(C_IP)  # 已是str

    # *C-AS建立连接
    ASsock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    ASsock.connect((AS_IP, AS_PORT))

    # TODO:ctf

    # *发送给AS
    C_Send(ASsock, 1, client_ip)

    # *接收k_ctgs, tkt_tgs
    k_ctgs, ticket_tgs = C_Recv(ASsock)
    ASsock.close()

    # *C-TGS建立连接
    TGSsock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    TGSsock.connect((TGS_IP, TGS_PORT))

    # *发送给TGS
    C_Send(TGSsock, 2, client_ip, tkt=ticket_tgs, k_share=k_ctgs)

    # *接收k_cv, tkt_v
    k_cv, tkt_v = C_Recv(TGSsock, k_ctgs)
    TGSsock.close()

    # *C-V建立连接
    Vsock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    Vsock.connect((V_IP, V_PORT))

    # *发送给V
    C_Send(Vsock, 3, client_ip, tkt_v, k_cv)

    # *接收mdTS_5
    ts_5 = C_Recv(Vsock, k_cv)
    print(ts_5)


if __name__ == '__main__':
    C_Main()
