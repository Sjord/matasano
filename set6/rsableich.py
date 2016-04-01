from base64 import b64decode 
from math import floor, ceil

e = 3
n = 102475686917025296766570439272120624752510811998694234970181967099024303462967
d = 68317124611350197844380292848080416501246442637454958102623396449974256861051 
bsize = 32

msg = b'kick it, CC'

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def is_conforming(cipher_num):
    plain_num = pow(cipher_num, d, n)
    plain = plain_num.to_bytes(bsize, 'big')
    return plain.startswith(b'\0\2')

def multiply(s, cipher_num):
    return (s ** e * cipher_num) % n

def pad(msg_num):
    msg = msg_num.to_bytes(bsize, 'big')
    msg = b'\0\2' + msg[2:]
    return int.from_bytes(msg, 'big')

def step2c(M, s):
    # 2c
    print(M)
    a, b = M

    r = ceil(2 * ((b * s - 2 * B) / n))
    assert r >= 2*((b * s - 2 * B) / n)

    while True:
        low_s = ceil((2 * B + r * n) / b)
        high_s = ceil((3 * B + r * n) / a)

        for s_attempt in range(low_s, high_s):
            assert s_attempt < (3 * B + r * n) / a
            assert s_attempt >= (2 * B + r * n) / b

            if is_conforming(multiply(s_attempt, cipher_num)):
                return r, s_attempt
        r += 1


def step3(M, s):
    a, b = M
    low_r = ceil((a * s - 3 * B + 1) / n)
    high_r = floor((b * s - 2 * B) / n)

    for r in range(low_r, 1 + high_r):
        a, b = (max(a, ceil((2 * B + r * n) / s)), min(b, floor((3 * B - 1 + r * n) / s)))

    return (a, b)


def step2a():
    s = ceil(n / (3 * B))
    assert s >= n / (3 * B)

    while True:
        if is_conforming(multiply(s, cipher_num)):
            return s
        s += 1


msg_num = int.from_bytes(msg, 'big')
msg_num = pad(msg_num)
cipher_num = pow(msg_num, e, n)

assert is_conforming(cipher_num)

B = 1 << (bsize * 8 - 16)
M = (2*B, 3*B-1)

# 2a
s = step2a()
assert s

M = step3(M, s)

while M[0] < M[1]:
    # 2c
    r, s = step2c(M, s)

    assert s >= (2 * B + r * n) / M[1]
    assert s < (3 * B + r * n) / M[0]

    # 3
    M = step3(M, s)

plain_num = M[0]
print(plain_num.to_bytes(bsize, 'big'))
