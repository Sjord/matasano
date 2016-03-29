from md4 import md4
import struct
from binascii import hexlify, unhexlify

def create_padding(plain_length):
    message_bit_length = plain_length * 8
    null_bytes = 64 - ((plain_length + 9) % 64)
    padding = b'\x80' + b'\0' * null_bytes + struct.pack(b'<Q', message_bit_length)
    return padding

def init_state(hexmac, blocks):
    binary = unhexlify(hexmac)
    int_parts = struct.unpack("<4I", binary)
    obj = md4(*int_parts)
    obj._count = blocks
    return obj        

def md4hash(msg):
    obj = md4()
    obj.update(msg)
    return obj.hexdigest()

plain = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
with open('word.txt', 'rb') as fp:
    key = fp.read()
mac = md4hash(key + plain)

print("Original MAC:", mac)

suffix = b';is_admin=true;'
attempt = key + plain
attempt += create_padding(len(attempt))
attempt += suffix
actual_mac = md4hash(attempt)
print("Actual MAC:  ", actual_mac)

obj = init_state(mac, 2) 
obj.update(suffix)
new_mac = obj.hexdigest()
print("Updated MAC: ", new_mac)
