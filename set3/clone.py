
(w, n, m, r) = (32, 624, 397, 31)
a = 0x9908B0DF
(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7, 0x9D2C5680)
(t, c) = (15, 0xEFC60000)
l = 18
f = 1812433253
w_mask = 0xFFFFFFFF
index = n



def undo_left_shift(y, s, b=w_mask):
    # Rightmost s bits are correct
    result = 0
    for i in range(w):
        bit = y & 1 << i
        xor_value = result << s
        xor_bit = xor_value & 1 << i
        result_bit = bit ^ (xor_bit & b)
        result |= result_bit
    return result


def undo_right_shift(y, s, b=w_mask):
    # Leftmost s bits are correct
    result = 0
    for i in range(w - 1, -1, -1):
        bit = y & 1 << i
        xor_value = result >> s
        xor_bit = xor_value & 1 << i
        result_bit = bit ^ (xor_bit & b)
        result |= result_bit
    return result




def rand_to_state(y):
    y = undo_right_shift(y, l)
    y = undo_left_shift(y, t, c)
    y = undo_left_shift(y, s, b)
    y = undo_right_shift(y, u, d)
    return y


def state_to_rand(y):
    y = y ^ ((y >> u) & d)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)
    return y



def back_forth(orig):
    rand = state_to_rand(orig)
    back = rand_to_state(rand)
    print(orig, rand, back, orig == back)


back_forth(1 << 20)
back_forth(0x55555555)
back_forth(0xDEADBEAF)
back_forth(0x12345678)
back_forth(1)
back_forth(1 << 31)

y = 0xDEADBEEF
print("{0:64b} y".format(y))
print("{0:64b} y << s".format(y << s))
print("{0:64b} b".format(b))
print("{0:64b} y << s & b".format((y << s) & b))
print("{0:64b} y ^ y << s & b".format(y ^ ((y << s) & b)))
print()
y = y ^ ((y << s) & b)
print("{0:64b} y".format(y))
print("{0:64b} y << s".format(y << s))
print("{0:64b} b".format(b))
print("{0:64b} y & b".format(y & b))
print("{0:64b} y << s & b".format((y << s) & b))
print("{0:64b} y ^ y << s & b".format(y ^ ((y << s) & b)))
print()

print("{0:64b} y".format(y))
y = y ^ ((y << s) & b)
print("{0:64b} y".format(y))
y = undo_left_shift(y, s, b)
print("{0:64b} y".format(y))
