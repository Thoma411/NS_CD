'''
Author: Thoma411
Date: 2023-05-13 18:59:23
LastEditTime: 2023-05-23 11:32:08
Description: 
'''

import datetime as dt
import random as rd
import string as st
import cbDES
import cbRSA

H_LIGAL = 80  # 合法包
EX_CTL = 10  # 控制报文
EX_DAT = 20  # 数据报文

# INC_:控制报文类型
INC_C2AS_CTF = 95  # C->AS 申请证书报文
INC_AS2C_CTF = 96  # AS->C 回复证书报文
INC_C2AS = 10
INC_AS2C = 20
INC_C2TGS = 30
INC_TGS2C = 40
INC_C2V = 50
INC_V2C = 60

# IND_:控制报文类型
IND_ADM = 10  # 管理员
IND_STU = 11  # 学生
IND_QRY = 12  # 请求/删除
IND_QRY_ADM = 13  # 管理员请求
IND_ADD = 14  # 管理员增加
IND_DEL = 15  # 管理员删除
IND_UPD = 16  # 管理员更新

DEF_LT = 6000  # 默认有效期

DID_TGS = 20  # 默认TGS的ID
DID_V = 30  # 默认V的ID

DEF_LEN_RSA_K = 256
# PKEY_C, SKEY_C = cbRSA.RSA_initKey('a', DEF_LEN_RSA_K)
# PKEY_V, SKEY_V = cbRSA.RSA_initKey('a', DEF_LEN_RSA_K)

# PKEY_AS = '00000000'  # AS的公钥
# SKEY_AS = '00000000'  # AS的私钥

DKEY_C = '00000000'  # 预置C密钥
DKEY_TGS = '00000000'  # 预置TGS密钥
DKEY_V = '00000000'  # 预置V密钥
DKEY_CV = '00000000'

PK_SUFFIX = 'x'  # PK字符串后缀

# 通用首部
MSG_HEAD = {
    'LIGAL': int,  # 合法性
    'EXTYPE': int,  # 外部类型
    'INTYPE': int,  # 内部类型
    'TS_H': int,  # 时间戳
    'LEN_MT': int,  # 正文长度
    'REDD': str  # 冗余
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

# (M)Signature_C/AS
M_SIG_SRC_AC = {
    'ID_SRC': int,  # 发送方的ID
    'PK_SRC': bytes,  # 发送方的公钥
    'TS_0': int
}

# Signature_C/AS
SIG_SRC_AC = {
    'M_SIG_SRC': bytes  # 加密后的数字签名
}

# Signature_C/V
SIG_SRC_CV = {
    'CPT_SIG': str  # 密文->摘要->签名
}

# certification step1 C->AS
M_C2AS_CTF = {
    'ID_C': int,
    'PK_C': bytes,  # C的公钥
}

# certification step1.5 AS->C K
M_AS2C_KC = {
    'K_C': bytes  # 下一步会话的对称钥
}

# certification step2 AS->C MT
M_AS2C_CTF = {
    'ID_AS': int,
    'PK_AS': bytes,  # AS的公钥
}

# *-----------------kerberos-----------------

# kerberos step1 C->AS
M_C2AS_REQ = {
    'ID_C': int,
    'ID_TGS': int,
    'TS_1': int
}

# kerberos step2 AS->C
M_AS2C_REP = {
    'K_C_TGS': str,
    'ID_TGS': int,
    'TS_2': int,
    'LT_2': int,
    'mTKT_T': str  # 加密
}

# kerberos step3 C->TGS
M_C2TGS_REQ = {
    'ID_V': int,
    'mTKT_T': str,  # 加密
    'mATC_C': str  # 加密
}

# kerberos step4 TGS->C
M_TGS2C_REP = {
    'K_C_V': str,
    'ID_V': int,
    'TS_4': int,
    'LT_4': int,
    'mTKT_V': str  # 加密
}

# kerberos step5 C->V
M_C2V_REQ = {
    'mTKT_V': str,  # 加密
    'mATC_C': str,  # 加密
}

# kerberos step6 V->C
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

# *-----------------data msg def-----------------

# login in
M_C2V_LOG = {
    'USER': str,  # 用户名
    'PSWD': str  # 密码
}

# add mdf chk
M_C2V_GRADE = {
    'NAME': str,  # 姓名
    'GEND': str,  # 性别
    'AGE': int,
    'MARK_C': int,  # 语文成绩
    'MARK_M': int,  # 数学成绩
    'MARK_E': int  # 英语成绩
}

M_C2V_ADD = {
    'ID': int,  # 学号
    'NAME': str,  # 姓名
    'GEND': str,  # 性别
    'AGE': int,
    'MARK_C': int,  # 语文成绩
    'MARK_M': int,  # 数学成绩
    'MARK_E': int  # 英语成绩
}

# del msg
M_C2V_DEL = {
    'SID': int  # 学号
}

# OK msg
M_V2C_ACC = {
    'STAT': int  # 确认状态
}

M_C2V_QRY = {
    'QRY': int
}

# *-----------------share method-----------------


def dict2str(sdict: dict):  # 字典转字符串
    st = str(sdict)
    return st


def str2dict(dstr: str):  # 字符串转字典
    dt = eval(dstr)
    return dt


def rmLRctlstr(sstr: str) -> str:  # 清除首尾控制字符
    sstr = sstr.lstrip('b').strip('"')
    tmpLs = sstr.split('}')
    sstr = tmpLs[0] + '}'
    return sstr


def IP2AD(IP: str):  # IP -> 6位AD字段
    IPsplit = IP.split('.')
    IPstr = []
    for i in IPsplit:
        i = i.zfill(3)
        IPstr.append(i)
        msg_ad = ''.join(IPstr)
    return msg_ad[6:]


def msg_getTime(dgt: int = 4, retType: str = 's'):  # 获取当前时间,默认精确到.后4位
    '''dgt: 时间精确到小数点后 dgt 位'''
    now_time = dt.datetime.now().strftime('%H%M%S%f')[:-(6 - dgt)]
    if retType == 's':
        return now_time
    else:
        return int(now_time)


def msg_rndKey(dgt: int = 8, retType: str = 's'):  # 生成定长随机字符串,默认8位
    '''dgt: 生成字符串位数'''
    rnd_str = ''.join(rd.sample(st.ascii_letters + st.digits, dgt))
    if retType == 's':
        return rnd_str
    else:
        return rnd_str.encode()


def PK2str(PK: tuple):  # 将PK由tuple转成拼接str
    n, e = PK
    SRsc_msg = str(n) + '+' + str(e) + PK_SUFFIX  # 添加识别后缀
    return SRsc_msg


def str2PK(str_msg: str):  # 将PK由拼接str转成tuple
    str_msg = str_msg.rstrip(PK_SUFFIX)
    n, e = str_msg.split('+')
    PK = int(n), int(e)
    return PK


def findstrX(Rsc_msg: str, tgt: str):  # 查找收到字符串中的指定元素
    findIdx = Rsc_msg.find(tgt)
    if findIdx == -1:
        return False
    else:
        return True

# *-----------------init method-----------------


def initHEAD(extp, intp, lmt):  # 装载首部
    hmsg_eg = MSG_HEAD
    hmsg_eg['LIGAL'] = H_LIGAL
    hmsg_eg['EXTYPE'] = extp
    hmsg_eg['INTYPE'] = intp
    hmsg_eg['TS_H'] = msg_getTime()
    hmsg_eg['LEN_MT'] = lmt
    hmsg_eg['REDD'] = '0000'
    return hmsg_eg


def initTKT(k_share, id_c, id_dst, ad_c, prtLog=False):  # 装载票据
    tmsg_eg = TKT_A
    tmsg_eg['K_SHARE'] = k_share
    tmsg_eg['ID_C'] = id_c
    tmsg_eg['ID_DST'] = id_dst
    tmsg_eg['AD_C'] = ad_c
    tmsg_eg['TS_A'] = msg_getTime()
    tmsg_eg['LT_A'] = DEF_LT
    if prtLog:  # 是否打印输出
        print('Ticket:\n', tmsg_eg)
    return tmsg_eg


def initATC(id_c, ad_c, ts=None):  # 装载Authenticator_C
    amsg_eg = ATC_C
    amsg_eg['ID_C'] = id_c
    amsg_eg['AD_C'] = ad_c
    if ts is not None:
        amsg_eg['TS_A'] = ts  # 手动给TS_5赋值
    else:
        amsg_eg['TS_A'] = msg_getTime()
    return amsg_eg


def initSIGN(cpmsg, sk_src):  # 生成数字签名
    dmsg_eg = SIG_SRC_CV
    ssmg_sig = cbRSA.RSA_sign(cpmsg, sk_src)
    dmsg_eg['CPT_SIG'] = ssmg_sig
    return dmsg_eg


def initM_C2AS_CTF(id_c, pk_c):  # certification step1正文
    mmsg_eg = M_C2AS_CTF
    mmsg_eg['ID_C'] = id_c
    mmsg_eg['PK_C'] = pk_c
    return mmsg_eg


def initM_AS2C_CTF(id_as, pk_as):  # certification step2正文
    mmsg_eg = M_AS2C_CTF
    mmsg_eg['ID_AS'] = id_as
    mmsg_eg['PK_AS'] = pk_as
    return mmsg_eg


def initM_C2AS_REQ(id_c, id_tgs):  # kerberos step1正文
    mmsg_eg = M_C2AS_REQ
    mmsg_eg['ID_C'] = id_c
    mmsg_eg['ID_TGS'] = id_tgs
    mmsg_eg['TS_1'] = msg_getTime()
    return mmsg_eg


def initM_AS2C_REP(k_ctgs, id_tgs, tkt_tgs):  # kerberos step2正文
    mmsg_eg = M_AS2C_REP
    mmsg_eg['K_C_TGS'] = k_ctgs  # 与TKT_T保持一致
    mmsg_eg['ID_TGS'] = id_tgs
    mmsg_eg['TS_2'] = msg_getTime()
    mmsg_eg['LT_2'] = DEF_LT
    # *str(tkt_tgs)是为了防止传入的是非字符串类型(如字典)
    sTKT_T = cbDES.DES_encry(str(tkt_tgs), DKEY_TGS)  # 加密
    mmsg_eg['mTKT_T'] = sTKT_T
    return mmsg_eg


def initM_C2TGS_REQ(id_v, tkt_tgs, atc_c, k_ctgs):  # kerberos step3正文
    mmsg_eg = M_C2TGS_REQ
    mmsg_eg['ID_V'] = id_v
    mmsg_eg['mTKT_T'] = tkt_tgs  # 这里tkt_tgs沿用上一步,无需生成
    sATC_C = cbDES.DES_encry(str(atc_c), k_ctgs)  # 使用k_ctgs加密ATC_C
    mmsg_eg['mATC_C'] = sATC_C  # sATC_C为字符串
    return mmsg_eg


def initM_TGS2C_REP(k_cv, id_v, tkt_v):  # kerberos step4正文
    mmsg_eg = M_TGS2C_REP
    mmsg_eg['K_C_V'] = k_cv  # 与TKT_V保持一致
    mmsg_eg['ID_V'] = id_v
    mmsg_eg['TS_4'] = msg_getTime()
    mmsg_eg['LT_4'] = DEF_LT
    sTKT_V = cbDES.DES_encry(str(tkt_v), DKEY_V)  # 加密
    mmsg_eg['mTKT_V'] = sTKT_V
    return mmsg_eg


def initM_C2V_REQ(tkt_v, atc_c, k_cv):  # kerberos step5正文
    mmsg_eg = M_C2V_REQ
    mmsg_eg['mTKT_V'] = tkt_v  # 这里tkt_v沿用上一步,无需生成
    sATC_C = cbDES.DES_encry(str(atc_c), k_cv)  # 使用k_cv加密ATC_C
    mmsg_eg['mATC_C'] = sATC_C
    return mmsg_eg


def initM_V2C_REP(ts_5):  # kerberos step6正文
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


def initM_C2V_LOG(user, pswd):  # 管理员登录正文
    mmsg_eg = M_C2V_LOG
    mmsg_eg['USER'] = user
    mmsg_eg['PSWD'] = pswd
    return mmsg_eg


def initM_C2V_GRADE(name, gend, age, markc, markm, marke):  # 学生成绩管理正文
    mmsg_eg = M_C2V_GRADE
    mmsg_eg['NAME'] = name
    mmsg_eg['GEND'] = gend
    mmsg_eg['AGE'] = age
    mmsg_eg['MARK_C'] = markc
    mmsg_eg['MARK_M'] = markm
    mmsg_eg['MARK_E'] = marke
    return mmsg_eg


def initM_C2V_DEL(sid):  # 删除正文
    mmsg_eg = M_C2V_DEL
    mmsg_eg['SID'] = sid
    return mmsg_eg


def initM_C2V_ADMIN_QRY(qry):  # 请求查询全部学生信息的正文
    mmsg_eg = M_C2V_QRY
    mmsg_eg['QRY'] = qry
    return mmsg_eg


def initM_V2C_ACC(state):  # 确认状态正文
    mmsg_eg = M_V2C_ACC
    mmsg_eg['STAT'] = state
    return mmsg_eg


if __name__ == '__main__':
    atc1 = initATC(1, '137001', 1)
    # print(atc1)
    # ds_atc1 = cbDES.DES_encry(str(atc1), msg_rndKey())
    # print(ds_atc1)
    # s1 = initSIGN('fw7qw', SKEY_C)
    # print(s1)
    pk1, sk1 = cbRSA.RSA_initKey('a', 40)
    spk1 = PK2str(pk1)
    print(pk1, '\nspk1:', spk1, len(spk1))
    print(findstrX(spk1, PK_SUFFIX))
    dspk1 = str2PK(spk1)
    print(dspk1)
