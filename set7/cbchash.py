from Crypto.Cipher import AES
from binascii import hexlify

def mac(key, plaintext, padded=True):
    if padded:
        pad = 16 - len(plaintext) % 16
        plaintext += bytes([pad]) * pad

    iv = b'\0' * 16 
    aes = AES.new(key, AES.MODE_CBC, IV=iv)
    ciphertext = aes.encrypt(plaintext)
    last_block = ciphertext[-16:]
    return last_block

def ecb(key, plaintext):
    assert len(plaintext) == 16
    aes = AES.new(key, AES.MODE_ECB)
    ciphertext = aes.encrypt(plaintext)
    return ciphertext


def ecb_decrypt(key, plaintext):
    assert len(plaintext) == 16
    aes = AES.new(key, AES.MODE_ECB)
    ciphertext = aes.decrypt(plaintext)
    return ciphertext


def verify(key, plaintext, hash):
    return mac(key, plaintext) == hash
 

def xor(a, b):
    result = []
    for la, lb in zip(a, b):
        result.append(la ^ lb)
    return bytes(result)


code = b"alert('MZA who was that?');\n"
key = b"YELLOW SUBMARINE"

assert mac(key, b'hello world') == ecb(key, b'hello world\5\5\5\5\5')

hash = mac(key, code)
assert hexlify(hash) == b"296b8d7cb78a243dda4d0a61d33bbdd1"
assert verify(key, code, hash)

# Compute ECB input to second block
partial = b"alert('MZA who w"
partial_mac = ecb(key, partial)
xor_result = xor(partial_mac, b"as that?');\n\4\4\4\4")

assert xor_result == ecb_decrypt(key, hash)

previous_xor_result = ecb_decrypt(key, xor(xor_result, bytes([16]) * 16))


new_code = b"alert('Ayo, the Wu is back!');               // "
new_mac = mac(key, new_code, False)
data_for_same_xor = xor(new_mac, previous_xor_result)

new_code += data_for_same_xor
assert len(new_code) % 16 == 0
print(new_code)
print(hexlify(mac(key, new_code)))
