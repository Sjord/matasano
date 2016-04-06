import struct
import os
from md4 import md4, F
from binascii import hexlify

def get_bit(n, bitnum):
    return (n & (1 << bitnum - 1)) >> bitnum - 1

def xor(a, b):
    return bytes([ca ^ cb for ca, cb in zip(a, b)])

def smd4(msg):
    m = md4()
    m.update(msg)
    return m.hexdigest()

def check_weak_message(message):
    m = md4()
    m.update(message)
    a, b, c, d = m.intermediates

    assert get_bit(a[1], 7) == get_bit(b[0], 7)
    assert get_bit(d[1], 7) == 0
    return
    assert get_bit(d[1], 8) == get_bit(a[1], 8)
    assert get_bit(d[1], 11) == get_bit(a[1], 11)
    assert get_bit(c[1], 7) == 1
    assert get_bit(c[1], 8) == 1
    assert get_bit(c[1], 11) == 0
    assert get_bit(c[1], 26) == get_bit(d[1], 26)
    assert get_bit(b[1], 7) == 1
    assert get_bit(b[1], 8) == 0
    assert get_bit(b[1], 11) == 0
    assert get_bit(b[1], 26) == 0

def xor_bit(a, b, bitnum):
    return (get_bit(a, bitnum) ^ get_bit(b, bitnum)) << (bitnum - 1)

def message_numbers(message):
    return list(struct.unpack("<16i", message))

def numbers_to_message(mnumbers):
    assert len(mnumbers) == 16
    return struct.pack("<16I", *mnumbers)

def make_weak_message(message):
    md = md4()
    md.update(message)
    a, b, c, d = md.intermediates

    m = message_numbers(message)

    # a17 = b07
    a[1] ^= xor_bit(a[1], b[0], 7)
    assert get_bit(a[1], 7) == get_bit(b[0], 7)
    m[0] = ror(a[1], 3) - a[0] - F(b[0], c[0], d[0])
    m[0] = m[0] & 0xffffffff

    assert a[1] == rol(a[0] + F(b[0], c[0], d[0]) + m[0], 3)
    assert get_bit(a[1], 7) == get_bit(b[0], 7)

    # d17 = 0
    d[1] ^= get_bit(d[1], 7) << 6
    
    return numbers_to_message(m)

def to_bytes(n):
    n %= 0xffffffff
    return n.to_bytes(4, 'big')


def rol(v, bits):
    v = v & 0xffffffff
    return ((v << bits) | (v >> 32-bits)) & 0xffffffff

assert get_bit(1, 1) == 1
assert get_bit(2, 1) == 0
assert get_bit(2, 2) == 1

assert xor_bit(1, 1, 1) == 0
assert xor_bit(2, 2, 2) == 0
assert xor_bit(1, 2, 2) == 2

assert ror(0xdeadbeef, 4) == 0xfdeadbee
assert rol(0xdeadbeef, 4) == 0xeadbeefd

assert numbers_to_message(message_numbers(b'test' * 16)) == b'test' * 16

message = os.urandom(64)
m = md4()
m.update(message)

a, b, c, d = m.intermediates

assert a[0] == 0x67452301
assert b[0] == 0xefcdab89
assert c[0] == 0x98badcfe
assert d[0] == 0x10325476

assert len(message) == 64

weakened = make_weak_message(message)
print(hexlify(message))
print(hexlify(weakened))
check_weak_message(weakened)

