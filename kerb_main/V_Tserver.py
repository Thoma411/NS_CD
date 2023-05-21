'''
Author: Thoma411
Date: 2023-05-13 20:22:53
LastEditTime: 2023-05-21 19:31:08
Description:
'''
import socket as sk
import threading as th
from MsgFieldDef import *
import DB_method as ss

V_PORT = 8030
MAX_SIZE = 2048
MAX_LISTEN = 16

PRT_LOG = False  # 是否打印输出


def Chandle_C2V(mt, caddr):  # 处理C2V报文 mt:str
    Rdm_c2v = str2dict(mt)  # 正文str->dict
    tkt_v, atc_c = Rdm_c2v['mTKT_V'], Rdm_c2v['mATC_C']

    # *解密Ticket_V, 获得K_C_V
    Rsm_tktV = cbDES.DES_decry(tkt_v, DKEY_V)  # *解密为str
    Rdm_tktV = str2dict(Rsm_tktV)  # str->dict
    k_cv = Rdm_tktV['K_SHARE']  # 取得k_cv共享密钥
    if PRT_LOG:
        print('Ticket_V:\n', Rdm_tktV)

    # *解密Authenticator_C, 获得TS_5
    Rsm_ATCC = cbDES.DES_decry(atc_c, k_cv)  # *解密为str
    Rdm_ATCC = str2dict(Rsm_ATCC)  # str->dict
    if PRT_LOG:
        print('Rdm_ATCC:\n', Rdm_ATCC)
    ts_5 = Rdm_ATCC['TS_A']

    # *生成mdTS_5 首部
    Sdm_v2c = initM_V2C_REP(ts_5)  # 生成正文(TS_5+=1)
    Sdh_v2c = initHEAD(EX_CTL, INC_V2C, len(Sdm_v2c))  # 生成首部
    Ssm_v2c = dict2str(Sdm_v2c)  # 正文dict->str
    Ssh_v2c = dict2str(Sdh_v2c)  # 首部dict->str
    Sbm_v2c = cbDES.DES_encry(Ssm_v2c, k_cv)  # *加密正文
    Ssa_v2c = Ssh_v2c + '|' + str(Sbm_v2c)  # 拼接str(Sbm_v2c已是str)
    if PRT_LOG:
        print('V->C:\n', Ssa_v2c)
    return Ssa_v2c, k_cv  # str+str(bytes)


def Dhangle_ADM_LOG(mt, k_cv):  # 处理管理员LOG报文 mt:str
    Rsm_log = cbDES.DES_decry(mt, k_cv)
    Rdm_log = str2dict(Rsm_log)  # str->dict
    user_adm = Rdm_log['USER']  # 获取登录的用户名和密码
    pswd_adm = Rdm_log['PSWD']
    return user_adm, pswd_adm


def Dhangle_STU_LOG(mt, k_cv):  # 处理学生LOG报文 mt:str
    Rsm_log = cbDES.DES_decry(mt, k_cv)
    Rdm_log = str2dict(Rsm_log)  # str->dict
    user_stu = Rdm_log['USER']  # 获取登录的用户名和密码
    pswd_stu = Rdm_log['PSWD']
    return user_stu, pswd_stu


def Dhangle_STU_QRY(mt, k_cv):  # 处理学生请求报文
    Rsm_qry = cbDES.DES_decry(mt, k_cv)
    Rdm_qry = str2dict(Rsm_qry)  # str->dict
    sid = Rdm_qry['SID']  # 获取学生ID
    return sid


K_CV = {}
lock = th.Lock()


def V_Recv(C_Socket: sk, cAddr):
    # k_cv = None  # 在while外临时存储k_cv
    while True:
        Rba_msg = C_Socket.recv(MAX_SIZE)  # 收
        tid = th.current_thread().ident  # 获取当前线程的ID

        # *初步分割
        if not Rba_msg:  # 判空
            # print('msg is empty!')
            break
        Rsa_msg = Rba_msg.decode()  # bytes->str
        if PRT_LOG:
            print('C->V:\n', Rsa_msg)
        Rsh_msg, Rsm_msg = Rsa_msg.split('|')  # 分割为首部+正文
        Rdh_msg = str2dict(Rsh_msg)  # 首部转字典(正文在函数中转字典)

        # *匹配报文类型
        if Rdh_msg['LIGAL'] == H_LIGAL:  # 收包合法
            msg_extp = Rdh_msg['EXTYPE']
            msg_intp = Rdh_msg['INTYPE']

            if msg_extp == EX_CTL:  # *控制报文
                if msg_intp == INC_C2V:
                    Ssa_msg, k_cv = Chandle_C2V(Rsm_msg, cAddr)  # 相应函数处理
                    with lock:
                        K_CV[tid] = k_cv  # 当前线程存储k_cv值
                    print('[ex_ctl] V got the K_cv:', k_cv)
                    C_Socket.send(Ssa_msg.encode())  # 编码发送
                else:  # 找不到处理函数
                    print('no match func for msg.')

            elif msg_extp == EX_DAT:  # *数据报文
                with lock:
                    k_cv = K_CV.get(tid)  # 从字典获取线程本地变量值
                if msg_intp == IND_ADM:  # 管理员
                    print('[ex_dat] K_cv:', k_cv)
                    user_adm, pswd_adm = Dhangle_ADM_LOG(
                        Rsm_msg, k_cv)
                    check_adm_pwd = ss.sql_login_adm(user_adm)  # 管理员登录
                    if pswd_adm == check_adm_pwd:
                        C_Socket.send('adm login'.encode())  # !格式

                elif msg_intp == IND_STU:  # 学生
                    print('[ex_dat] K_cv:', k_cv)
                    user_stu, pswd_stu = Dhangle_STU_LOG(
                        Rsm_msg, k_cv)
                    check_stu_pwd = ss.sql_login_stu(user_stu)  # 学生登录
                    if pswd_stu == check_stu_pwd:
                        C_Socket.send('stu login'.encode())  # !格式

                elif msg_intp == IND_QRY:  # 请求/删除
                    sid = Dhangle_STU_QRY(Rsm_msg, k_cv)
                    stu_dict = ss.sql_search_stu(sid)  # 学生查询成绩
                    C_Socket.send(dict2str(stu_dict).encode())  # !格式

        else:  # 收包非法
            print('illegal package!')
            break

        # print(Rsh_msg, Rsm_msg, cAddr)
        # *发送
        # C_Socket.send(Rsa_msg.encode())
        # print('external loop K_CV:', local_data.K_CV)
    C_Socket.close()


def V_Main():
    Vsock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    Vsock.bind(('', V_PORT))
    Vsock.listen(MAX_LISTEN)
    print('V_Tserver started...')
    while True:
        cSocket, cAddr = Vsock.accept()
        print('conn:', cAddr)
        thr = th.Thread(target=V_Recv, args=(cSocket, cAddr))
        thr.start()
    Vsock.close()


if __name__ == '__main__':
    V_Main()
