e = 3 
n = 988582109822018694814510067699057031875575406574761089951324280216712816399100991004017126071521290194351458696434954341224967003274948343908614966095049387052788153628746155553156891135889531591539269628966927867972783839138373009
d = 659054739881345796543006711799371354583716937716507393300882853477808544266067327336011417381014193462900972464289927629356610192681107857114800225369758972227458114694576351389360043609116081119091634932201874331684643985681792803 
bsize = 96

msg = b'kick it, CC'

def is_padded(cipher_num):
    plain_num = pow(cipher_num, d, n)
    plain = plain_num.to_bytes(bsize, 'big')
    return plain.startswith(b'\0\2')


padded = b'\0\2' + b'\0' * (bsize - 2 - len(msg)) + msg
assert len(padded) == bsize

msg_num = int.from_bytes(padded, 'big')
cipher_num = pow(msg_num, e, n)
assert is_padded(cipher_num)


B = pow(2, 8 * (bsize - 2))

def divceil(a, b):
    res = a // b
    if a % b:
        res += 1
    return res

def divfloor(a, b):
    return a // b

def step2a():
    s = divceil(n, (3*B))
    while True:
        if is_padded(cipher_num * s ** e % n):
            return s

        s += 1


def step2b(s):
    while True:
        s += 1   
        if is_padded(cipher_num * s ** e % n):
            return s


def step2c(s, M):
    assert len(M) == 1
    (a, b), = M

    low_r = divceil(2 * b * s - 2 * B, n)
    r = low_r
    
    while True:
        low_s = divfloor(2 * B + r * n, b)
        high_s = divceil(3 * B + r * n, a)

        for s in range(low_s, high_s):
            if is_padded(cipher_num * s ** e % n):
                return s
        
        r += 1


def step3(s, M):
    new_M = set()

    for a, b in M:
        low_r = divceil(a * s - 3 * B + 1, n)
        high_r = divfloor(b * s - 2 * B, n)

        for r in range(low_r, 1 + high_r):
            new_a = max(a, divceil(2 * B + r * n, s))
            new_b = min(b, divfloor(3 * B - 1 + r * n, s))
            new_M.add((new_a, new_b))

    return new_M

def has_solution(M):
    if len(M) > 1:
        return False
    (a, b), = M
    return a == b


M = {(2 * B, 3 * B - 1)}
s = step2a()
M = step3(s, M)

while not has_solution(M):
    if len(M) > 1:
        s = step2b(s)
    else:
        s = step2c(s, M)

    M = step3(s, M)

    if len(M) == 1:
        (a, b), = M
        print(b.to_bytes(bsize, 'big'))
