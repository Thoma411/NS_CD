'''
Author: Thoma411
Date: 2023-04-28 16:34:29
LastEditTime: 2023-05-10 22:20:18
Description: 共用变量/方法/函数
'''
import time as tm


def gt(t):  # 获取当前时间
    t = tm.strftime("%H:%M:%S", tm.localtime())
    return t


def mixSTR(str: str, rm: str):  # 剔除字符串内的指定字符
    str = str.replace(rm, '')
    return str


'''UDP_Parameter'''
U_sIP = '192.168.137.1'
U_cIP = '192.168.137.1'
U_sPort = 12100
U_cPort = 12200
U_V_IP = '192.168.137.49'  # 服务端V
U_AS_IP = ''  # 认证服务器AS
U_TGS_IP = ''  # 票据服务器TGS
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
