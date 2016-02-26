from base64 import b64decode
from Crypto.Cipher import AES
import os
from random import randint

something = b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")


def pad(data):
    pad_length = 16 - len(data) % 16
    return data + bytearray(pad_length * [pad_length])


def encrypt(data):
    with open('key.txt', 'rb') as fp:
        key = fp.read()
    assert len(key) == 16
    return AES.new(key, AES.MODE_ECB).encrypt(pad(data))

def random_prefix():
    byte_count = randint(16, 64)
    return os.urandom(byte_count)


prefix = random_prefix()
def oracle(data):
    data = prefix + data + something
    return encrypt(data)

def blocks(data, blocksize=16):
    for i in range(int(len(data) / blocksize)):
        yield data[i*blocksize:(i+1)*blocksize]

encrypted_as = oracle(b'a' * 1000)
blocks = list(blocks(encrypted_as))
a_block = max(blocks, key=blocks.count)

for i in range(1, 100):
    ciphertext = oracle(b'a' * i)
    if a_block in ciphertext:
        random_length = ciphertext.index(a_block) - i + 16
        print(random_length)
        break

length = 192 + random_length
message = b'a' * 192
decoded = b''

while True:
    message = message[1:]
    target = oracle(message)[0:length]
    for i in range(255):
        ciphertext = oracle(message + decoded + bytearray([i]))
        if ciphertext[0:length] == target:
            decoded += bytearray([i])
            print(decoded)
            break
    else:
        print("done")
        break
