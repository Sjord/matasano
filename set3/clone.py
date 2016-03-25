from mt19937 import Random

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


seed = 22131
orig = Random(seed)
clone = Random(0)

for i in range(624):
    output = orig.next_int()
    state = rand_to_state(output)
    clone.x[i] = state

for i in range(100):
    print orig.next_int(), clone.next_int()
