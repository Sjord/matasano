from base64 import b64decode
from Crypto.Cipher import AES

something = b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")


def pad(data):
    pad_length = 16 - len(data) % 16
    return data + bytearray(pad_length * [pad_length])


def encrypt(data):
    with open('key.txt', 'rb') as fp:
        key = fp.read()
    assert len(key) == 16
    return AES.new(key, AES.MODE_ECB).encrypt(pad(data + something))


# Determine block size
prev_len = None
jumps = []
for i in range(1, 100):
    ciphertext = encrypt(b'a' * i)
    if prev_len is not None and len(ciphertext) != prev_len:
        jumps.append(i)
    prev_len = len(ciphertext)
block_size = jumps[1] - jumps[0]
print('Block size:', block_size)
assert block_size == 16

# Is ECB?
ciphertext = encrypt(b'a' * 500)
assert ciphertext[320:336] == ciphertext[336:352]


target = encrypt(b'a' * 15)[0:16]
for i in range(255):
    ciphertext = encrypt(b'a' * 15 + bytearray([i]))
    if ciphertext[0:16] == target:
        print(i, chr(i))
        break

message = b'a' * 192
decoded = b''
while True:
    message = message[1:]
    target = encrypt(message)[0:192]
    for i in range(255):
        ciphertext = encrypt(message + decoded + bytearray([i]))
        if ciphertext[0:192] == target:
            decoded += bytearray([i])
            print(decoded)
            break
    else:
        print("done")
        break
