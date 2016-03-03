import os
from Crypto.Cipher import AES


with open('key.txt', 'rb') as fp:
    key = fp.read()

def pad(data):
    pad_length = 16 - len(data) % 16
    return data + bytearray(pad_length * [pad_length])


def wrap_user_data(input):
    data = b"comment1=cooking%20MCs;userdata=" + input + b";comment2=%20like%20a%20pound%20of%20bacon"
    data = pad(data)
    return encrypt(data)


def decrypt(input):
    assert len(key) == 16
    return AES.new(key, AES.MODE_CBC, IV=key).decrypt(input)


def encrypt(data):
    assert len(key) == 16
    return AES.new(key, AES.MODE_CBC, IV=key).encrypt(data)


encrypted = wrap_user_data(b'_admin_true_')
encrypted = bytearray(encrypted)
encrypted[16] ^= 100  # _ -> ;
encrypted[22] ^= 98   # _ -> =
encrypted[27] ^= 100  # _ -> ;
encrypted = bytes(encrypted)
print(decrypt(encrypted))
