'''
Author: Thoma411
Date: 2023-05-13 20:22:53
LastEditTime: 2023-05-24 20:39:07
Description:
'''
import socket as sk
import threading as th
from MsgFieldDef import *
import DB_method as ss

V_PORT = 8030
MAX_SIZE = 2048
MAX_LISTEN = 16

PRT_LOG = True  # 是否打印输出
PKEY_V, SKEY_V = myRSA.RSA_initKey('a', DEF_LEN_RSA_K)  # *生成V的公私钥


def Chandle_C2V(mt):  # 处理C2V报文 mt:str
    Rdm_c2v = str2dict(mt)  # 正文str->dict
    tkt_v, atc_c = Rdm_c2v['mTKT_V'], Rdm_c2v['mATC_C']

    # *解密Ticket_V, 获得K_C_V
    Rsm_tktV = myDES.DES_decry(tkt_v, DKEY_V)  # *解密为str
    Rdm_tktV = str2dict(Rsm_tktV)  # str->dict
    k_cv = Rdm_tktV['K_SHARE']  # 取得k_cv共享密钥
    if PRT_LOG:
        print('Ticket_V:\n', Rdm_tktV)

    # *解密Authenticator_C, 获得TS_5
    Rsm_ATCC = myDES.DES_decry(atc_c, k_cv)  # *解密为str
    Rdm_ATCC = str2dict(Rsm_ATCC)  # str->dict
    if PRT_LOG:
        print('Rdm_ATCC:\n', Rdm_ATCC)
    ts_5 = Rdm_ATCC['TS_A']

    # *生成mdTS_5 首部
    Sdm_v2c = initM_V2C_REP(ts_5)  # 生成正文(TS_5+=1)
    Sdh_v2c = initHEAD(EX_CTL, INC_V2C, len(Sdm_v2c))  # 生成首部
    Ssm_v2c = dict2str(Sdm_v2c)  # 正文dict->str
    Ssh_v2c = dict2str(Sdh_v2c)  # 首部dict->str
    Sbm_v2c = myDES.DES_encry(Ssm_v2c, k_cv)  # *加密正文
    Ssa_v2c = Ssh_v2c + '|' + str(Sbm_v2c) + '|' + \
        PK2str(PKEY_V)  # 拼接str(Sbm_v2c已是str)
    if PRT_LOG:
        print('V->C:\n', Ssa_v2c)
    return Ssa_v2c, k_cv  # str+str(bytes)

# *------------处理数据报文------------


def Dhangle_ADM_LOG(mt, k_cv):  # 处理管理员LOG报文 mt:str
    Rsm_log = myDES.DES_decry(mt, k_cv)
    Rdm_log = str2dict(Rsm_log)  # str->dict
    user_adm = Rdm_log['USER']  # 获取登录的用户名和密码
    pswd_adm = Rdm_log['PSWD']
    return user_adm, pswd_adm


def Dhangle_STU_LOG(mt, k_cv):  # 处理学生LOG报文 mt:str
    Rsm_log = myDES.DES_decry(mt, k_cv)
    Rdm_log = str2dict(Rsm_log)  # str->dict
    user_stu = Rdm_log['USER']  # 获取登录的用户名和密码
    pswd_stu = Rdm_log['PSWD']
    return user_stu, pswd_stu


def Dhangle_STU_QRY(mt, k_cv):  # 处理学生请求报文
    Rsm_qry = myDES.DES_decry(mt, k_cv)
    Rdm_qry = str2dict(Rsm_qry)  # str->dict
    sid = Rdm_qry['SID']  # 获取学生ID
    return sid


def Dhangle_ADM_QRY(mt, k_cv):  # 处理管理员请求报文
    adm_str_qry = myDES.DES_decry(mt, k_cv)
    adm_dict_qry = str2dict(adm_str_qry)
    qry = adm_dict_qry['QRY']  # 获取请求讯号
    return qry


def Dhangle_ADM_ADD(mt, k_cv):  # 处理管理员添加学生信息的报文
    adm_str_add = myDES.DES_decry(mt, k_cv)
    adm_dict_add = str2dict(adm_str_add)
    return adm_dict_add


def Dhangle_ADM_UPD(mt, k_cv):  # 处理管理员更新学生信息的报文
    adm_str_update = myDES.DES_decry(mt, k_cv)
    adm_dict_update = str2dict(adm_str_update)
    return adm_dict_update


def Dhangle_ADM_DEL(mt, k_cv):  # 处理管理员删除学生信息的报文
    adm_str_del = myDES.DES_decry(mt, k_cv)
    adm_dict_del = str2dict(adm_str_del)
    sid = adm_dict_del['SID']
    return sid


def create_D_ACC(LOG_TYPE, k_cv):  # 生成登录确认报文
    Sdm_acc = initM_V2C_ACC(LOG_ACC)  # 生成登录确认正文
    Sdh_acc = initHEAD(EX_DAT, LOG_TYPE, len(Sdm_acc))  # 生成首部
    Ssm_acc = dict2str(Sdm_acc)
    Ssh_acc = dict2str(Sdh_acc)
    Sbm_acc = myDES.DES_encry(Ssm_acc, k_cv)
    Sbc_acc = myRSA.RSA_sign(Sbm_acc, SKEY_V)  # *加密正文生成数字签名
    Ssa_acc = Ssh_acc + '|' + Sbm_acc + '|' + Sbc_acc
    if PRT_LOG:
        print('[create_D_ACC]:', Ssa_acc)
    Sba_acc = Ssa_acc.encode()
    return Sba_acc


def create_D_STUQRY(stu_dict, k_cv):  # 生成学生查询报文
    Sdh_qry = initHEAD(EX_DAT, IND_QRY, len(stu_dict))
    Ssm_qry = dict2str(stu_dict)
    Ssh_qry = dict2str(Sdh_qry)
    Sbm_qry = myDES.DES_encry(Ssm_qry, k_cv)
    Sbc_qry = myRSA.RSA_sign(Sbm_qry, SKEY_V)
    Ssa_qry = Ssh_qry + '|' + Sbm_qry + '|' + Sbc_qry
    if PRT_LOG:
        print('[create_D_STUQRY]:', Ssa_qry)
    Sba_qry = Ssa_qry.encode()
    return Sba_qry


def create_D_ADMQRY(stu_all_dict, k_cv):  # 生成管理员查询报文
    Sdh_qry = initHEAD(EX_DAT, IND_QRY, len(stu_all_dict))
    Ssm_qry = dict2str(stu_all_dict)
    Ssh_qry = dict2str(Sdh_qry)
    Sbm_qry = myDES.DES_encry(Ssm_qry, k_cv)
    Sbc_qry = myRSA.RSA_sign(Sbm_qry, SKEY_V)
    Ssa_qry = Ssh_qry + '|' + Sbm_qry + '|' + Sbc_qry
    if PRT_LOG:
        print('[create_D_ADMQRY]:', Ssa_qry)
    Sba_qry = Ssa_qry.encode()
    return Sba_qry


def V_Recv(C_Socket: sk):
    k_cv, V_PKEY_C = None, None  # 在while外临时存储k_cv, PK_C
    while True:
        Rba_msg = C_Socket.recv(MAX_SIZE)  # 收

        # *初步分割
        if not Rba_msg:  # 判空
            # print('msg is empty!')
            break
        Rsa_msg = Rba_msg.decode()  # bytes->str
        Rsh_msg, Rsm_msg, Rsc_msg = Rsa_msg.split('|')  # 分割为首部+正文+PK/Sign
        Rdh_msg = str2dict(Rsh_msg)  # 首部转字典(正文在函数中转字典)
        if PRT_LOG:
            print('C->V:\n', Rsa_msg)  # 输出收到的报文
            # print('sign:', Rsc_msg)
            # print('正文:', Rsm_msg)
        if findstrX(Rsc_msg, PK_SUFFIX):  # 匹配PK后缀
            V_PKEY_C = str2PK(Rsc_msg)  # *得到PK_C str->tuple
        else:
            verFlag = myRSA.RSA_verf(Rsm_msg, Rsc_msg, V_PKEY_C)
            print('数字签名验证:', verFlag)

        # *匹配报文类型
        if Rdh_msg['LIGAL'] == H_LIGAL:  # 收包合法
            msg_extp = Rdh_msg['EXTYPE']
            msg_intp = Rdh_msg['INTYPE']

            if msg_extp == EX_CTL:  # *控制报文
                if msg_intp == INC_C2V:
                    Ssa_msg, k_cv = Chandle_C2V(Rsm_msg)  # 相应函数处理
                    C_Socket.send(Ssa_msg.encode())  # 编码发送
                else:  # 找不到处理函数
                    print('no match func for msg.')

            elif msg_extp == EX_DAT:  # *数据报文
                if msg_intp == IND_ADM:  # 管理员登录
                    print('[ex_dat] K_cv:', k_cv)
                    user_adm, pswd_adm = Dhangle_ADM_LOG(Rsm_msg, k_cv)
                    check_adm_pwd = ss.sql_login_adm(user_adm)  # 管理员登录
                    if pswd_adm == check_adm_pwd:
                        C_Socket.send(create_D_ACC(IND_ADM, k_cv))

                elif msg_intp == IND_STU:  # 学生登录
                    print('[ex_dat] K_cv:', k_cv)
                    user_stu, pswd_stu = Dhangle_STU_LOG(Rsm_msg, k_cv)
                    check_stu_pwd = ss.sql_login_stu(user_stu)  # 学生登录
                    if pswd_stu == check_stu_pwd:
                        C_Socket.send(create_D_ACC(IND_STU, k_cv))

                elif msg_intp == IND_QRY:  # 学生查询请求
                    sid = Dhangle_STU_QRY(Rsm_msg, k_cv)
                    stu_dict = ss.sql_search_stu(sid)  # 学生查询成绩
                    C_Socket.send(create_D_STUQRY(stu_dict, k_cv))

                elif msg_intp == IND_QRY_ADM:  # 管理员查询请求
                    qry = Dhangle_ADM_QRY(Rsm_msg, k_cv)
                    stu_all_dict = ss.sql_search_adm()
                    C_Socket.send(create_D_STUQRY(stu_all_dict, k_cv))

                elif msg_intp == IND_ADD:  # 管理员添加
                    stu_add_dict = Dhangle_ADM_ADD(Rsm_msg, k_cv)
                    ss.sql_add_stu(stu_add_dict)

                elif msg_intp == IND_DEL:  # 管理员删除
                    stu_id = Dhangle_ADM_DEL(Rsm_msg, k_cv)
                    ss.sql_del_stu(stu_id)
                elif msg_intp == IND_UPD:
                    stu_update_dict = Dhangle_ADM_UPD(Rsm_msg, k_cv)
                    ss.sql_update_stu(stu_update_dict)

        else:  # 收包非法
            print('illegal package!')
            break
    C_Socket.close()


def V_Main():
    Vsock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    Vsock.bind(('', V_PORT))
    Vsock.listen(MAX_LISTEN)
    print('V_Tserver started...')
    print('线程信息(连接前):', th.enumerate())
    while True:
        cSocket, cAddr = Vsock.accept()
        print('conn:', cAddr)
        thr = th.Thread(target=V_Recv, args=(cSocket,))
        thr.start()
        thread_num = len(th.enumerate())
        print("线程数量(连接后): %d" % thread_num)
    Vsock.close()


if __name__ == '__main__':
    V_Main()
