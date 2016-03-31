import hashlib
from random import randrange

p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1

q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b

g = 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291

x = randrange(1, q)
y = pow(g, x, p)


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

def sha1num(msg):
    return int.from_bytes(hashlib.sha1(msg).digest(), 'big')


def sign(msg, x, k=None):
    hash = sha1num(msg)
    s = 0
    while s == 0:
        r = 0
        while r == 0:
            if k is None:
                k = randrange(1, q)
            r = pow(g, k, p) % q
        s = (modinv(k, q) * (hash + x * r)) % q
    return (r, s)
 
 
def verify(msg, signature):
    r, s = signature
    assert 0 < r < q
    assert 0 < s < q
    w = modinv(s, q)
    u1 = (sha1num(msg) * w) % q
    u2 = (r * w) % q
    v = (pow(g, u1, p) * pow(y, u2, p)) % p % q
    return v == r


def private_key_from_k(k, msg, signature):
    r, s = signature
    hash = sha1num(msg)
    x = ((s * k) - hash) * modinv(r, q)
    return x % q



msg = b'hi mom'

k = randrange(1, q)
signature = sign(msg, x, k)
print(verify(msg, signature))

msg = b'For those that envy a MC it can be hazardous to your health\nSo be friendly, a matter of life and death, just like a etch-a-sketch\n'
assert sha1num(msg) == 0xd2d0714f014a9784047eaeccf956520045c45265
r = 548099063082341131477253921760299949438196259240
s = 857042759984254168557880549501802188789837994940
signature = (r, s)

for k in range(1, 2 ** 16):
    x = private_key_from_k(k, msg, signature)
    signature_for_k = sign(msg, x, k)
    if signature_for_k == signature:
        print(x)
        break

assert hashlib.sha1(hex(x)[2:].encode('ascii')).hexdigest() == '0954edd5e0afe5542a4adf012611a91912a3ec16'
