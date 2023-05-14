'''
Author: Thoma411
Date: 2023-05-13 20:18:23
LastEditTime: 2023-05-14 23:32:18
Description:
'''
import socket as sk
from MsgFieldDef import *

AS_IP, AS_PORT = '192.168.137.1', 8010
TGS_IP, TGS_PORT = '192.168.137.1', 8020
V_IP, V_PORT = '192.168.137.1', 8030
MAX_SIZE = 2048

# !是否需要建立一个收包线程


def handleC_AS2C(mt):  # 处理AS2C控制报文
    mt = mt.lstrip('b').strip("'")
    # print(mt, len(mt))
    Rhm_as2c = cyDES.binascii.unhexlify(mt.encode())  # 得到加密正文
    Rsm_as2c = cyDES.DES_decry(Rhm_as2c, DKEY_C, 's')  # bytes直接解密为str
    Rsm_as2c = Rsm_as2c.lstrip('b').strip('"').rstrip('\\x01')
    # print(Rsm_as2c)
    Rdm_as2c = str2dict(Rsm_as2c)
    k_ctgs = Rdm_as2c['K_C_TGS']  # 获取共享密钥
    Ticket_TGS = Rdm_as2c['mTKT_T']  # 获取Ticket_TGS
    # print(mTKT_t)
    # Rhm_tkt = cyDES.binascii.unhexlify(mTKT_t)
    # Tkt = cyDES.DES_decry(Rhm_tkt, DKEY_TGS)
    # print(Tkt)
    return k_ctgs, Ticket_TGS


def handleC_TGS2C(mt):  # 处理TGS2C控制报文
    pass


def handleC_V2C(mt):  # 处理V2C控制报文
    pass


msg_handles = {  # 消息处理函数字典
    (EX_CTL, INC_AS2C): handleC_AS2C,
    (EX_CTL, INC_TGS2C): handleC_TGS2C,
    (EX_CTL, INC_V2C): handleC_V2C
}


def C_Recv(Dst_socket: sk):
    Rba_msg = Dst_socket.recv(MAX_SIZE)  # 收

    # *初步分割
    Rsa_msg = Rba_msg.decode()  # bytes->str
    Rsh_msg, Rsm_msg = Rsa_msg.split('|')  # 分割为首部+正文
    Rdh_msg = str2dict(Rsh_msg)  # 首部转字典(正文在函数中转字典)

    # *匹配报文类型
    if Rdh_msg['LIGAL'] == H_LIGAL:  # 收包合法
        msg_extp = Rdh_msg['EXTYPE']
        msg_intp = Rdh_msg['INTYPE']
        # 在消息处理函数字典中匹配
        handler = msg_handles.get((msg_extp, msg_intp))
        if handler:
            k_share, tkt_next = handler(Rsm_msg)  # 相应函数处理
            print(k_share, tkt_next)
        else:  # 找不到处理函数
            print('no match func for msg.')
    else:  # 收包非法
        print('illegal package!')
    pass


def C_Main():
    # *:C-AS建立连接
    ASsock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    ASsock.connect((AS_IP, AS_PORT))

    # *生成C2AS报文
    '''
    变量说明:
    S/R - 发送/接收
    d/s/b/h - 字典/字符串/比特/16进制比特
    h/m/a - 首部/正文/拼接整体
    '''
    Sdm_c2as = initM_C2AS_REQ(1, 1)
    Sdh_c2as = initHEAD(EX_CTL, INC_C2AS, len(Sdm_c2as))
    Ssm_c2as = dict2str(Sdm_c2as)  # dict->str
    Ssh_c2as = dict2str(Sdh_c2as)
    Ssa_c2as = Ssh_c2as + '|' + Ssm_c2as  # 拼接
    Sba_c2as = Ssa_c2as.encode()  # str->bytes

    # *发送
    ASsock.send(Sba_c2as)

    # *接收
    C_Recv(ASsock)
    # print(response)
    ASsock.close()


if __name__ == '__main__':
    C_Main()
    # print(C2AS_REQ)
    # packed_data = st.pack(
    #     '!HH10s', C2AS_REQ['ID_C'], C2AS_REQ['ID_TGS'], C2AS_REQ['TS_1'].encode('ascii'))
    # print(packed_data)
    # upd = st.unpack('!HH10s', packed_data)
    # print(upd)
