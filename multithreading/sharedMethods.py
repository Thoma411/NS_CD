'''
Author: Thoma411
Date: 2023-04-28 16:34:29
LastEditTime: 2023-04-30 23:30:07
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
U_OPT_CLS = 'shutdown'

if __name__ == '__main__':
    ''''''
    a = ''
    atime = gt(a)
    print(atime)
