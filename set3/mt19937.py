(w, n, m, r) = (64, 312, 156, 31)
a = 0xB5026F5AA96619E9
(u, d) = (29, 0x5555555555555555)
(s, b) = (17, 0x71D67FFFEDA60000)
(t, c) = (37, 0xFFF7EEE000000000)
l = 43
f = 6364136223846793005
w_mask = 0xFFFFFFFFFFFFFFFF
index = n

def w_trunc(number):
    return number & w_mask

x = []
def init(seed):
    x.append(seed)
    for i in range(1, n):
        x.append(w_trunc(f * (x[i - 1] ^ (x[i - 1] >> (w - 2))) + i))


def next():
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


init(12345)
for i in range(1000):
    print(next())
