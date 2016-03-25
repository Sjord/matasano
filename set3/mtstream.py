from mt19937 import Random
from random import randrange

def stream(seed):
    seed = seed & 0xffff  # 16-bit seed
    rand = Random(seed)
    while True:
        yield rand.next_int() & 0xff

def encrypt(seed, plain):
    result = []
    for p, s in zip(plain, stream(seed)):
        result.append(p ^ s)
    return bytes(result)

def random_prefix():
    result = []
    for i in range(randrange(5, 15)):
        result.append(randrange(0, 256))
    return bytes(result)


cipher = encrypt(1234, random_prefix() + b'a' * 14)
print(encrypt(1234, cipher))
