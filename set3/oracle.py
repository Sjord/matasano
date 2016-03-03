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
    for i in range(pad_length):
        if data[-i-1] != pad_length:
            return False
    return True

def encrypt():
    data = b64decode(random.choice(strings))
    with open('key.txt', 'rb') as fp:
        key = fp.read()
    assert len(key) == 16
    iv = os.urandom(16)
    ciphertext = AES.new(key, AES.MODE_CBC, IV=iv).encrypt(pad(data))
    return (iv, ciphertext)

def valid_padding(iv, ciphertext):
    with open('key.txt', 'rb') as fp:
        key = fp.read()
    plain = AES.new(key, AES.MODE_CBC, IV=iv).decrypt(ciphertext)
    return validate_padding(plain)

assert valid_padding(*encrypt())


iv, ciphertext = encrypt()
first_block = ciphertext[0:16]
some_block = bytearray(b'0' * 16)
for i in range(256):
    some_block[-1] = i
    attempt = some_block + first_block
    if valid_padding(iv, bytes(attempt)):
        some_block[-1] ^= 3
        for j in range(256):
            some_block[-2] = j
            attempt = some_block + first_block
            if valid_padding(iv, bytes(attempt)):
                print(i ^ ciphertext[-1] ^ 1, j ^ ciphertext[-2] ^ 1)
