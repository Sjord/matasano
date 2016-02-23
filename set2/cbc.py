import base64
from Crypto.Cipher import AES


def blocks(data, blocksize):
    for i in range(int(len(data) / blocksize)):
        yield data[i*blocksize:(i+1)*blocksize]


def xor(a, b):
    assert len(a) == len(b)
    result = b''
    for i in range(len(a)):
        result += bytes([a[i] ^ b[i]])
    return result


def encrypt(iv, key, data):
    aes = AES.new(key, AES.MODE_ECB)
    encrypted = b''
    previous = iv
    for block in blocks(data, 16):
        xorred = xor(block, previous)
        crypt_block = aes.encrypt(xorred)
        encrypted += crypt_block
        previous = crypt_block
    return encrypted


def decrypt(iv, key, data):
    aes = AES.new(key, AES.MODE_ECB)
    decrypted = b''
    previous = iv
    for block in blocks(data, 16):
        xorred = aes.decrypt(block)
        decrypted += xor(xorred, previous)
        previous = block
    return decrypted




with open('10.txt') as fp:
    data = base64.b64decode(fp.read())
    print(decrypt(b"\0" * 16, "YELLOW SUBMARINE", data))
