'''
Author: Thoma411
Date: 2023-05-17 23:38:16
LastEditTime: 2023-05-18 14:43:19
Description: 
'''
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import binascii as ba


def RSA_encry(PK, msg):  # RSA加密
    key = RSA.import_key(PK)
    cipherText = pow(msg, key.e, key.n)
    return cipherText


def RSA_decry(SK, cpText):  # RSA解密
    key = RSA.import_key(SK)
    dcpText = pow(cpText, key.d, key.n)
    return dcpText


def RSA_sign(SK, msg, retType='b'):  # 生成数字签名
    key = RSA.import_key(SK)
    h = SHA256.new(str(msg).encode('utf-8'))
    bSign = pkcs1_15.new(key).sign(h)
    if retType == 'b':
        return bSign
    elif retType == 'h':
        hSign = ba.hexlify(Sig)
        return hSign
    elif retType == 's':
        hSign = ba.hexlify(Sig)
        return str(hSign)
    else:
        print('[Func: RSA_sign] no such retType.')


def RSA_verf(PK, msg, Sign):  # 验证数字签名
    key = RSA.import_key(PK)
    h = SHA256.new(str(msg).encode('utf-8'))
    try:
        pkcs1_15.new(key).verify(h, Sign)
        print("Signature is valid.")
    except (ValueError, TypeError):
        print("Signature is invalid.")


if __name__ == '__main__':
    key = RSA.generate(1024)  # 生成RSA密钥对
    test_SK = key.export_key()
    test_PK = key.publickey().export_key()

    msg = 'Hello, World!:|?>}{'
    cpMsg = RSA_encry(test_PK, int.from_bytes(msg.encode(), 'big'))
    dcpMsg = RSA_decry(test_SK, cpMsg)

    Sig = RSA_sign(test_SK, msg)
    print(Sig)
    hsig = ba.hexlify(Sig)
    print(hsig)
    print(str(hsig))
    RSA_verf(test_PK, msg, Sig)
