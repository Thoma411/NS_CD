'''
Author: Thoma411
Date: 2023-05-13 20:18:23
LastEditTime: 2023-05-25 13:03:05
Description:
'''
import socket as sk
from MsgFieldDef import *

ID_C = 11  # 每个C的ID需不同
C_IP = '192.168.137.1'  # !IP需提前声明
AS_IP, AS_PORT = '192.168.137.1', 8010
TGS_IP, TGS_PORT = '192.168.137.1', 8020
V_IP, V_PORT = '192.168.137.60', 8030

MAX_SIZE = 2048

PRT_LOG = True  # 是否打印输出
PKEY_C, SKEY_C = myRSA.RSA_initKey('a', DEF_LEN_RSA_K)  # *生成C的公私钥

K_C = None
C_PKEY_V = None


def Chandle_AS2C_CTF(mt):  # 处理AS2C认证报文
    Rdm_as2c = str2dict(mt)  # str->dict
    cpK_c = Rdm_as2c['K_C']  # 获取K_c(加密状态)
    tmpk_c = myRSA.RSA_decry(cpK_c, SKEY_C)
    k_c = str(tmpk_c).zfill(8)
    if PRT_LOG:
        print('k_c', k_c)
    return k_c


def Chandle_AS2C(mt, k_c):  # 处理AS2C控制报文
    Rsm_as2c = myDES.DES_decry(mt, k_c)  # bytes直接解密为str
    Rdm_as2c = str2dict(Rsm_as2c)  # str->dict
    k_ctgs = Rdm_as2c['K_C_TGS']  # 获取共享密钥k_ctgs
    Ticket_TGS = Rdm_as2c['mTKT_T']  # 获取Ticket_TGS
    if PRT_LOG:
        print('K_ctgs:', k_ctgs)
        print('Ticket_TGS:\n', Ticket_TGS)
    return k_ctgs, Ticket_TGS


def Chandle_TGS2C(mt, k_ctgs):  # 处理TGS2C控制报文
    Rsm_tgs2c = myDES.DES_decry(mt, k_ctgs)  # bytes直接解密为str
    Rdm_tgs2c = str2dict(Rsm_tgs2c)  # str->dict
    k_cv = Rdm_tgs2c['K_C_V']  # 获取共享密钥k_cv
    Ticket_V = Rdm_tgs2c['mTKT_V']  # 获取Ticket_V
    if PRT_LOG:
        print('K_cv:', k_cv)
        print('Ticket_V:\n', Ticket_V)
    return k_cv, Ticket_V


def Chandle_V2C(mt, k_cv):  # 处理V2C控制报文
    Rsm_v2c = myDES.DES_decry(mt, k_cv)  # bytes直接解密为str
    Rdm_v2c = str2dict(Rsm_v2c)  # str->dicts
    ts_5 = Rdm_v2c['TS_5']  # 获取ts_5
    if PRT_LOG:
        print('ts_5:', ts_5)
    return ts_5


def Dhandle_ACC(mt, k_cv):  # 处理允许登录报文
    Rsm_acc = myDES.DES_decry(mt, k_cv)
    Rdm_acc = str2dict(Rsm_acc)
    acc = Rdm_acc['STAT']
    return acc


def Dhandle_QRY(mt, k_cv):  # 处理请求报文
    Rsm_qry = myDES.DES_decry(mt, k_cv)
    Rdm_qry = str2dict(Rsm_qry)
    return Rdm_qry


def C_Recv(Dst_socket: sk, k_share=None):  # C的接收方法
    '''报文在此分割为首部+正文, 正文在函数字典对应的方法处理'''
    Rba_msg = Dst_socket.recv(MAX_SIZE)
    global K_C, C_PKEY_V  # str, tuple

    # *初步分割
    Rsa_msg = Rba_msg.decode()  # bytes->str
    if PRT_LOG:
        print('[C_Recv] C Recv:\n', Rsa_msg)

    if Rsa_msg.count('|') == 1:  # 按分隔符数量划分
        Rsh_msg, Rsm_msg = Rsa_msg.split('|')  # 分割为首部+正文
    elif Rsa_msg.count('|') == 2:
        Rsh_msg, Rsm_msg, Rsc_msg = Rsa_msg.split('|')  # 分割为首部+正文+Rsc
        if findstrX(Rsc_msg, PK_SUFFIX):
            C_PKEY_V = str2PK(Rsc_msg)  # *得到PK_V
        else:
            verFlag = myRSA.RSA_verf(Rsm_msg, Rsc_msg, C_PKEY_V)
            print('数字签名验证:', verFlag)
            if verFlag:
                with open('kerb_main/text1.txt', 'a', encoding='gbk') as f:
                    f.write('successfully verified Digital signature.' + '\n\n')

    Rdh_msg = str2dict(Rsh_msg)  # 首部转字典(正文在函数中转字典)

    # *匹配报文类型
    TMP_KEY, TMP_TKT, TMP_TS = None, None, None  # 临时变量, 将返回值传出if-else
    retFlag: int = 0  # 根据该值决定返回值

    if Rdh_msg['LIGAL'] == H_LIGAL:  # *收包合法
        msg_extp = Rdh_msg['EXTYPE']
        msg_intp = Rdh_msg['INTYPE']

        # *控制报文
        if msg_extp == EX_CTL:
            if msg_intp == INC_AS2C_KC:
                # with open('kerb_main/text2.txt', 'w', encoding='gbk') as f:
                #     f.write('AS to C :' + str(Rsa_msg) + '\n\n')
                K_C = Chandle_AS2C_CTF(Rsm_msg)
                retFlag = INC_AS2C_KC

            elif msg_intp == INC_AS2C:
                with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
                    f.write('AS to C :' + str(Rsa_msg) + '\n\n')
                k_ctgs, tkt_tgs = Chandle_AS2C(Rsm_msg, K_C)  # 处理AS2C正文
                TMP_KEY = k_ctgs  # 将k_ctgs,tkt_tgs传出if-else
                TMP_TKT = tkt_tgs
                retFlag = INC_AS2C

            elif msg_intp == INC_TGS2C:
                with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
                    f.write('TGS to C :' + str(Rsa_msg) + '\n\n')
                k_cv, tkt_v = Chandle_TGS2C(Rsm_msg, k_share)  # 处理TGS2C正文
                TMP_KEY = k_cv  # 将k_cv,tkt_v传出if-else
                TMP_TKT = tkt_v
                retFlag = INC_TGS2C

            elif msg_intp == INC_V2C:
                with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
                    f.write('V to C :' + str(Rsa_msg) + '\n\n')
                ts_5 = Chandle_V2C(Rsm_msg, k_share)  # 处理V2C正文
                TMP_TS = ts_5  # 将ts_5传出if-else
                retFlag = INC_V2C

            else:
                print('no match func for control msg.')

        # *数据报文
        elif msg_extp == EX_DAT:
            if msg_intp == IND_ADM or msg_intp == IND_STU:
                with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
                    f.write('V to C LOGIN :' + str(Rsa_msg) + '\n\n')
                log_acc = Dhandle_ACC(Rsm_msg, k_share)
                retFlag = LOG_ACC
            elif msg_intp == IND_QRY_STU:
                with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
                    f.write('V to C STU_QUERY :' + str(Rsa_msg) + '\n\n')
                Rstu_dict = Dhandle_QRY(Rsm_msg, k_share)
                retFlag = IND_QRY_STU
            elif msg_intp == IND_QRY_ADM:
                with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
                    f.write('V to C ADM_QUERY :' + str(Rsa_msg) + '\n\n')
                Rstu_all_dict = Dhandle_QRY(Rsm_msg, k_share)
                retFlag = IND_QRY_ADM
                pass
            elif msg_intp == IND_ADD:
                pass
            elif msg_intp == IND_DEL:
                pass
            elif msg_intp == IND_UPD:
                pass
            else:
                print('no match func for data msg.')
                pass
    else:  # 收包非法
        print('illegal package!')

    # *根据retFlag决定返回值
    if retFlag == INC_AS2C:  # 返回step2的共享密钥/票据
        return TMP_KEY, TMP_TKT
    elif retFlag == INC_TGS2C:  # 返回step4的共享密钥/票据
        return TMP_KEY, TMP_TKT
    elif retFlag == INC_V2C:  # 返回step6 V生成的时间戳和PK_V
        return TMP_TS, C_PKEY_V
    elif retFlag == LOG_ACC:  # 返回登录许可
        return log_acc
    elif retFlag == IND_QRY_STU:  # 返回单个学生信息字典
        return Rstu_dict
    elif retFlag == IND_QRY_ADM:  # 返回学生信息字典列表
        return Rstu_all_dict
    else:
        pass


def create_C2AS_CTF():  # 生成C2AS_CTF报文
    '''
    变量说明:
    S/R - 发送/接收
    d/s/b/h - 字典/字符串/比特/16进制比特
    h/m/c/a - 首部/正文/签名/拼接整体
    '''
    Sdm_c2as_ctf = initM_C2AS_CTF(ID_C, PKEY_C)  # 生成正文
    Sdh_c2as_ctf = initHEAD(EX_CTL, INC_C2AS_CTF, len(Sdm_c2as_ctf))  # 生成首部
    Ssm_c2as_ctf = dict2str(Sdm_c2as_ctf)  # 正文dict->str
    Ssh_c2as_ctf = dict2str(Sdh_c2as_ctf)  # 首部dict->str
    Ssc_c2as_ctf = myRSA.RSA_sign(Ssm_c2as_ctf, SKEY_C)
    Ssa_c2as_ctf = Ssh_c2as_ctf + '|' + Ssm_c2as_ctf + '|' + Ssc_c2as_ctf  # 拼接
    if PRT_LOG:
        print('Ssa_c2as_ctf:\n', Ssa_c2as_ctf)
    Sba_c2as_ctf = Ssa_c2as_ctf.encode()  # str->bytes
    return Sba_c2as_ctf

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
    Ssa_c2v = Ssh_c2v + '|' + Ssm_c2v + '|' + PK2str(PKEY_C)  # 拼接并加上PK_C
    Sba_c2v = Ssa_c2v.encode()  # str->bytes
    return Sba_c2v


# *------------生成数据报文------------


def create_D_ADMLOG(usr, pwd, k_cv):  # 生成管理员登录报文
    Sdm_log = initM_C2V_LOG(usr, pwd)  # 生成登录正文
    Sdh_log = initHEAD(EX_DAT, IND_ADM, len(Sdm_log))  # 生成首部
    Ssm_log = dict2str(Sdm_log)  # 正文dict->str
    Ssh_log = dict2str(Sdh_log)  # 首部dict->str
    Sbm_log = myDES.DES_encry(Ssm_log, k_cv)  # 已是str类型
    Sbc_log = myRSA.RSA_sign(Sbm_log, SKEY_C)  # *加密正文生成数字签名
    Ssa_log = Ssh_log + '|' + Sbm_log + '|' + Sbc_log  # *拼接含数字签名
    print('[admin_on_login]:', Sbc_log, len(Sbc_log))
    Sba_log = Ssa_log.encode()
    return Sba_log


def create_D_STULOG(usr, pwd, k_cv):  # 生成学生登录报文
    Sdm_log = initM_C2V_LOG(usr, pwd)  # 生成登录正文
    Sdh_log = initHEAD(EX_DAT, IND_STU, len(Sdm_log))  # 生成首部
    Ssm_log = dict2str(Sdm_log)  # 正文dict->str
    Ssh_log = dict2str(Sdh_log)  # 首部dict->str
    Sbm_log = myDES.DES_encry(Ssm_log, k_cv)  # 已是str类型
    Sbc_log = myRSA.RSA_sign(Sbm_log, SKEY_C)  # *加密正文生成数字签名
    Ssa_log = Ssh_log + '|' + Sbm_log + '|' + Sbc_log  # *拼接含数字签名
    print('[stu_on_login]:', Sbc_log, len(Sbc_log))
    Sba_log = Ssa_log.encode()
    return Sba_log


def create_D_STUQRY(sid, k_cv):  # 生成学生查询报文
    Sdm_qry = initM_C2V_DEL(sid)
    Sdh_qry = initHEAD(EX_DAT, IND_QRY_STU, len(Sdm_qry))
    Ssm_qry = dict2str(Sdm_qry)  # 正文dict->str
    Ssh_qry = dict2str(Sdh_qry)  # 首部dict->str
    Sbm_qry = myDES.DES_encry(Ssm_qry, k_cv)  # 已是str类型
    Sbc_qry = myRSA.RSA_sign(Sbm_qry, SKEY_C)  # *加密正文生成数字签名
    Ssa_qry = Ssh_qry + '|' + Sbm_qry + '|' + Sbc_qry  # *拼接含数字签名
    print('[query_student_score]:', Sbc_qry)
    Sba_qry = Ssa_qry.encode()
    return Sba_qry


def create_D_ADMQRY(qry, k_cv):  # 生成管理员查询报文
    Sdm_qry = initM_C2V_ADMIN_QRY(qry)
    Sdh_qry = initHEAD(EX_DAT, IND_QRY_ADM, len(Sdm_qry))
    Ssm_qry = dict2str(Sdm_qry)  # 正文dict->str
    Ssh_qry = dict2str(Sdh_qry)  # 首部dict->str
    Sbm_qry = myDES.DES_encry(Ssm_qry, k_cv)  # 已是str类型
    Sbc_qry = myRSA.RSA_sign(Sbm_qry, SKEY_C)  # *加密正文生成数字签名
    Ssa_qry = Ssh_qry + '|' + Sbm_qry + '|' + Sbc_qry  # *拼接含数字签名
    print('[query_admin_stuscore]:', Sbc_qry)
    Sba_qry = Ssa_qry.encode()
    return Sba_qry


def create_D_ADMADD(stu_dict, k_cv):  # 生成管理员添加学生信息报文
    Sdh_add = initHEAD(EX_DAT, IND_ADD, len(stu_dict))
    Ssm_add = dict2str(stu_dict)  # 正文dict->str
    Ssh_add = dict2str(Sdh_add)  # 首部dict->str
    Sbm_add = myDES.DES_encry(Ssm_add, k_cv)
    Sbc_add = myRSA.RSA_sign(Sbm_add, SKEY_C)  # *加密正文生成数字签名
    Ssa_add = Ssh_add + '|' + Sbm_add + '|' + Sbc_add  # *拼接含数字签名
    print('[add_admin_stuscore]:', Sbc_add)
    Sba_add = Ssa_add.encode()
    return Sba_add


def create_D_ADMDEL(sid, k_cv):  # 生成管理员删除学生信息报文
    Sdm_del = initM_C2V_DEL(sid)
    Sdh_del = initHEAD(EX_DAT, IND_DEL, len(Sdm_del))
    Ssm_del = dict2str(Sdm_del)  # 正文dict->str
    Ssh_del = dict2str(Sdh_del)  # 首部dict->str
    Sbm_del = myDES.DES_encry(Ssm_del, k_cv)
    Sbc_del = myRSA.RSA_sign(Sbm_del, SKEY_C)  # *加密正文生成数字签名
    Ssa_del = Ssh_del + '|' + Sbm_del + '|' + Sbc_del  # *拼接含数字签名
    print('[del_admin_stuscore]:', Sbc_del)
    Sba_del = Ssa_del.encode()
    return Sba_del


def create_D_ADMUPD(stu_dict, k_cv):  # 生成管理员更新学生信息报文
    Sdh_upd = initHEAD(EX_DAT, IND_UPD, len(stu_dict))
    Ssm_upd = dict2str(stu_dict)
    Ssh_upd = dict2str(Sdh_upd)
    Sbm_upd = myDES.DES_encry(Ssm_upd, k_cv)
    Sbc_upd = myRSA.RSA_sign(Sbm_upd, SKEY_C)  # *加密正文生成数字签名
    Ssa_upd = Ssh_upd + '|' + Sbm_upd + '|' + Sbc_upd  # *拼接含数字签名
    print('[query_student_score]:', Sbc_upd)
    Sba_upd = Ssa_upd.encode()
    return Sba_upd


def C_C_Send(Dst_socket: sk, dst_flag: int,
             caddr_ip, tkt=None, k_share=None, ts_5=None):  # 发送控制报文
    # *生成报文
    Sba_msg = None
    if dst_flag == INC_C2AS_CTF:
        Sba_msg = create_C2AS_CTF()  # *生成C2AS_CTF报文
        pass
    elif dst_flag == INC_C2AS:
        Sba_msg = create_C_C2AS()  # 生成C2AS报文
        with open('kerb_main/text1.txt', 'w', encoding='gbk') as f:
            f.write('C to AS :' + str(Sba_msg) + '\n\n')
    elif dst_flag == INC_C2TGS:
        Sba_msg = create_C_C2TGS(caddr_ip, tkt, k_share)  # 生成C2TGS报文
        with open('kerb_main/text1.txt', 'a', encoding='gbk') as f:
            f.write('C to TGS :' + str(Sba_msg) + '\n\n')
    elif dst_flag == INC_C2V:
        Sba_msg = create_C_C2V(caddr_ip, tkt, k_share, ts_5)  # 生成C2V报文
        with open('kerb_main/text1.txt', 'a', encoding='gbk') as f:
            f.write('C to V :' + str(Sba_msg) + '\n\n')
    else:
        print('[C_C_Send] no match func for send ctl_msg.')
    Dst_socket.send(Sba_msg)  # 发送


def C_D_Send(Dst_socket: sk, dst_flag: int,
             usr=None, pwd=None, sid=None, qry=None, stu_dict=None, k_share=None):  # 发送数据报文
    Sba_msg = None
    if dst_flag == IND_ADM:
        Sba_msg = create_D_ADMLOG(usr, pwd, k_share)  # 生成管理员登录报文
        with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
            f.write('C to V LOGIN_ADMIN :' + str(Sba_msg) + '\n\n')
    elif dst_flag == IND_STU:
        Sba_msg = create_D_STULOG(usr, pwd, k_share)  # 生成学生登录报文
        with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
            f.write('C to V LOGIN_STU :' + str(Sba_msg) + '\n\n')
    elif dst_flag == IND_QRY_STU:
        Sba_msg = create_D_STUQRY(sid, k_share)  # 生成学生查询报文
        with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
            f.write('C to V QUERY_STU :' + str(Sba_msg) + '\n\n')
    elif dst_flag == IND_QRY_ADM:
        Sba_msg = create_D_ADMQRY(qry, k_share)  # 生成管理员查询报文
        with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
            f.write('C to V QUERY_ADM :' + str(Sba_msg) + '\n\n')
    elif dst_flag == IND_ADD:
        Sba_msg = create_D_ADMADD(stu_dict, k_share)  # 生成管理员添加学生信息报文
        with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
            f.write('C to V ADD_ADM :' + str(Sba_msg) + '\n\n')
    elif dst_flag == IND_DEL:
        Sba_msg = create_D_ADMDEL(sid, k_share)  # 生成管理员删除学生信息报文
        with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
            f.write('C to V DEL_ADM :' + str(Sba_msg) + '\n\n')
    elif dst_flag == IND_UPD:
        Sba_msg = create_D_ADMUPD(stu_dict, k_share)  # 生成管理员更新学生信息报文
        with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
            f.write('C to V UPDATE_ADM :' + str(Sba_msg) + '\n\n')
    else:
        print('[C_D_Send] no match func for send dat_msg.')
    Dst_socket.send(Sba_msg)  # 发送


def C_Kerberos():
    client_ip = IP2AD(C_IP)  # 已是str

    # *C-AS建立连接
    ASsock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    ASsock.connect((AS_IP, AS_PORT))

    # *获取K_C
    C_C_Send(ASsock, INC_C2AS_CTF, client_ip)
    C_Recv(ASsock)

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
        return True, k_cv, C_PKEY_V, Vsock  # *返回业务逻辑所需的对称钥和PK_V
    else:
        print('[Kerberos] Authentication failed.')
        return False


# *登录调用函数
def SndRcv_msg(Dst_socket: sk, bmsg, k_cv=None):  # 收发消息(含返回值)
    try:
        Dst_socket.sendall(bmsg)  # 发送
        print("Sent message:", bmsg)
        # resp = Dst_socket.recv(MAX_SIZE)
        # print("Received response:", resp)
        # return resp.decode()
        ret = C_Recv(Dst_socket, k_cv)
        return ret
    except Exception as e:
        print("Error:", e)


def admin_on_login(usr, pwd):  # 管理员登录消息
    atc_flag, k_cv, C_PKEY_V, Vsock = C_Kerberos()  # *获取共享密钥和PK_V
    if atc_flag:  # 认证成功
        Sba_log = create_D_ADMLOG(usr, pwd, k_cv)
        # Rsa_log = SndRcv_msg(Vsock, Sba_log, k_cv)  # 收发消息
        # print("[C] admin login response")
        # if Rsa_log == "adm login":
        #     return LOG_ACC, k_cv, C_PKEY_V, Vsock  # *返回PK_V
        # else:
        #     pass
        with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
            f.write('C to V LOG_ADM :' + str(Sba_log) + '\n\n')
        ret = SndRcv_msg(Vsock, Sba_log, k_cv)  # 收发消息
        with open('kerb_main/text1.txt', 'a', encoding='gbk') as f:
            f.write('V to C LOG_ADM :' + str(ret) + '\n\n')
        if ret == LOG_ACC:  # 返回结果为登录ACC
            return LOG_ACC, k_cv, C_PKEY_V, Vsock  # *返回PK_V
        else:
            print('[admLogin] LOG_ACC匹配失败')
    else:
        print('[admLogin] fatal.')


def stu_on_login(usr, pwd):  # 学生登陆消息
    atc_flag, k_cv, C_PKEY_V, Vsock = C_Kerberos()
    if atc_flag:  # 认证成功
        Sba_log = create_D_STULOG(usr, pwd, k_cv)
        # Rsa_log = SndRcv_msg(Vsock, Sba_log)  # 收发消息
        # print("[C] stu login response")
        # if Rsa_log == "stu login":
        #     return LOG_ACC, k_cv, C_PKEY_V, Vsock  # *返回PK_V
        # else:
        #     pass
        with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
            f.write('C to V LOG_STU :' + str(Sba_log) + '\n\n')
        ret = SndRcv_msg(Vsock, Sba_log, k_cv)  # 收发消息
        with open('kerb_main/text1.txt', 'a', encoding='gbk') as f:
            f.write('V to C LOG_STU :' + str(ret) + '\n\n')
        if ret == LOG_ACC:  # 返回结果为登录ACC
            return LOG_ACC, k_cv, C_PKEY_V, Vsock  # *返回PK_V
        else:
            print('[stuLogin] LOG_ACC匹配失败')
    else:
        print('[stuLogin] fatal.')


def query_student_score(Dst_socket: sk, sid, k_cv):  # 学生查询学生成绩
    Sba_qry = create_D_STUQRY(sid, k_cv)
    with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
        f.write('C to V QRY_STU :' + str(Sba_qry) + '\n\n')
    ret = SndRcv_msg(Dst_socket, Sba_qry, k_cv)
    with open('kerb_main/text1.txt', 'a', encoding='gbk') as f:
        f.write('V to C QRY_STU :' + str(ret) + '\n\n')
    return ret


def query_admin_stuscore(Dst_socket: sk, qry, k_cv):  # 管理员查询学生成绩
    Sba_qry = create_D_ADMQRY(qry, k_cv)
    with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
        f.write('C to V QRY_ADM :' + str(Sba_qry) + '\n\n')
    ret = SndRcv_msg(Dst_socket, Sba_qry, k_cv)
    with open('kerb_main/text1.txt', 'a', encoding='gbk') as f:
        f.write('V to C QRY_ADM :' + str(ret) + '\n\n')
    return ret


def add_admin_stuscore(Dst_socket: sk, stu_dict, k_cv):  # 管理员添加学生信息
    Sba_add = create_D_ADMADD(stu_dict, k_cv)
    with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
        f.write('C to V ADD_ADM :' + str(Sba_add) + '\n\n')
    Dst_socket.sendall(Sba_add)


def del_admin_stuscore(Dst_socket: sk, sid, k_cv):  # 管理员删除学生信息
    Sba_del = create_D_ADMDEL(sid, k_cv)
    with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
        f.write('C to V DEL_ADM :' + str(Sba_del) + '\n\n')
    Dst_socket.sendall(Sba_del)


def update_admin_stuscore(Dst_socket: sk, stu_dict, k_cv):  # 管理员更新学生信息
    Sba_upd = create_D_ADMUPD(stu_dict, k_cv)
    with open('kerb_main/text2.txt', 'a', encoding='gbk') as f:
        f.write('C to V UPD_ADM :' + str(Sba_upd) + '\n\n')
    Dst_socket.sendall(Sba_upd)


if __name__ == '__main__':
    # print(C_Kerberos())
    C_Kerberos()
