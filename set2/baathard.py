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


def oracle(data):
    data = random_prefix() + data + something
    return encrypt(data)

print(len(oracle(b'attacker controlled')))
