'''
Author: Thoma411
Date: 2023-05-13 18:59:23
LastEditTime: 2023-05-15 20:12:17
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

DID_TGS = 20  # 默认TGS的ID
DID_V = 30

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

# Ticket_TGS/V
TKT_A = {
    'K_SHARE': bytes,  # K_C_TGS/K_C_V
    'ID_C': int,
    'AD_C': str,
    'ID_DST': int,  # 目标ID
    'TS_A': int,  # 时间戳(共同)
    'LT_A': int  # 有效期(共同)
}

# Authenticator_C
ATC_C = {
    'ID_C': int,
    'AD_C': str,
    'TS_A': int
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
    'mTKT_T': bytes  # 加密bytes
}

# step3 C->TGS
M_C2TGS_REQ = {
    'ID_V': int,
    'mTKT_T': bytes,  # 加密bytes
    'mATC_C': bytes  # 加密bytes
}

# step4 TGS->C
M_TGS2C_REP = {
    'K_C_V': bytes,
    'ID_V': int,
    'TS_4': int,
    'LT_4': int,
    'mTKT_V': bytes  # 加密bytes
}

# step5 C->V
M_C2V_REQ = {
    'mTKT_V': bytes,  # 加密bytes
    'mATC_C': bytes,  # 加密bytess
}

# step6 V->C
M_V2C_REP = {
    'TS_5': int
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


def rmLRctlstr(sstr: str) -> str:  # 清除首尾控制字符
    sstr = sstr.lstrip('b').strip('"')
    tmpLs = sstr.split('}')
    sstr = tmpLs[0] + '}'
    return sstr


def initHEAD(extp, intp, lmt):  # 装载首部
    hmsg_eg = MSG_HEAD
    hmsg_eg['LIGAL'] = H_LIGAL
    hmsg_eg['EXTYPE'] = extp
    hmsg_eg['INTYPE'] = intp
    hmsg_eg['TS_H'] = mf.msg_getTime()
    hmsg_eg['LEN_MT'] = lmt
    hmsg_eg['REDD'] = '0000'
    return hmsg_eg


def initTKT(k_share, id_c, id_dst, ad_c):  # 装载票据
    tmsg_eg = TKT_A
    tmsg_eg['K_SHARE'] = k_share
    tmsg_eg['ID_C'] = id_c
    tmsg_eg['ID_DST'] = id_dst
    tmsg_eg['AD_C'] = ad_c
    tmsg_eg['TS_A'] = mf.msg_getTime()
    tmsg_eg['LT_A'] = DEF_LT
    return tmsg_eg


def initATC(id_c, ad_c):  # 装载Authenticator_C
    amsg_eg = ATC_C
    amsg_eg['ID_C'] = id_c
    amsg_eg['AD_C'] = ad_c
    amsg_eg['TS_A'] = mf.msg_getTime()
    return amsg_eg


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


def initM_C2TGS_REQ(id_v, tkt_tgs, atc_c, k_ctgs):  # step3正文
    mmsg_eg = M_C2TGS_REQ
    mmsg_eg['ID_V'] = id_v
    mmsg_eg['mTKT_T'] = tkt_tgs  # 这里tkt_tgs沿用上一步,无需生成
    mATC_C = cyDES.DES_encry(str(atc_c), k_ctgs)  # 使用k_ctgs加密ATC_C
    hmATC_C = cyDES.binascii.hexlify(mATC_C)  # 转16进制
    mmsg_eg['mATC_C'] = hmATC_C
    return mmsg_eg


def initM_TGS2C_REP(k_cv, id_v, tkt_v):  # step4正文
    mmsg_eg = M_TGS2C_REP
    mmsg_eg['K_C_V'] = k_cv  # 与TKT_V保持一致
    mmsg_eg['ID_V'] = id_v
    mmsg_eg['TS_4'] = mf.msg_getTime()
    mmsg_eg['LT_4'] = DEF_LT
    mTKT_V = cyDES.DES_encry(str(tkt_v), DKEY_V)  # 加密
    hmTKT_V = cyDES.binascii.hexlify(mTKT_V)  # 转16进制
    mmsg_eg['mTKT_V'] = hmTKT_V
    return mmsg_eg


def initM_C2V_REQ(tkt_v, atc_c, k_cv):  # step5正文
    mmsg_eg = M_C2V_REQ
    mmsg_eg['mTKT_V'] = tkt_v  # 这里tkt_v沿用上一步,无需生成
    mATC_C = cyDES.DES_encry(str(atc_c), k_cv)  # 使用k_cv加密ATC_C
    hmATC_C = cyDES.binascii.hexlify(mATC_C)  # 转16进制
    mmsg_eg['mATC_C'] = hmATC_C
    return mmsg_eg


def initM_V2C_REP(ts_5):  # step6正文
    mmsg_eg = M_V2C_REP
    mmsg_eg['TS_5'] = ts_5
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
