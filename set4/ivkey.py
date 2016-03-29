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
    plain = AES.new(key, AES.MODE_CBC, IV=key).decrypt(input)
    try:
        return plain.decode('ascii')
    except UnicodeDecodeError:
        raise RuntimeError(plain)


def encrypt(data):
    assert len(key) == 16
    return AES.new(key, AES.MODE_CBC, IV=key).encrypt(data)


encrypted = wrap_user_data(b'a' * 16 * 3)
first_block = encrypted[0:16]
modified = first_block + b'\0' * 16 + first_block
try:
    print(decrypt(modified))
except RuntimeError as e:
    plain = e.args[0]
    p1 = plain[0:16]
    p3 = plain[32:48]
    iv = bytes([a ^ b for a, b in zip(p1, p3)])
    print(iv)
    assert key == iv
