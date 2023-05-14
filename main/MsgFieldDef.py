'''
Author: Thoma411
Date: 2023-05-13 18:59:23
LastEditTime: 2023-05-14 22:06:44
Description: 
'''
import messageFormat as mf
import cyDES

H_LIGAL = 80  # 合法包
EX_CTL = 10  # 控制报文
EX_DAT = 20  # 数据报文

# INC_:控制报文类型
INC_C2AS = 10
INC_AS2C = 20
INC_C2TGS = 30
INC_TGS2C = 40
INC_C2V = 50
INC_V2C = 60

DEF_LT = 6000  # 默认有效期

DKEY_C = '00000000'  # 预置C密钥
DKEY_TGS = '00000000'  # 预置TGS密钥
DKEY_V = '00000000'  # 预置V密钥

# 首部
MSG_HEAD = {
    'LIGAL': int,
    'EXTYPE': int,
    'INTYPE': int,
    'TS_H': int,
    'LEN_MT': int,
    'REDD': str
}

# Ticket_TGS
TKT_T = {
    'K_C_TGS': bytes,
    'ID_C': int,
    'AD_C': str,
    'ID_TGS': int,
    'TS_2': int,
    'LT_2': int
}

# Ticket_V
TKT_V = {
    'K_C_V': bytes,
    'ID_C': int,
    'AD_C': str,
    'ID_V': int,
    'TS_4': int,
    'LT_4': int
}

# Authenticator_C
ATC_C = {
    'ID_C': int,
    'AD_C': str,
    'TS_3': int
}

# step1 C->AS
M_C2AS_REQ = {
    'ID_C': int,
    'ID_TGS': int,
    'TS_1': int
}

# step2 AS->C
M_AS2C_REP = {
    'K_C_TGS': bytes,
    'ID_TGS': int,
    'TS_2': int,
    'LT_2': int,
    'mTKT_T': bytes  # 加密字符串
}

# step3 C->TGS
M_C2TGS_REQ = {
    'ID_V': int,
    'mTKT_T': bytes,  # 加密字符串
    'mATC_C': bytes  # 加密字符串
}

# step4 TGS->C
M_TGS2C_REP = {
    'K_C_V': bytes,
    'ID_V': int,
    'TS_4': int,
    'LT_4': int,
    'mTKT_V': bytes  # 加密字符串
}

# step5 C->V
M_C2V_REQ = {
    'mTKT_V': bytes,  # 加密字符串
    'mATC_C': bytes  # 加密字符串
}

# step6 V->C
M_V2C_REP = {
    'TS_4': int
}

C2AS_REQ = {
    'MSG_HEAD': MSG_HEAD,
    'M_C2AS_REQ': M_C2AS_REQ
}

AS2C_REP = {
    'MSG_HEAD': MSG_HEAD,
    'M_AS2C_REP': M_AS2C_REP
}

C2TGS_REQ = {
    'MSG_HEAD': MSG_HEAD,
    'M_C2TGS_REQ': M_C2TGS_REQ
}

TGS2C_REP = {
    'MSG_HEAD': MSG_HEAD,
    'M_TGS2C_REP': M_TGS2C_REP
}

C2V_REQ = {
    'MSG_HEAD': MSG_HEAD,
    'M_C2V_REQ': M_C2V_REQ
}

V2C_REP = {
    'MSG_HEAD': MSG_HEAD,
    'M_V2C_REP': M_V2C_REP
}


def dict2str(sdict: dict):
    st = str(sdict)
    return st


def str2dict(dstr: str):
    dt = eval(dstr)
    return dt


def initHEAD(extp, intp, lmt):
    hmsg_eg = MSG_HEAD
    hmsg_eg['LIGAL'] = H_LIGAL
    hmsg_eg['EXTYPE'] = extp
    hmsg_eg['INTYPE'] = intp
    hmsg_eg['TS_H'] = mf.msg_getTime()
    hmsg_eg['LEN_MT'] = lmt
    hmsg_eg['REDD'] = '0000'
    return hmsg_eg


def initTKT(k_share, id_c, id_tgs, ad_c):
    tmsg_eg = TKT_T
    tmsg_eg['K_SHARE'] = k_share
    tmsg_eg['ID_C'] = id_c
    tmsg_eg['ID_TGS'] = id_tgs
    tmsg_eg['AD_C'] = ad_c
    tmsg_eg['TS_2'] = mf.msg_getTime()
    tmsg_eg['LT_2'] = DEF_LT
    return tmsg_eg


def initM_C2AS_REQ(id_c, id_tgs):  # step1正文
    mmsg_eg = M_C2AS_REQ
    mmsg_eg['ID_C'] = id_c
    mmsg_eg['ID_TGS'] = id_tgs
    mmsg_eg['TS_1'] = mf.msg_getTime()
    return mmsg_eg


def initM_AS2C_REP(k_ctgs, id_tgs, tkt_tgs):  # step2正文
    mmsg_eg = M_AS2C_REP
    mmsg_eg['K_C_TGS'] = k_ctgs  # 与TKT_T保持一致
    mmsg_eg['ID_TGS'] = id_tgs
    mmsg_eg['TS_2'] = mf.msg_getTime()
    mmsg_eg['LT_2'] = DEF_LT
    mTKT_T = cyDES.DES_encry(str(tkt_tgs), DKEY_TGS)  # 加密
    hmTKT_T = cyDES.binascii.hexlify(mTKT_T)  # 转16进制
    mmsg_eg['mTKT_T'] = hmTKT_T
    return mmsg_eg


def initC2AS_REQ(head, mt):  # step1
    msg_eg = C2AS_REQ
    msg_eg['MSG_HEAD'] = head
    msg_eg['M_C2AS_REQ'] = mt
    return msg_eg


def initAS2C_REP(head, mt):  # step2
    #!正文待加密
    msg_eg = AS2C_REP
    msg_eg['MSG_HEAD'] = head
    msg_eg['M_AS2C_REP'] = mt
    return msg_eg


if __name__ == '__main__':
    m1 = initM_C2AS_REQ(1, 1)
    h1 = initHEAD(10, 10, len(m1))
    hm1 = initC2AS_REQ(h1, m1)
    shm1 = dict2str(hm1)
    print(shm1, type(shm1))

    # s1 = dict2str(m1)
    # print(s1, type(s1))
    rhm1 = str2dict(shm1)
    idc = rhm1['M_C2AS_REQ']['ID_C']
    print(rhm1, type(rhm1))
    print(idc)
