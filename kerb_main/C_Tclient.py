'''
Author: Thoma411
Date: 2023-05-13 20:18:23
LastEditTime: 2023-05-23 10:30:11
Description:
'''
import socket as sk
from MsgFieldDef import *

ID_C = 13  # !每个C的ID需不同
# C_IP = '192.128.137.60'  # !IP需提前声明
#
# AS_IP, AS_PORT = '192.128.137.60', 8010
# TGS_IP, TGS_PORT = '192.128.137.60', 8020
# V_IP, V_PORT = '192.128.137.60', 8030
C_IP = '127.0.0.1'  # !IP需提前声明

AS_IP, AS_PORT = '127.0.0.1', 8010
TGS_IP, TGS_PORT = '127.0.0.1', 8020
V_IP, V_PORT = '127.0.0.1', 8030
MAX_SIZE = 2048

PKEY_C, SKEY_C = cbRSA.RSA_initKey('a', DEF_LEN_RSA_K)  # *生成C的公私钥


def Chandle_AS2C(mt):  # 处理AS2C控制报文
    Rsm_as2c = cbDES.DES_decry(mt, DKEY_C)  # *bytes直接解密为str
    Rdm_as2c = str2dict(Rsm_as2c)  # str->dict
    k_ctgs = Rdm_as2c['K_C_TGS']  # 获取共享密钥k_ctgs
    Ticket_TGS = Rdm_as2c['mTKT_T']  # 获取Ticket_TGS
    return k_ctgs, Ticket_TGS


def Chandle_TGS2C(mt, k_ctgs):  # 处理TGS2C控制报文
    Rsm_tgs2c = cbDES.DES_decry(mt, k_ctgs)  # *bytes直接解密为str
    Rdm_tgs2c = str2dict(Rsm_tgs2c)  # str->dict
    # print(Rdm_tgs2c)
    k_cv = Rdm_tgs2c['K_C_V']  # 获取共享密钥k_cv
    Ticket_V = Rdm_tgs2c['mTKT_V']  # 获取Ticket_V
    return k_cv, Ticket_V


def Chandle_V2C(mt, k_cv):  # 处理V2C控制报文
    Rsm_v2c = cbDES.DES_decry(mt, k_cv)  # *bytes直接解密为str
    Rdm_v2c = str2dict(Rsm_v2c)  # str->dicts
    ts_5 = Rdm_v2c['TS_5']  # 获取ts_5
    return ts_5


Dmsg_handles = {  # 数据报文处理函数字典
    # TODO:预留存放数据报文处理函数
}


def C_Recv(Dst_socket: sk, k_share=None):  # C的接收方法
    '''报文在此分割为首部+正文, 正文在函数字典对应的方法处理'''
    Rba_msg = Dst_socket.recv(MAX_SIZE)  # 收
    C_PKEY_V = 0
    # *初步分割
    Rsa_msg = Rba_msg.decode()  # bytes->str
    if Rsa_msg.count('|') == 1:  # 按分隔符数量划分
        Rsh_msg, Rsm_msg = Rsa_msg.split('|')  # 分割为首部+正文
    elif Rsa_msg.count('|') == 2:  # !此处要求V统一报文后C收到的msg为三段
        Rsh_msg, Rsm_msg, Rsc_msg = Rsa_msg.split('|')  # 分割为首部+正文+Rsc
        if len(Rsc_msg) == DEF_LEN_RSA_K:
            C_PKEY_V = int(Rsc_msg)  # *得到PK_V

    Rdh_msg = str2dict(Rsh_msg)  # 首部转字典(正文在函数中转字典)

    # *匹配报文类型
    TMP_KEY, TMP_TKT, TMP_TS = None, None, None  # 临时变量, 将返回值传出if-else
    retFlag: int = 0  # 根据该值决定返回值

    if Rdh_msg['LIGAL'] == H_LIGAL:  # *收包合法
        msg_extp = Rdh_msg['EXTYPE']
        msg_intp = Rdh_msg['INTYPE']

        # *控制报文
        if msg_extp == EX_CTL:
            if msg_intp == INC_AS2C_CTF:
                # TODO:处理CTF报文
                pass
            elif msg_intp == INC_AS2C:
                k_ctgs, tkt_tgs = Chandle_AS2C(Rsm_msg)  # 处理AS2C正文
                TMP_KEY = k_ctgs  # 将k_ctgs,tkt_tgs传出if-else
                TMP_TKT = tkt_tgs
                retFlag = 2
            elif msg_intp == INC_TGS2C:
                k_cv, tkt_v = Chandle_TGS2C(Rsm_msg, k_share)  # 处理TGS2C正文
                TMP_KEY = k_cv  # 将k_cv,tkt_v传出if-else
                TMP_TKT = tkt_v
                retFlag = 4
            elif msg_intp == INC_V2C:
                ts_5 = Chandle_V2C(Rsm_msg, k_share)  # 处理V2C正文
                TMP_TS = ts_5  # 将ts_5传出if-else
                retFlag = 6
            else:
                print('no match func for control msg.')
        # *数据报文
        elif msg_extp == EX_DAT:
            Dhandler = Dmsg_handles.get((msg_extp, msg_intp))
            if Dhandler:
                pass  # TODO:合并后数据报文处理方法
            else:
                print('no match func for data msg.')
                pass
    else:  # 收包非法
        print('illegal package!')

    # *根据retFlag决定返回值
    if retFlag == 2:  # 返回step2的共享密钥/票据
        return TMP_KEY, TMP_TKT
    elif retFlag == 4:  # 返回step4的共享密钥/票据
        return TMP_KEY, TMP_TKT
    elif retFlag == 6:  # *返回step6 V生成的时间戳和PK_V
        return TMP_TS, C_PKEY_V
    else:
        pass

    # def create_C2AS_CTF():  # 生成C2AS_CTF报文
    '''
    变量说明:
    S/R - 发送/接收
    d/s/b/h - 字典/字符串/比特/16进制比特
    h/m/c/a - 首部/正文/签名/拼接整体
    '''
#     Sdm_c2as_ctf = initM_C2AS_CTF(ID_C, PKEY_C)  # 生成正文
#     Sdc_c2as_ctf = initSIGN(SKEY_C, ID_C, PKEY_C)  # 生成签名
#     Sdh_c2as_ctf = initHEAD(EX_CTL, INC_C2AS_CTF,
#                             len(Sdm_c2as_ctf + Sdc_c2as_ctf))  # 生成首部
#     Ssm_c2as_ctf = dict2str(Sdm_c2as_ctf)  # 正文dict->str
#     Ssc_c2as_ctf = dict2str(Sdc_c2as_ctf)  # 签名dict->str
#     Ssh_c2as_ctf = dict2str(Sdh_c2as_ctf)  # 首部dict->str
#     Ssa_c2as_ctf = Ssh_c2as_ctf + '|' + Ssm_c2as_ctf + '|'+Ssc_c2as_ctf  # 拼接
#     Sba_c2as_ctf = Ssa_c2as_ctf.encode()  # str->bytes
#     return Sba_c2as_ctf

# *------------生成控制报文------------


def create_C_C2AS():  # 生成C2AS报文
    Sdm_c2as = initM_C2AS_REQ(ID_C, DID_TGS)  # 生成正文
    Sdh_c2as = initHEAD(EX_CTL, INC_C2AS, len(Sdm_c2as))  # 生成首部
    Ssm_c2as = dict2str(Sdm_c2as)  # 正文dict->str
    Ssh_c2as = dict2str(Sdh_c2as)  # 首部dict->str
    Ssa_c2as = Ssh_c2as + '|' + Ssm_c2as  # 拼接
    Sba_c2as = Ssa_c2as.encode()  # str->bytes
    return Sba_c2as


def create_C_C2TGS(c_ip, tkt_tgs, k_ctgs):  # 生成C2TGS报文
    Sdm_ATCC = initATC(ID_C, c_ip)  # 生成Authenticator_C
    Sdm_c2tgs = initM_C2TGS_REQ(
        DID_V, tkt_tgs, Sdm_ATCC, k_ctgs)  # 生成正文并用k_ctgs加密ATC_C
    Sdh_c2tgs = initHEAD(EX_CTL, INC_C2TGS, len(Sdm_c2tgs))  # 生成首部
    Ssm_c2tgs = dict2str(Sdm_c2tgs)  # 正文dict->str
    Ssh_c2tgs = dict2str(Sdh_c2tgs)  # 首部dict->str
    Ssa_c2tgs = Ssh_c2tgs + '|' + Ssm_c2tgs  # 拼接
    Sba_c2tgs = Ssa_c2tgs.encode()  # str->bytes
    return Sba_c2tgs


def create_C_C2V(c_ip, tkt_v, k_cv, ts_5=None):  # 生成C2V报文
    Sdm_ATCC = initATC(ID_C, c_ip, ts_5)  # 生成Authenticator_C
    Sdm_c2v = initM_C2V_REQ(tkt_v, Sdm_ATCC, k_cv)  # 生成正文并用k_cv加密ATC_C
    Sdh_c2v = initHEAD(EX_CTL, INC_C2V, len(Sdm_c2v))  # 生成首部
    Ssm_c2v = dict2str(Sdm_c2v)  # 正文dict->str
    Ssh_c2v = dict2str(Sdh_c2v)  # 首部dict->str
    Ssa_c2v = Ssh_c2v + '|' + Ssm_c2v + '|' + str(PKEY_C)  # 拼接并加上PK_C
    Sba_c2v = Ssa_c2v.encode()  # str->bytes
    return Sba_c2v


# *------------生成数据报文------------


def create_D_ADMLOG(user, pswd, k_cv):
    Sdm_log = initM_C2V_LOG(user, pswd)  # 生成登录正文
    Sdh_log = initHEAD(EX_DAT, IND_ADM, len(Sdm_log))  # 生成首部
    Ssm_log = dict2str(Sdm_log)  # 正文dict->str
    Ssh_log = dict2str(Sdh_log)  # 首部dict->str
    Sbm_log = cbDES.DES_encry(Ssm_log, k_cv)  # 已是str类型
    Ssa_log = Ssh_log + '|' + Sbm_log + '|'  # 拼接
    Sba_log = Ssa_log.encode()
    return Sba_log


def create_D_STULOG(user, pswd, k_cv):
    Sdm_log = initM_C2V_LOG(user, pswd)  # 生成登录正文
    Sdh_log = initHEAD(EX_DAT, IND_STU, len(Sdm_log))  # 生成首部
    Ssm_log = dict2str(Sdm_log)  # 正文dict->str
    Ssh_log = dict2str(Sdh_log)  # 首部dict->str
    Sbm_log = cbDES.DES_encry(Ssm_log, k_cv)  # 已是str类型
    Ssa_log = Ssh_log + '|' + Sbm_log + '|'  # 拼接
    Sba_log = Ssa_log.encode()
    print(Ssa_log)
    return Sba_log


def C_C_Send(Dst_socket: sk, dst_flag: int,
             caddr_ip, tkt=None, k_share=None, ts_5=None):  # 发送控制报文
    # *生成报文
    Sba_msg = None
    if dst_flag == INC_C2AS_CTF:
        # Sba_msg = create_C2AS_CTF()  # *生成C2AS_CTF报文
        pass
    elif dst_flag == INC_C2AS:
        Sba_msg = create_C_C2AS()  # *生成C2AS报文
    elif dst_flag == INC_C2TGS:
        Sba_msg = create_C_C2TGS(caddr_ip, tkt, k_share)  # *生成C2TGS报文
    elif dst_flag == INC_C2V:
        Sba_msg = create_C_C2V(caddr_ip, tkt, k_share, ts_5)  # *生成C2V报文
    # *发送
    Dst_socket.send(Sba_msg)
    pass


def C_D_Send(Dst_socket: sk, dst_flag: int,
             user, pswd, k_share=None):  # 发送数据报文
    Sba_msg = None
    if dst_flag == IND_ADM:
        Sba_msg = create_D_ADMLOG(user, pswd, k_share)  # 生成管理员登录报文
    elif dst_flag == IND_STU:
        Sba_msg = create_D_STULOG(user, pswd, k_share)  # 生成学生登录报文
    # *发送
    Dst_socket.send(Sba_msg)
    pass


def C_Kerberos():
    client_ip = IP2AD(C_IP)  # 已是str

    # *C-AS建立连接
    ASsock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    ASsock.connect((AS_IP, AS_PORT))

    # TODO:ctf

    # *发送给AS
    C_C_Send(ASsock, INC_C2AS, client_ip)

    # *接收k_ctgs, tkt_tgs
    k_ctgs, ticket_tgs = C_Recv(ASsock)
    ASsock.close()

    # *C-TGS建立连接
    TGSsock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    TGSsock.connect((TGS_IP, TGS_PORT))

    # *发送给TGS
    C_C_Send(TGSsock, INC_C2TGS, client_ip, tkt=ticket_tgs, k_share=k_ctgs)

    # *接收k_cv, tkt_v
    k_cv, tkt_v = C_Recv(TGSsock, k_ctgs)
    TGSsock.close()

    # *C-V建立连接
    Vsock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    Vsock.connect((V_IP, V_PORT))

    # *发送给V
    send_ts_5 = msg_getTime()
    # print(send_ts_5, type(send_ts_5))
    C_C_Send(Vsock, INC_C2V, client_ip, tkt_v, k_cv, send_ts_5)

    # *接收mdTS_5和PK_V
    recv_ts_5, C_PKEY_V = C_Recv(Vsock, k_cv)
    # print(recv_ts_5, type(recv_ts_5))
    if send_ts_5 == recv_ts_5:
        print('[Kerberos] Authentication success.')
        return True, k_cv, C_PKEY_V  # *返回业务逻辑所需的对称钥和PK_V
    else:
        print('[Kerberos] Authentication failed.')
        return False


# *登录调用函数


def send_message(host, port, bmsg):  # 消息的发送与接收
    # 连接到服务器并发送数据
    try:
        sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        server_address = (host, port)  # 将服务器IP地址和端口号设置为实际情况
        sock.connect(server_address)
        sock.sendall(bmsg)  # 发送
        print("Sent message:", bmsg)
        response = sock.recv(MAX_SIZE)
        print("Received response:", response)
        return response
    except Exception as e:
        print("Error:", e)
    finally:
        sock.close()


def send_message_tmp(host, port, bmsg):  # 消息的发送与接收
    # 连接到服务器并发送数据
    try:
        sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        server_address = (host, port)  # 将服务器IP地址和端口号设置为实际情况
        sock.connect(server_address)
        sock.sendall(bmsg)  # 发送
        print("Sent message:", bmsg)
    except Exception as e:
        print("Error:", e)
    finally:
        sock.close()


def admin_on_login(usr, pwd):  # 管理员登录消息
    atc_flag, k_cv, C_PKEY_V = C_Kerberos()  # *获取共享密钥和PK_V
    if atc_flag:  # 认证成功
        Sdm_log = initM_C2V_LOG(usr, pwd)  # 生成登录正文
        Sdh_log = initHEAD(EX_DAT, IND_ADM, len(Sdm_log))  # 生成首部
        Ssm_log = dict2str(Sdm_log)  # 正文dict->str
        Ssh_log = dict2str(Sdh_log)  # 首部dict->str
        Sbm_log = cbDES.DES_encry(Ssm_log, k_cv)  # 已是str类型
        Sbc_log = cbRSA.RSA_sign(Sbm_log, SKEY_C)  # *加密正文生成数字签名
        Ssa_log = Ssh_log + '|' + Sbm_log + '|' + Sbc_log  # *拼接含数字签名
        print('[admin_on_login]:', Sbc_log, len(Sbc_log))
        # testRSA = cbRSA.RSA_verf(Sbm_log, Sbc_log, PKEY_C)
        # print('C自己解得摘要:', testRSA)
        Sba_log = Ssa_log.encode()
        # 发送消息
        Rba_log = send_message(V_IP, V_PORT, Sba_log)
        Rsa_log = Rba_log.decode()
        print("[C] admin login response")
        if Rsa_log == "adm login":
            return 1, k_cv, C_PKEY_V  # *返回PK_V
        else:
            pass
    else:
        print('[admin_on_login] fatal.')


def stu_on_login(usr, pwd):  # 学生登陆消息
    atc_flag, k_cv, C_PKEY_V = C_Kerberos()
    if atc_flag:  # 认证成功
        Sdm_log = initM_C2V_LOG(usr, pwd)  # 生成登录正文
        Sdh_log = initHEAD(EX_DAT, IND_STU, len(Sdm_log))  # 生成首部
        Ssm_log = dict2str(Sdm_log)  # 正文dict->str
        Ssh_log = dict2str(Sdh_log)  # 首部dict->str
        Sbm_log = cbDES.DES_encry(Ssm_log, k_cv)  # 已是str类型
        Sbc_log = cbRSA.RSA_sign(Sbm_log, SKEY_C)  # *加密正文生成数字签名
        Ssa_log = Ssh_log + '|' + Sbm_log + '|' + Sbc_log  # *拼接含数字签名
        print('[stu_on_login]:', Sbc_log)
        Sba_log = Ssa_log.encode()
        # 发送消息
        Rba_log = send_message(V_IP, V_PORT, Sba_log)
        Rsa_log = Rba_log.decode()
        print("[C] stu login response")
        if Rsa_log == "stu login":
            return 1, k_cv, C_PKEY_V  # *返回PK_V
        else:
            pass
    else:
        print('[stu_on_login] fatal.')


# 学生查询学生成绩
def query_student_score(sid, k_cv):
    Sdm_qry = initM_C2V_DEL(sid)
    Sdh_qry = initHEAD(EX_DAT, IND_QRY, len(Sdm_qry))
    Ssm_qry = dict2str(Sdm_qry)  # 正文dict->str
    Ssh_qry = dict2str(Sdh_qry)  # 首部dict->str
    Sbm_qry = cbDES.DES_encry(Ssm_qry, k_cv)  # 已是str类型
    Sbc_qry = cbRSA.RSA_sign(Sbm_qry, SKEY_C)  # *加密正文生成数字签名
    Ssa_qry = Ssh_qry + '|' + Sbm_qry + '|' + Sbc_qry  # *拼接含数字签名
    print('[query_student_score]:', Sbc_qry)
    Sba_qry = Ssa_qry.encode()

    Rba_log = send_message(V_IP, V_PORT, Sba_qry)
    Rsa_log = Rba_log.decode()
    Rda_log = str2dict(Rsa_log)
    return Rda_log


# 管理员查询学生成绩
def query_admin_stuscore(qry, k_cv):
    Sdm_qry = initM_C2V_ADMIN_QRY(qry)
    Sdh_qry = initHEAD(EX_DAT, IND_QRY_ADM, len(Sdm_qry))
    Ssm_qry = dict2str(Sdm_qry)  # 正文dict->str
    Ssh_qry = dict2str(Sdh_qry)  # 首部dict->str
    Sbm_qry = cbDES.DES_encry(Ssm_qry, k_cv)  # 已是str类型
    Sbc_qry = cbRSA.RSA_sign(Sbm_qry, SKEY_C)  # *加密正文生成数字签名
    Ssa_qry = Ssh_qry + '|' + Sbm_qry + '|' + Sbc_qry  # *拼接含数字签名
    print('[query_admin_stuscore]:', Sbc_qry)
    Sba_qry = Ssa_qry.encode()
    # print('[query_admin_stuscore] encode')
    Rba_qry = send_message(V_IP, V_PORT, Sba_qry)  # 发送接收
    Rsa_qry = Rba_qry.decode()
    Rda_qry = str2dict(Rsa_qry)
    return Rda_qry


# 管理员添加学生信息
def add_admin_stuscore(stu_dict, k_cv):
    Sdh_add = initHEAD(EX_DAT, IND_ADD, len(stu_dict))
    Ssm_add = dict2str(stu_dict)  # 正文dict->str
    Ssh_add = dict2str(Sdh_add)  # 首部dict->str
    Sbm_add = cbDES.DES_encry(Ssm_add, k_cv)
    Sbc_add = cbRSA.RSA_sign(Sbm_add, SKEY_C)  # *加密正文生成数字签名
    Ssa_add = Ssh_add + '|' + Sbm_add + '|' + Sbc_add  # *拼接含数字签名
    print('[add_admin_stuscore]:', Sbc_add)
    Sba_add = Ssa_add.encode()
    send_message_tmp(V_IP, V_PORT, Sba_add)
    pass


def del_admin_stuscore(stu_id, k_cv):
    Sdm_del = initM_C2V_DEL(stu_id)
    Sdh_del = initHEAD(EX_DAT, IND_DEL, len(Sdm_del))
    Ssm_del = dict2str(Sdm_del)  # 正文dict->str
    Ssh_del = dict2str(Sdh_del)  # 首部dict->str
    Sbm_del = cbDES.DES_encry(Ssm_del, k_cv)
    Sbc_del = cbRSA.RSA_sign(Sbm_del, SKEY_C)  # *加密正文生成数字签名
    Ssa_del = Ssh_del + '|' + Sbm_del + '|' + Sbc_del  # *拼接含数字签名
    print('[del_admin_stuscore]:', Sbc_del)
    Sba_del = Ssa_del.encode()
    send_message_tmp(V_IP, V_PORT, Sba_del)


def update_admin_stuscore(stu_dict, k_cv):
    Sdh_upd = initHEAD(EX_DAT, IND_UPD, len(stu_dict))
    Ssm_upd = dict2str(stu_dict)
    Ssh_upd = dict2str(Sdh_upd)
    Sbm_upd = cbDES.DES_encry(Ssm_upd, k_cv)
    Sbc_upd = cbRSA.RSA_sign(Sbm_upd, SKEY_C)  # *加密正文生成数字签名
    Ssa_upd = Ssh_upd + '|' + Sbm_upd + '|' + Sbc_upd  # *拼接含数字签名
    print('[query_student_score]:', Sbc_upd)
    Sba_upd = Ssa_upd.encode()
    send_message_tmp(V_IP, V_PORT, Sba_upd)


if __name__ == '__main__':
    print(C_Kerberos())
