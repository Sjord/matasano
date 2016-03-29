from sha1 import sha1, Sha1Hash
import struct

def create_padding(plain_length):
    message_bit_length = plain_length * 8
    null_bytes = 64 - ((plain_length + 9) % 64)
    padding = b'\x80' + b'\0' * null_bytes + struct.pack(b'>Q', message_bit_length)
    return padding

def init_state(hexmac, length):
    hex_parts = [hexmac[i*8:(i+1)*8] for i in range(5)]
    int_parts = [int(h, 16) for h in hex_parts]
    obj = Sha1Hash()
    obj._h = int_parts
    obj._message_byte_length = length
    return obj        

plain = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
with open('word.txt', 'rb') as fp:
    key = fp.read()
mac = sha1(key + plain)

print("Original MAC:", mac)

suffix = b';is_admin=true;'
attempt = key + plain
attempt += create_padding(len(attempt))
attempt += suffix
actual_mac = sha1(attempt)
print("Actual MAC:  ", actual_mac)

obj = init_state(mac, 2 * 64) 
obj.update(suffix)
new_mac = obj.hexdigest()
print("Updated MAC: ", new_mac)
