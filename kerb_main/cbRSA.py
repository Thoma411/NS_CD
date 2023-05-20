import random as rd
import hashlib as hs


def gcd(a, b):  # 求最大公约数
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


def power(a, b, c):  # 快速幂+取模
    ans = 1
    while b != 0:
        if b & 1:
            ans = (ans * a) % c
        b >>= 1
        a = (a * a) % c
    return ans


def quick_power(a: int, b: int) -> int:  # 快速幂
    ans = 1
    while b != 0:
        if b & 1:
            ans = ans * a
        b >>= 1
        a = a * a
    return ans


def Miller_Rabin(n):  # 大素数检测
    a = rd.randint(2, n - 2)  # 随机第选取一个a∈[2,n-2]
    # print("随机选取的a=%lld\n"%a)
    s = 0  # s为d中的因子2的幂次数。
    d = n - 1
    while (d & 1) == 0:  # 将d中因子2全部提取出来。
        s += 1
        d >>= 1
    x = power(a, d, n)
    for i in range(s):  # 进行s次二次探测
        newX = power(x, 2, n)
        if newX == 1 and x != 1 and x != n - 1:
            return False  # 用二次定理的逆否命题，此时n确定为合数。
        x = newX
    if x != 1:  # 用费马小定理的逆否命题判断，此时x=a^(n-1) (mod n)，那么n确定为合数。
        return False
    return True  # 用费马小定理的逆命题判断。能经受住考验至此的数，大概率为素数。


# 卢卡斯-莱墨素性检验
def Lucas_Lehmer(num: int) -> bool:  # 快速检验pow(2,m)-1是不是素数
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    s = 4
    Mersenne = pow(2, num) - 1  # pow(2, num)-1是梅森数
    for x in range(1, (num - 2) + 1):  # num-2是循环次数，+1表示右区间开
        s = ((s * s) - 2) % Mersenne
    if s == 0:
        return True
    else:
        return False


# 扩展的欧几里得算法，ab=1 (mod m), 得到a在模m下的乘法逆元b
def Extended_Eulid(a: int, m: int) -> int:
    def extended_eulid(a: int, m: int):
        if a == 0:  # 边界条件
            return 1, 0, m
        else:
            x, y, gcd = extended_eulid(m % a, a)  # 递归
            x, y = y, (x - (m // a) * y)  # 递推关系，左端为上层
            return x, y, gcd  # 返回第一层的计算结果。
        # 最终返回的y值即为b在模a下的乘法逆元
        # 若y为复数，则y+a为相应的正数逆元
    n = extended_eulid(a, m)
    if n[1] < 0:
        return n[1] + m
    else:
        return n[1]


def Generate_prime(key_size: int) -> int:  # 按照需要的bit来生成大素数
    while True:
        num = rd.randrange(quick_power(
            2, key_size - 1), quick_power(2, key_size))
        if Miller_Rabin(num):
            return num


def KeyGen(p: int, q: int):  # 生成公钥和私钥
    n = p * q
    e = rd.randint(1, (p - 1) * (q - 1))
    while gcd(e, (p - 1) * (q - 1)) != 1:
        e = rd.randint(1, (p - 1) * (q - 1))
    d = Extended_Eulid(e, (p - 1) * (q - 1))
    return n, e, d


def hash_string(message):
    sha256 = hs.sha256()
    sha256.update(message.encode('utf-8'))
    return int(sha256.hexdigest(), 16)


def RSA_sign(message: str, d: int, n: int) -> int:
    x = hash_string(message)
    s = power(x, d, n)
    return s


def RSA_verf(message: str, s: int, e: int, n: int) -> bool:
    x_ = hash_string(message)
    x_verified = power(s, e, n)
    return x_ == x_verified


if __name__ == '__main__':
    key_size = 128
    p = Generate_prime(key_size)
    q = Generate_prime(key_size)
    n, e, d = KeyGen(p, q)

    # 消息
    inputMsg = '\{123cs4\}'
    sig = RSA_sign(inputMsg, d, n)
    print("Signature:", sig)

    testMsg = '\{123cs4\}'
    is_verified = RSA_verf(inputMsg, sig, e, n)
    print("Verification result:", is_verified)

    # Output
    print("Private Key: ")
    print("N: ", n)
    print("d: ", d)
    print("Public Key: ")
    print("N: ", n)
    print("e: ", e)
    print("Signature: ")
    print("s: ", sig)
    print("Verify s of m: ")
    if is_verified:
        print("valid")
    else:
        print("invalid")
