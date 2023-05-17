'''
Author: Thoma411
Date: 2023-05-17 23:38:16
LastEditTime: 2023-05-18 00:21:00
Description: 
'''
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


def RSA_encry(PK, msg):  # RSA加密
    key = RSA.import_key(PK)
    cipherText = pow(msg, key.e, key.n)
    return cipherText


def RSA_decry(SK, cpText):  # RSA解密
    key = RSA.import_key(SK)
    dcpText = pow(cpText, key.d, key.n)
    return dcpText


def RSA_sign(SK, msg):  # 生成数字签名
    key = RSA.import_key(SK)
    h = SHA256.new(str(msg).encode('utf-8'))
    Sign = pkcs1_15.new(key).sign(h)
    return Sign


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
    RSA_verf(test_PK, msg, Sig)
