import os
from base64 import b64decode
from Crypto.Cipher import AES
import random

strings = [
    b'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
    b'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
    b'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
    b'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
    b'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
    b'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
    b'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
    b'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
    b'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
    b'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93',
]

def pad(data):
    pad_length = 16 - len(data) % 16
    return data + bytearray(pad_length * [pad_length])

def validate_padding(data):
    pad_length = data[-1]
    if pad_length == 0 or pad_length > 16:
        return False
    for i in range(pad_length):
        if data[-i-1] != pad_length:
            return False
    return True

def encrypt():
    data = b64decode(strings[0])  # random.choice(strings))
    with open('key.txt', 'rb') as fp:
        key = fp.read()
    assert len(key) == 16
    iv = os.urandom(16)
    assert len(iv) == 16
    ciphertext = AES.new(key, AES.MODE_CBC, IV=iv).encrypt(pad(data))
    return (iv, ciphertext)

def valid_padding(iv, ciphertext):
    with open('key.txt', 'rb') as fp:
        key = fp.read()
    assert len(key) == 16
    assert len(iv) == 16
    plain = AES.new(key, AES.MODE_CBC, IV=iv).decrypt(ciphertext)
    return validate_padding(plain)

assert valid_padding(*encrypt())


iv, ciphertext = encrypt()
first_block = ciphertext[0:16]
second_block = ciphertext[16:32]
some_block = bytearray(b'\0' * 16)
for i in range(256):
    some_block[-1] = i
    attempt = some_block + second_block
    if valid_padding(iv, bytes(attempt)):
        print(i ^ first_block[-1] ^ 1)
