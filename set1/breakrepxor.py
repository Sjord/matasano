from __future__ import division
import base64

def distance(a, b):
    assert len(a) == len(b)
    count = 0;
    for i in range(len(a)):
        differences = ord(a[i]) ^ ord(b[i])
        count += bin(differences).count('1')
    return count


def key_distance(encrypted, i):
    a = encrypted[0:i]
    b = encrypted[i:2*i]
    dist = distance(a, b)
    return dist / i


assert distance('this is a test', 'wokka wokka!!!') == 37

def guess_key_size(encrypted):
    return min(range(2, 100), key=lambda i: key_distance(encrypted, i))


with open('6.txt') as fp:
    encoded = fp.read()
    encrypted = base64.b64decode(encoded)
    print(guess_key_size(encrypted))
