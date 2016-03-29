from Crypto.Cipher import AES
from struct import pack
from base64 import b64decode

# format=64 bit unsigned little endian nonce,
#        64 bit little endian block count (byte count / 16)

def get_stream(nonce, key, length):
    aes = AES.new(key, AES.MODE_ECB)
    stream = b''
    for i in range(0, 1 + (length // 16)):
        counter = pack('<QQ', nonce, i)
        hash = aes.encrypt(counter)
        stream += hash
    return stream[:length]


def encrypt(nonce, key, plain):
    stream = get_stream(nonce, key, len(plain))
    return bytes([c ^ s for c, s in zip(plain, stream)])


def edit(ciphertext, nonce, key, offset, newtext):
    stream = get_stream(nonce, key, len(ciphertext))
    stream_part = stream[offset:offset+len(newtext)]
    cipher_part = bytearray([p ^ s for p, s in zip(newtext, stream_part)])
    result = bytearray(ciphertext)
    result[offset:offset+len(newtext)] = cipher_part
    return bytes(result)


class Ciphertext:
    def __init__(self, nonce, key, plain):
        self._nonce = nonce
        self._key = key
        self.ciphertext = encrypt(nonce, key, plain)

    def edit(self, offset, newtext):
        return edit(self.ciphertext, self._nonce, self._key, offset, newtext)


def get_ciphertext():
    nonce=30208
    with open('key.txt', 'rb') as fp:
        key = fp.read()

    with open('25.txt', 'rb') as fp:
        key = "YELLOW SUBMARINE"
        aes = AES.new(key, AES.MODE_ECB)
        plain = aes.decrypt(b64decode(fp.read()))

    return Ciphertext(nonce, key, plain)


if __name__ == "__main__":
    obj = get_ciphertext()
    goal = obj.ciphertext
    result = b''
    for offset in range(len(goal)):
        for attempt in range(0xff):
            b = bytes([attempt])
            if obj.edit(offset, b) == goal:
                result += b
                break
        print(result)
