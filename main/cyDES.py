'''
Author: Thoma411
Date: 2023-05-09 11:23:42
LastEditTime: 2023-05-14 22:08:16
Description: 
'''
from Crypto.Cipher import DES
import binascii


def padding(strb: bytes):  # 补全8倍长度
    pad_len = 8 - len(strb) % 8
    padd = bytes([pad_len] * pad_len)
    resb = strb + padd
    return resb


def DES_encry(strs: 'str|bytes', key: 'str|bytes', retType='b'):  # DES加密
    if type(strs) == str:
        strb = bytes(strs.encode())
    elif type(strs) == bytes:
        strb = bytes(strs)
    else:
        print('[typeError] strs')
    if type(key) == str:
        keyb = bytes(key.encode())
    elif type(key) == bytes:
        keyb = bytes(key)
    else:
        print('[typeError] key')
    strb = padding(strb)
    cipher = DES.new(keyb, DES.MODE_ECB)  # 初始化加密器
    ciphertext = cipher.encrypt(strb)
    resb = ciphertext  # bytes->16进制
    if retType == 'b':  # 默认返回bytes
        return resb
    else:
        ress = str(binascii.hexlify(ciphertext))
        return ress


def DES_decry(strb: bytes, key: 'str|bytes', retType='b'):  # DES解密
    if type(key) == str:
        keyb = bytes(key.encode())
    elif type(key) == bytes:
        keyb = bytes(key)
    else:
        print('[typeError] key')
    cipher = DES.new(keyb, DES.MODE_ECB)  # 初始化加密器
    resb = cipher.decrypt(strb)
    if retType == 'b':  # 默认返回bytes
        return resb
    else:
        ress = str(resb)
        return ress


if __name__ == '__main__':
    key = b'secret_1'  # 初始密钥
    pltext = b'111100001111v001abcdufwk12341284'  # 明文数据
    print("明文: ", pltext, 'len:', len(pltext))

    # cipher = DES.new(key, DES.MODE_ECB)  # 初始化加密器
    cptext = DES_encry(pltext, key)  # 加密
    cptexth = binascii.hexlify(cptext)
    print("密文: ", cptexth, 'len:', len(cptexth))
    print('密文(未转16进制): ', cptext, 'len:', len(cptext))

    # decrypted = cipher.decrypt(cptext)  # 解密
    # dpltext = decrypted[:-decrypted[-1]]
    # print("解密后的明文: ", dpltext.decode())

    # 去除padding，并打印明文数据
    dcptext = DES_decry(cptext, key)
    dpltext = dcptext[:-dcptext[-1]]
    print("解密后的明文: ", dpltext.decode())
