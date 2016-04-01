


e = 3 
n = 90587157434501026549952310384970631951370855552491309829786573238506360478351
d = 60391438289667351033301540256647087967178072160209458029332904639264889982075
bsize = 32

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
