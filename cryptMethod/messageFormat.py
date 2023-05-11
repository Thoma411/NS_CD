'''
Author: Thoma411
Date: 2023-05-10 22:23:04
LastEditTime: 2023-05-11 13:23:49
Description: 
'''
import datetime as dt
import random as rd
import string as st

LEN_ID = 2  # 编号长度
LEN_AD = 6  # 地址长度
LEN_TS = 10  # 时间戳长度
LEN_LT = 4  # 有效期长度
LEN_KEY = 8  # 密钥长度

DLEN_ID = 1  # 常规ID扩充前的长度
DLEN_TS = 9  # 常规TS扩充前的长度


def msg_i2s(i: 'int|str', li: int, lo: int):  # 类型转换并扩充报文至目标长度
    '''
    i:输入数字\n
    li:输入长度\n
    lo:目标长度\n
    '''
    if len(str(i)) == li:
        si = str(i).zfill(lo)
        return si
    else:
        print(f'[inputError] len(input) must be 1, but now is {len(str(i))}')


def msg_getTime(dgt: int = 4):  # 获取当前时间,默认精确到.后四位
    now_time = dt.datetime.now().strftime('%H%M%S%f')[:-(6 - dgt)]
    return now_time


def msg_rndKey(dgt: int = 8):  # 生成定长随机字符串
    rnd_str = ''.join(rd.sample(st.ascii_letters + st.digits, dgt))
    return rnd_str


class C2AS:
    ID_C = 00
    ID_TGS = 00
    TS_1 = ''
    MSG_C2AS = ''

    def __init__(self, id_c, id_tgs):
        self.ID_C = id_c
        self.ID_TGS = id_tgs
        self.TS_1 = msg_getTime()

    def show(self):
        print(f'ID_C: {self.ID_C}, ID_TGS: {self.ID_TGS}, TS_1: {self.TS_1}')

    def concatmsg(self):
        MSG_C2AS = msg_i2s(self.ID_C, DLEN_ID, LEN_ID) + \
            msg_i2s(self.ID_TGS, DLEN_ID, LEN_ID) + \
            msg_i2s(self.TS_1, LEN_TS, LEN_TS)
        return MSG_C2AS


class AS2C:
    ID_C = 00
    ID_TGS = 00
    K_C_TGS = ''
    TS_2 = ''
    LT_2 = ''
    TICKET_TGS = ''
    MSG_AS2C = ''

    def __init__(self,  id_tgs, lt_2):
        self.K_C_TGS = msg_rndKey()
        self.ID_TGS = id_tgs
        self.TS_2 = msg_getTime()
        self.LT_2 = lt_2

    def show(self):
        print(
            f'ID_C: {self.K_C_TGS}, ID_TGS: {self.ID_TGS}, TS_2: {self.TS_2}, LT_2: {self.LT_2}')

    def concatmsg(self):
        MSG_AS2C = self.K_C_TGS + \
            msg_i2s(self.ID_TGS, DLEN_ID, LEN_ID) + \
            msg_i2s(self.TS_2, LEN_TS, LEN_TS) +\
            msg_i2s(self.LT_2, LEN_LT, LEN_LT)
        return MSG_AS2C


if __name__ == '__main__':
    # !由于精度较高,临时生成的时间戳可能导致时间比较不同(ticket里的和ticket外的)
    msg1 = C2AS(1, 1)
    msg1.show()
    m1 = msg1.concatmsg()
    print(m1, len(m1))

    msg2 = AS2C(1, 6000)
    msg2.show()
    m2 = msg2.concatmsg()
    print(m2, len(m2))
