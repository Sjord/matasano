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
    data = b64decode(random.choice(strings))
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


def decode(iv, first_block, second_block):
    plaintext = bytearray(b'?' * 16)
    some_block = bytearray(b'\0' * 16)

    for x in range(1, 17):
        for j in range(1, x):
            some_block[-j] ^= x ^ (x-1)

        for i in range(256):
            some_block[-x] = i
            attempt = some_block + second_block
            if valid_padding(iv, bytes(attempt)):
                plaintext[-x] = i ^ first_block[-x] ^ x
                break

    return plaintext


assert valid_padding(*encrypt())


iv, ciphertext = encrypt()
blocks = list([ciphertext[i*16:(i+1)*16] for i in range(len(ciphertext) // 16)])
previous_blocks = [iv] + blocks
for prev_block, block in zip(previous_blocks, blocks):
    print(decode(iv, prev_block, block))
