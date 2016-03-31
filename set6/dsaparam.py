import hashlib
from random import randrange
from dsa import sha1num, modinv


class DSA:
    def __init__(self, p, q, g):
        self.p = p
        self.q = q
        self.g = g

    def create_keys(self):
        x = randrange(1, self.q)
        y = pow(self.g, x, self.p)
        return (x, y)

    def sign(self, msg, x):
        hash = sha1num(msg)
        return self.sign_hash(hash, x)

    def sign_hash(self, hash, x):
        s = 0
        while s == 0:
            r = 0
            # while r == 0:
            if True:
                k = randrange(1, self.q)
                r = pow(self.g, k, self.p) % self.q
            s = (modinv(k, self.q) * (hash + x * r)) % self.q
        return (r, s)
     
    def verify(self, msg, signature, y):
        r, s = signature
        # assert 0 < r < self.q
        assert 0 < s < self.q
        w = modinv(s, self.q)
        u1 = (sha1num(msg) * w) % self.q
        u2 = (r * w) % self.q
        v = (pow(self.g, u1, self.p) * pow(y, u2, self.p)) % self.p % self.q
        return v == r




default_p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1

default_q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b

default_g = 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291

dsa = DSA(default_p, default_q, default_g)
private, public = dsa.create_keys()

zero_dsa = DSA(default_p, default_q, 0)
signature = zero_dsa.sign(b'hello world', private)
assert zero_dsa.verify(b'hello world', signature, public)
assert zero_dsa.verify(b'other message', signature, public)
