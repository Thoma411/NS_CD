'''
Author: Thoma411
Date: 2023-05-13 20:22:53
LastEditTime: 2023-05-20 11:40:29
Description:
'''
import socket as sk
import threading as th
from MsgFieldDef import *
import server as ss

SERVER_HOST = '192.168.137.1'
V_PORT = 8030
MAX_SIZE = 2048
MAX_LISTEN = 16


def Chandle_C2V(mt, caddr):  # 处理C2V报文 mt:str
    Rdm_c2v = str2dict(mt)  # 正文str->dict
    tkt_v, atc_c = Rdm_c2v['mTKT_V'], Rdm_c2v['mATC_C']

    # *解密Ticket_V, 获得K_C_V
    Rsm_tktV = cbDES.DES_decry(tkt_v, DKEY_V)  # *解密为str
    Rdm_tktV = str2dict(Rsm_tktV)  # str->dict
    k_cv = Rdm_tktV['K_SHARE']  # 取得k_cv共享密钥
    # print(Rdm_tktV)

    # *解密Authenticator_C, 获得TS_5
    Rsm_ATCC = cbDES.DES_decry(atc_c, k_cv)  # *解密为str
    Rdm_ATCC = str2dict(Rsm_ATCC)  # str->dict
    # print('Rdm_ATCC:\n', Rdm_ATCC)
    ts_5 = Rdm_ATCC['TS_A']

    # *生成mdTS_5 首部
    Sdm_v2c = initM_V2C_REP(ts_5)  # 生成正文(TS_5+=1)
    Sdh_v2c = initHEAD(EX_CTL, INC_V2C, len(Sdm_v2c))  # 生成首部
    Ssm_v2c = dict2str(Sdm_v2c)  # 正文dict->str
    Ssh_v2c = dict2str(Sdh_v2c)  # 首部dict->str
    Sbm_v2c = cbDES.DES_encry(Ssm_v2c, k_cv)  # *加密正文
    Ssa_v2c = Ssh_v2c + '|' + str(Sbm_v2c)  # 拼接str(Sbm_v2c已是str)
    return Ssa_v2c  # str+str(bytes)


def Dhangle_ADM_LOG(mt, k_cv):  # 处理管理员LOG报文 mt:str
    Rsm_log = cbDES.DES_decry(mt, k_cv)
    Rdm_log = str2dict(Rsm_log)  # str->dict
    user = Rdm_log['USER']  # 获取登录的用户名和密码
    pswd = Rdm_log['PSWD']
    return user, pswd


def Dhangle_STU_LOG(mt, k_cv):  # 处理学生LOG报文 mt:str
    Rsm_log = cbDES.DES_decry(mt, k_cv)
    Rdm_log = str2dict(Rsm_log)  # str->dict
    user = Rdm_log['USER']  # 获取登录的用户名和密码
    pswd = Rdm_log['PSWD']
    return user, pswd


Dmsg_handles = {  # 数据报文处理函数字典
    # TODO:预留存放数据报文处理函数
}


def V_Recv(C_Socket: sk, cAddr, k_cv):
    while True:
        Rba_msg = C_Socket.recv(MAX_SIZE)  # 收

        # *初步分割
        if not Rba_msg:  # 判空
            print('msg is empty!')
            break
        Rsa_msg = Rba_msg.decode()  # bytes->str
        Rsh_msg, Rsm_msg = Rsa_msg.split('|')  # 分割为首部+正文
        Rdh_msg = str2dict(Rsh_msg)  # 首部转字典(正文在函数中转字典)

        # *匹配报文类型
        if Rdh_msg['LIGAL'] == H_LIGAL:  # 收包合法
            msg_extp = Rdh_msg['EXTYPE']
            msg_intp = Rdh_msg['INTYPE']

            if msg_extp == EX_CTL:  # *控制报文
                if msg_intp == INC_C2V:
                    Ssa_msg = Chandle_C2V(Rsm_msg, cAddr)  # 相应函数处理
                    C_Socket.send(Ssa_msg.encode())  # 编码发送
                else:  # 找不到处理函数
                    print('no match func for msg.')

            elif msg_extp == EX_DAT:  # *数据报文
                if msg_intp == IND_ADM:  # 管理员
                    user, pswd = Dhangle_ADM_LOG(Rsm_msg, k_cv)
                    check_adm_pwd = ss.sql_login_admin(user)  # 登录
                    if pswd == check_adm_pwd:
                        C_Socket.send('01'.encode())  # !格式
                elif msg_intp == IND_STU:  # 学生
                    user, pswd = Dhangle_STU_LOG(Rsm_msg, k_cv)
                    check_stu_pwd = ss.sql_login_stu(user)  # 登录
                    if pswd == check_stu_pwd:
                        C_Socket.send('01'.encode())  # !格式
                    pass
                print('This is a dataMsg.')
        else:  # 收包非法
            print('illegal package!')
            break

        # print(Rsh_msg, Rsm_msg, cAddr)
        # *发送
        # C_Socket.send(Rsa_msg.encode())
    C_Socket.close()


def V_Main():
    Vsock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    Vsock.bind(('', V_PORT))
    Vsock.listen(MAX_LISTEN)
    print('V_Tserver started...')
    K_cv = '00000000'  # !临时共享密钥
    while True:
        cSocket, cAddr = Vsock.accept()
        print('conn:', cAddr)
        thr = th.Thread(target=V_Recv, args=(cSocket, cAddr, K_cv))
        thr.start()
    Vsock.close()


if __name__ == '__main__':
    V_Main()
