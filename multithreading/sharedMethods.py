'''
Author: Thoma411
Date: 2023-04-28 16:34:29
LastEditTime: 2023-05-07 09:41:28
Description: 共用变量/方法/函数
'''
import time as tm


def gt(t):
    t = tm.strftime("%H:%M:%S", tm.localtime())
    return t


'''UDP_Parameter'''
U_sIP = '192.168.137.1'
U_cIP = '192.168.137.1'
U_sPort = 12100
U_cPort = 12200
U_MAX_SIZE = 2048  # 数值可上调
U_EDCODE = 'utf-8'
U_OPT_CLS = 'shutdown'

U_MATCH_LIST = {'TS1': 1001, 'TS2': 1002, 'TS3': 1003}

if __name__ == '__main__':
    ''''''
    a = ''
    atime = gt(a)
    print(atime)
    ik = input('key: ')
    for k, v in U_MATCH_LIST.items():
        if ik == k:
            print(v)
