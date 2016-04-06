import struct
from md4 import md4, F, G
from random import randrange

# Chaining variables
# Conditions on bits
# 31 - 0
bmap = [b'-' * 32] * 48
bmap[1]  = '10------a-------------a-a---a-01'
bmap[2]  = '10-0-a------0-------a-1-0-----01'
bmap[3]  = '11-1a-a00-aa1-aaaaaa1a0-0---1-10'
bmap[4]  = '1-a-1011aa100-011111011a1aaaa---'
bmap[5]  = 'a---000011000a100000000111111---'
bmap[6]  = '0-0-1-11111100111111-10000000aa-'
bmap[7]  = '0-1---1100-010--------011111111-'
bmap[8]  = '1-----a000-101-----0--000000100-'
bmap[9]  = '0aa-aa0101---------a--111101111-'
bmap[10] = '011-100-11---a-----1-00---------'
bmap[11] = '000-110-11---------0-11---------'
bmap[12] = '011a001------1-----1-10---------'
bmap[13] = '--10--0------1-----0-00---------'
bmap[14] = '--00--0-----a------0-11---------'
bmap[15] = 'a-11b-1--------b----------------'
bmap[16] = '1--a0-------c-------------------'
bmap[17] = 'b--0--------a-------------------'
bmap[18] = 'b--c----------------------------'
bmap[19] = '---a----------------------------'
bmap[20] = 'a-------------------------------'
bmap[21] = '0--------b----------------------'
bmap[22] = 'c-------------------------------'
bmap[23] = 'a-------------------------------'
bmap[24] = '--------------------------------'
bmap[33] = '0-------------------------------'

def md4hex(message):
    md = md4()
    md.update(message)
    return md.hexdigest()

def H(x,y,z):
    return x ^ y ^ z

def ror(v, bits):
    v = v & 0xffffffff
    return ((v >> bits) | (v << 32-bits)) & 0xffffffff

def rol(v, bits):
    v = v & 0xffffffff
    return ((v << bits) | (v >> 32-bits)) & 0xffffffff

def clear_bit(n, bitnum):
    bit = 1 << bitnum
    return n & ~bit

def set_bit(n, bitnum):
    bit = 1 << bitnum
    return n | bit

def copy_bit(n, from_, bitnum):
    mask = 1 << bitnum
    bit = from_ & mask
    return (n & ~mask) | bit

def change_b(new_b, old_b, i):
    bitmap = bmap[i]
    for bitnum in range(32):
        condition = bitmap[31-bitnum]
        if condition == '0':
            new_b = clear_bit(new_b, bitnum)
        if condition == '1':
            new_b = set_bit(new_b, bitnum)
        if condition == 'a':
            new_b = copy_bit(new_b, old_b, bitnum)
    return new_b

def has_conditions(new_b, old_b, i):
    bitmap = bmap[i]
    match = True
    for bitnum in range(32):
        condition = bitmap[31-bitnum]
        if condition == '0':
            match = (new_b & 1 << bitnum) == 0
        if condition == '1':
            match = (new_b & 1 << bitnum) != 0
        if condition == 'a':
            match = (new_b & 1 << bitnum) == (old_b & 1 << bitnum)
        if not match:
            return False
    return True

def numbers_to_message(mnumbers):
    assert len(mnumbers) == 16
    return struct.pack("<16I", *mnumbers)

def message_numbers(message):
    return list(struct.unpack("<16i", message))

assert ror(0xdeadbeef, 4) == 0xfdeadbee
assert rol(0xdeadbeef, 4) == 0xeadbeefd
assert set_bit(0, 0) == 1
assert clear_bit(1, 0) == 0
assert copy_bit(0, 1, 0) == 1
assert numbers_to_message(message_numbers(b'test' * 16)) == b'test' * 16
assert has_conditions(0b10101011111000011111011111111000, 0b00100000110000000000000101111000, 4)

def find_collision():
    a = [0x67452301]
    b = [0xefcdab89]
    c = [0x98badcfe]
    d = [0x10325476]
    m = []

    # Round 1
    for i in range(1, 17):
        s = md4._round1[i-1][-1]
        k = md4._round1[i-1][-2]
        t = 0

        new_b = randrange(0xffffffff)
        new_b = change_b(new_b, b[i-1], i)
        m.append((ror(new_b, s) - a[i-1] - F(b[i-1], c[i-1], d[i-1])) & 0xffffffff)

        assert has_conditions(new_b, b[i-1], i)
        assert new_b == rol(a[i-1] + F(b[i-1], c[i-1], d[i-1]) + m[k] + t, s)

        a.append(d[i-1])
        b.append(new_b)
        c.append(b[i-1])
        d.append(c[i-1])

    # Round 2
    for i in range(17, 33):
        s = md4._round2[i-17][-1]
        k = md4._round2[i-17][-2]
        t = 0x5a827999

        new_b = rol(a[i-1] + G(b[i-1], c[i-1], d[i-1]) + m[k] + t, s)
        a.append(d[i-1])
        b.append(new_b)
        c.append(b[i-1])
        d.append(c[i-1])

    # Round 3   
    for i in range(33, 49):
        s = md4._round3[i-33][-1]
        k = md4._round3[i-33][-2]
        t = 0x6ed9eba1

        new_b = rol(a[i-1] + H(b[i-1], c[i-1], d[i-1]) + m[k] + t, s)
        a.append(d[i-1])
        b.append(new_b)
        c.append(b[i-1])
        d.append(c[i-1])

    m_col = list(m)
    m_col[0] = (m_col[0] + 2**28) & 0xffffffff
    m_col[2] = (m_col[2] + 2**31) & 0xffffffff
    m_col[4] = (m_col[4] + 2**31) & 0xffffffff
    m_col[8] = (m_col[8] + 2**31) & 0xffffffff
    m_col[12] = (m_col[12] + 2**31) & 0xffffffff

    message = numbers_to_message(m)
    col_message = numbers_to_message(m_col)
    return message, col_message

while True:
    message, col_message = find_collision()
    if md4hex(message) == md4hex(col_message):
        print(md4hex(message), message)
        print(md4hex(col_message), col_message)
        break
