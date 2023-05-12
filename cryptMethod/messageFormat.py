'''
Author: Thoma411
Date: 2023-05-10 22:23:04
LastEditTime: 2023-05-12 12:17:22
Description: message definition
'''
import datetime as dt
import random as rd
import string as st
import time as tm

LEN_ID = 2  # 编号长度
LEN_AD = 6  # 地址长度
LEN_TS = 10  # 时间戳长度
LEN_LT = 4  # 有效期长度
LEN_KEY = 8  # 密钥长度

DLEN_ID = 1  # 常规ID扩充前的长度
DLEN_TS = 9  # 常规TS扩充前的长度

DEFAULT_KEY = '00000000'  # 默认初始化密钥
DEFAULT_TS = '0000000000'  # 默认初始化时间


def msg_i2s(nu: 'int|str', lo: int):  # 类型转换并扩充报文至目标长度
    '''
    nu: 输入数字\n
    lo: 目标长度\n
    '''
    if len(str(nu)) <= lo:  # 输入数字长度不超过目标长度
        si = str(nu).zfill(lo)
        return si
    else:
        print(f'[inputError] len(input) must be 1, but now is {len(str(nu))}')


def msg_getTime(dgt: int = 4):  # 获取当前时间,默认精确到.后4位
    '''dgt: 时间精确到小数点后 dgt 位'''
    now_time = dt.datetime.now().strftime('%H%M%S%f')[:-(6 - dgt)]
    return now_time


def msg_rndKey(dgt: int = 8):  # 生成定长随机字符串,默认8位
    '''dgt: 生成字符串位数'''
    rnd_str = ''.join(rd.sample(st.ascii_letters + st.digits, dgt))
    return rnd_str


class TICKET:  # ticket内部字段定义
    ID_SRC = 00  # 源编号
    AD_SRC = ''  # 源地址
    ID_DST = ''  # 目标编号
    LT_2 = ''  # *AS2C生成的有效期
    KEY_SHARE = None  # 共享密钥
    TS_2 = None  # *AS2C生成的时间戳

    def __init__(self, id_src, ad_src, id_dst, lt_2, key_share=None, ts_2=None):
        self.ID_SRC = id_src
        self.AD_SRC = ad_src
        self.ID_DST = id_dst
        self.LT_2 = lt_2
        if key_share is not None:  # 判断类型并初始化 防止潜在类型报错
            self.KEY_SHARE = key_share
        else:
            self.KEY_SHARE = msg_rndKey()
        if ts_2 is not None:
            self.TS_2 = ts_2
        else:
            self.TS_2 = msg_getTime()

    @classmethod
    def getTicket(cls, tkt: str):  # 接收票据
        key_share = tkt[:LEN_KEY]
        id_src = tkt[LEN_KEY:LEN_KEY + LEN_ID]
        ad_src = tkt[LEN_KEY + LEN_ID:LEN_KEY + LEN_ID + LEN_AD]
        id_dst = tkt[LEN_KEY + LEN_ID + LEN_AD:
                     LEN_KEY + LEN_ID + LEN_AD + LEN_ID]
        ts_2 = tkt[LEN_KEY + LEN_ID + LEN_AD + LEN_ID:
                   LEN_KEY + LEN_ID + LEN_AD + LEN_ID + LEN_TS]
        lt_2 = tkt[LEN_KEY + LEN_ID + LEN_AD + LEN_ID + LEN_TS:
                   LEN_KEY + LEN_ID + LEN_AD + LEN_ID + LEN_TS + LEN_LT]
        MSG_TICKET = TICKET(id_src, ad_src, id_dst, lt_2, key_share, ts_2)
        return MSG_TICKET

    def show(self):
        print(f'KEY_SHARE: {self.KEY_SHARE}, ID_SRC: {self.ID_SRC},', end=' ')
        print(f'AD_SRC: {self.AD_SRC}, ID_DST: {self.ID_DST},', end=' ')
        print(f'TS_2: {self.TS_2}, LT_2: {self.LT_2}')

    def concatmsg(self):  # 拼接各字段
        MSG_TICKET = self.KEY_SHARE + \
            msg_i2s(self.ID_SRC, LEN_ID) + \
            msg_i2s(self.AD_SRC, LEN_AD) + \
            msg_i2s(self.ID_DST, LEN_ID) +\
            msg_i2s(self.TS_2, LEN_TS) +\
            msg_i2s(self.LT_2, LEN_LT)
        return MSG_TICKET


class C2AS:  # C->AS 报文字段定义
    ID_C = 00
    ID_TGS = 00
    TS_1 = None
    # MSG_C2AS = ''

    def __init__(self, id_c, id_tgs, ts_1=None):
        self.ID_C = id_c
        self.ID_TGS = id_tgs
        if ts_1 is not None:  # 判断类型并初始化 防止潜在类型报错
            self.TS_1 = ts_1
        else:
            self.TS_1 = msg_getTime()

    @classmethod
    def getMsg(cls, msg: str):  # 接收报文 -> class<C2AS>
        id_c = msg[:LEN_ID]  # 0-2
        id_tgs = msg[LEN_ID:LEN_ID * 2]  # 2-4
        ts_1 = msg[LEN_ID * 2:LEN_ID * 2 + LEN_TS]  # 4-14
        MSG_C2AS = C2AS(id_c, id_tgs, ts_1)
        return MSG_C2AS

    @property
    def updateT(self):  # 更新时间戳
        return self.TS_1

    @updateT.setter
    def updateT(self, ts_1):
        self.TS_1 = ts_1

    @updateT.getter
    def updateT(self):
        self.TS_1 = msg_getTime()  # 即时更新时间戳
        return self.TS_1

    def show(self):
        self.updateT
        print(f'ID_C: {self.ID_C}, ID_TGS: {self.ID_TGS}, TS_1: {self.TS_1}')

    def concatmsg(self):  # 拼接各字段
        MSG_C2AS = msg_i2s(self.ID_C, LEN_ID) + \
            msg_i2s(self.ID_TGS, LEN_ID) + \
            msg_i2s(self.TS_1, LEN_TS)
        return MSG_C2AS


class AS2C:  # AS->C 报文字段定义
    ID_C = 00
    ID_TGS = 00
    K_C_TGS = None
    TS_2 = None
    LT_2 = ''
    TICKET_TGS = ''
    #MSG_AS2C = ''

    def __init__(self,  id_tgs, lt_2, k_c_tgs: str = None, ts_2=None):
        self.ID_TGS = id_tgs
        self.LT_2 = lt_2
        if k_c_tgs is not None:
            self.K_C_TGS = k_c_tgs
        else:
            self.K_C_TGS = msg_rndKey()
        if ts_2 is not None:
            self.TS_2 = ts_2
        else:
            self.TS_2 = msg_getTime()

    @classmethod
    def getMsg(cls, msg: str):  # 接收报文 -> class<AS2C>
        k_c_tgs = msg[:LEN_KEY]  # 0-8
        id_tgs = msg[LEN_KEY:LEN_KEY + LEN_ID]  # 8-10
        ts_2 = msg[LEN_KEY + LEN_ID:LEN_KEY + LEN_ID + LEN_TS]  # 10-20
        lt_2 = msg[LEN_KEY + LEN_ID + LEN_TS:LEN_KEY +
                   LEN_ID + LEN_TS + LEN_LT]  # 20-24
        MSG_AS2C = AS2C(id_tgs, lt_2, k_c_tgs, ts_2)
        return MSG_AS2C

    @property
    def updateT(self):  # 更新时间戳和密钥
        return self.K_C_TGS, self.TS_2

    @updateT.setter
    def updateT(self, k_c_tgs, ts_2):
        self.K_C_TGS = k_c_tgs
        self.TS_2 = ts_2

    @updateT.getter
    def updateT(self):
        self.K_C_TGS = msg_rndKey()
        self.TS_2 = msg_getTime()
        return self.TS_2

    def show(self):
        self.updateT
        print(f'K_C_TGS: {self.K_C_TGS}, ID_TGS: {self.ID_TGS},', end=' ')
        print(f'TS_2: {self.TS_2}, LT_2: {self.LT_2}')

    def concatmsg(self):
        MSG_AS2C = self.K_C_TGS + \
            msg_i2s(self.ID_TGS, LEN_ID) + \
            msg_i2s(self.TS_2, LEN_TS) + \
            msg_i2s(self.LT_2, LEN_LT)
        return MSG_AS2C


if __name__ == '__main__':
    # !由于精度较高,临时生成的时间戳可能导致时间比较不同(ticket里的和ticket外的)
    # *别忘了还有首部没写,记得加上偏移量 / 或者剥去首部再调用类方法
    msg1 = C2AS(1, 1)
    msg1.show()
    m1 = msg1.concatmsg()
    print(m1, len(m1))

    msg11 = C2AS.getMsg(m1)
    msg11.show()

    msg2 = AS2C(1, 6000)
    msg2.show()
    m2 = msg2.concatmsg()
    print(m2, len(m2))

    # msg22 = AS2C.getMsg(m2)
    # msg22.show()
    # testmsg1 = C2AS(1, 1)
    # print(testmsg1.updateT)
    # tm.sleep(1)
    # print(testmsg1.updateT)
    # tm.sleep(1)
    # print(testmsg1.TS_1)

    tkt1 = TICKET(1, '127001', 2, 6000)
    tkt1.show()
    tkt11 = tkt1.concatmsg()
    print(tkt11, len(tkt11))
