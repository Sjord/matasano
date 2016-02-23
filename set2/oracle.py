import os
from random import randrange, choice
from Crypto.Cipher import AES


def generate_random_aes_key():
    return os.urandom(16)

def random_bytes():
    len = randrange(5, 10)
    return bytearray(len * [len])

def encryption_oracle(data):
    data = random_bytes() + data + random_bytes()
    pad = 16 - len(data) % 16
    data += bytearray([pad]) * pad
    mode = choice([AES.MODE_ECB, AES.MODE_CBC])
    key = generate_random_aes_key()
    iv = generate_random_aes_key()
    return AES.new(key, mode, IV=iv).encrypt(bytes(data))

def is_ebc(data):
    return data[16:32] == data[32:48]


print(is_ebc(encryption_oracle(b'\0' * 100)))
