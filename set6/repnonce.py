from dsa import modinv, q, sign_hash
import hashlib


messages = []
with open('44.txt') as fp:
    message = {}
    for line in fp:
        (key, value) = line.split(': ')
        value = value.strip('\n')
        if key in ('s', 'r'):
            value = int(value)
        if key == 'msg':
            value = value.encode('ascii')
        if key == 'm':
            value = int(value, 16)
        message[key] = value
        if key == 'm':
            messages.append(message)
            message = {}
                    
y = 0x2d026f4bf30195ede3a088da85e398ef869611d0f68f0713d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b85519b1c23cc3ecdc6062650462e3063bd179c2a6581519f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d32971c3de5084cce04a2e147821

def reused_k(m1, s1, m2, s2, q):
    sm = (s1 - s2) % q
    mm = (m1 - m2) % q
    k = modinv(sm, q) * mm
    return k % q


assert reused_k(1, 1, 0, 0, 7) == 1
assert reused_k(8, 1, 0, 0, 7) == 1
assert reused_k(0, 1, 6, 0, 7) == 1


for m1 in messages:
    for m2 in messages:
        if m1 is m2:
            continue
        k = reused_k(m1['m'], m1['s'], m2['m'], m2['s'], q)
        if k == 0:
            continue
        x = (((m1['s'] * k) - m1['m']) * modinv(m1['r'], q)) % q
        r, s = sign_hash(m1['m'], x, k, q)
        if r == m1['r'] and s == m1['s']:
            print(x)
            break


assert hashlib.sha1(hex(x)[2:].encode('ascii')).hexdigest() == 'ca8f6f7c66fa362d40760d135b763eb8527d3d52'
