from Crypto.Cipher import AES
import os


def pad(message):
    pad_bytes = 16 - len(message) % 16
    return message + bytes([pad_bytes] * pad_bytes)


def blocks(message):
    for i in range(len(message) // 16):
        yield message[i * 16:(i + 1) * 16]


def C(block, H):
    key = H.to_bytes(16, 'big')
    aes = AES.new(key, AES.MODE_ECB)
    cipher = aes.encrypt(block)
    cipher_num = int.from_bytes(cipher, 'big')
    return cipher_num % 0xffff


def expensiveC(block, H):
    key = H.to_bytes(24, 'big')
    aes = AES.new(key, AES.MODE_CBC, IV=b'\0' * 16)
    cipher = aes.encrypt(block)
    cipher_num = int.from_bytes(cipher, 'big')
    return cipher_num % 0xffffff


def expensiveMD(message):
    H = 0xde9812
    for block in blocks(pad(message)):
        H = C(block, H)
    return H


def MD(message):
    H = 0x3fe4
    for block in blocks(pad(message)):
        H = C(block, H)
    return H


def f(n):
    collisions = []
    hashes = {}
    while len(collisions) < 2**n:
        message = os.urandom(2+n)
        hash = MD(message)
        if hash in hashes and hashes[hash] != message:
            collisions.append((message, hashes[hash]))
        else:
            hashes[hash] = message
    return collisions


def find_double_collisions():
    while True:
        cheap_candidates = f(10)
        for m1, m2 in cheap_candidates:
            if expensiveMD(m1) == expensiveMD(m2):
                print(m1, m2)
                return


if __name__ == "__main__":
    find_double_collisions()
