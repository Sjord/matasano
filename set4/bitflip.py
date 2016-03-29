import os
from Crypto.Cipher import AES
from randctr import encrypt


nonce = 7932
with open('key.txt', 'rb') as fp:
    key = fp.read()

def wrap_user_data(input):
    data = b"comment1=cooking%20MCs;userdata=" + input + b";comment2=%20like%20a%20pound%20of%20bacon"
    return encrypt(nonce, key, data)

def decrypt(ciphertext):
    return encrypt(nonce, key, ciphertext)


encrypted = wrap_user_data(b'_admin_true_')
encrypted = bytearray(encrypted)
encrypted[32] ^= 100  # _ -> ;
encrypted[38] ^= 98   # _ -> =
encrypted[43] ^= 100  # _ -> ;
encrypted = bytes(encrypted)
print(decrypt(encrypted))
