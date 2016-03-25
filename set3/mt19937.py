import time

(w, n, m, r) = (32, 624, 397, 31)
a = 0x9908B0DF
(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7, 0x9D2C5680)
(t, c) = (15, 0xEFC60000)
l = 18
f = 1812433253
w_mask = 0xFFFFFFFF

def w_trunc(number):
    return number & w_mask


class Random:
    def __init__(self, seed):
        self.x = [seed]
        for i in range(1, n):
            self.x.append(w_trunc(f * (self.x[i - 1] ^ (self.x[i - 1] >> (w - 2))) + i))
        self.index = n

    def next_int(self):
        if self.index >= n:
            self.twist()

        y = self.x[self.index]
        y = y ^ ((y >> u) & d)
        y = y ^ ((y << s) & b)
        y = y ^ ((y << t) & c)
        y = y ^ (y >> l)

        self.index += 1
        return w_trunc(y)

    def twist(self):
        lower_mask = (1 << r) - 1
        upper_mask = w_trunc(~lower_mask)
        for i in range(n):
            y = (self.x[i] & upper_mask) + (self.x[(i+1) % n] & lower_mask)
            yA = y >> 1
            if (y & 1):
                yA = yA ^ a
            self.x[i] = self.x[(i+m) % n] ^ yA
        self.index = 0


if __name__ == "__main__":
    random = Random(1)
    for i in range(10):
        print(random.next_int())

# 1791095845
# 4282876139
# 3093770124
# 4005303368
# 491263
# 550290313
# 1298508491
# 4290846341
# 630311759
# 1013994432
        
