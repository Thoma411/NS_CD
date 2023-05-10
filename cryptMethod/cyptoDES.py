'''
Author: Thoma411
Date: 2023-05-09 11:23:42
LastEditTime: 2023-05-10 11:44:07
Description: 
'''
from Crypto.Cipher import DES
import binascii


def padding(strb: bytes):  # 补全8倍长度
    pad_len = 8 - len(strb) % 8
    padd = bytes([pad_len] * pad_len)
    resb = strb + padd
    return resb


def encry(strs: 'str|bytes', retType='b'):  # 加密
    if type(strs) == str:
        strb = bytes(strs.encode())
    elif type(strs) == bytes:
        strb = bytes(strs)
    else:
        print('[typeError]')
    strb = padding(strb)
    ciphertext = cipher.encrypt(strb)
    resb = ciphertext  # bytes->16进制
    if retType == 'b':
        return resb
    else:
        ress = str(binascii.hexlify(ciphertext))
        return ress


def decry(strb: bytes, retType='b'):  # 解密
    resb = cipher.decrypt(strb)
    if retType == 'b':
        return resb
    else:
        ress = str(resb)
        return ress


if __name__ == '__main__':
    key = b'secret_k'  # 初始密钥
    pltext = b'111100001111v001abcdufwk12341234'  # 明文数据
    print("明文: ", pltext, 'len:', len(pltext))

    cipher = DES.new(key, DES.MODE_ECB)  # 初始化加密器
    cptext = encry(pltext)  # 加密
    cptexth = binascii.hexlify(cptext)
    print("密文: ", cptexth, 'len:', len(cptexth))

    # decrypted = cipher.decrypt(cptext)  # 解密
    # dpltext = decrypted[:-decrypted[-1]]
    # print("解密后的明文: ", dpltext.decode())

    # 去除padding，并打印明文数据
    dcptext = decry(cptext)
    dpltext = dcptext[:-dcptext[-1]]
    print("解密后的明文: ", dpltext.decode())
