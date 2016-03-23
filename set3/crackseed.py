from mt19937 import init, next_int
import time

random = 1853705539
i = int(time.time())
while True:
    init(i)
    if random == next_int():
        print(i)
        break
    i -= 1
