from random import randrange

p = 27
g = 5
n = 37

a = randrange(0, n)
A = (g ** a) % n

b = randrange(0, n)
B = (g ** b) % n
print(A, B)

sa = (B ** a) % n
sb = (A ** b) % n
assert sa == sb
