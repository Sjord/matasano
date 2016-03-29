from sha1 import sha1
import struct

def create_padding(plain):
    message_bit_length = len(plain) * 8
    null_bytes = 64 - ((len(plain) + 9) % 64)
    padding = b'\x80' + b'\0' * null_bytes + struct.pack(b'>Q', message_bit_length)
    return padding


plain = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
with open('word.txt', 'rb') as fp:
    key = fp.read()
mac = sha1(key + plain)

print(mac)

print(plain+ create_padding(key + plain))
