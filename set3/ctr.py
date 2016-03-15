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


def encode(nonce, key, plain):
    stream = get_stream(nonce, key, len(plain))
    return bytearray([c ^ s for c, s in zip(plain, stream)])


if __name__ == "__main__":
    ciphertext = 'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
    key='YELLOW SUBMARINE'
    nonce=0

    ciphertext = b64decode(ciphertext)
    stream = get_stream(nonce, key, len(ciphertext))
    print(encode(nonce, key, ciphertext))
