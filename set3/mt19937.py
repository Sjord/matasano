import time

(w, n, m, r) = (32, 624, 397, 31)
a = 0x9908B0DF
(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7, 0x9D2C5680)
(t, c) = (15, 0xEFC60000)
l = 18
f = 1812433253
w_mask = 0xFFFFFFFF
index = n


def w_trunc(number):
    return number & w_mask

x = []
def init(seed):
    global x, index
    x = [seed]
    for i in range(1, n):
        x.append(w_trunc(f * (x[i - 1] ^ (x[i - 1] >> (w - 2))) + i))
    index = n


def next_int():
    global index

    if index >= n:
        twist()

    y = x[index]
    y = y ^ ((y >> u) & d)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)

    index += 1
    return w_trunc(y)


def twist():
    global index

    lower_mask = (1 << r) - 1
    upper_mask = w_trunc(~lower_mask)
    for i in range(n):
        y = (x[i] & upper_mask) + (x[(i+1) % n] & lower_mask)
        yA = y >> 1
        if (y & 1):
            yA = yA ^ a
        x[i] = x[(i+m) % n] ^ yA
    index = 0


if __name__ == "__main__":
    init(int(time.time()))
    print(next_int())
