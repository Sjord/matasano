from Crypto.Cipher import AES
import os

def mac(key, plaintext, iv=None):
    while len(plaintext) % 16 != 0:
        plaintext += b'\0'

    if iv is None:
        iv = os.urandom(16)
    aes = AES.new(key, AES.MODE_CBC, IV=iv)
    ciphertext = aes.encrypt(plaintext)
    last_block = ciphertext[-16:]
    return (last_block, iv)
    
    
class Client:
    def __init__(self, key, account):
        self._key = key
        self._account = account

    def create_transfer(self, amount, to):
        message = b"from=%s&to=%s&amount=%s" % (self._account, to, amount)
        return message, mac(self._key, message)


class Server:
    def __init__(self, key):
        self._key = key

    def verify_transfer(self, transfer):
        message, (last_block, iv) = transfer
        good_mac = mac(self._key, message, iv)
        return good_mac[0] == last_block

client = Client(b'some random key.', b'1234567')
server = Server(b'some random key.')
transfer = client.create_transfer(b'1000000', b'1234567')

(message, (last_block, iv)) = transfer
# message = b'from=1234567&to=2345678&amount=123'

message = bytearray(message)
# 1234567 -> 2345678
message[5] ^= 3
message[6] ^= 1
message[7] ^= 7
message[8] ^= 1
message[9] ^= 3
message[10] ^= 1
message[11] ^= 15
message = bytes(message)

iv = bytearray(iv)
iv[5] ^= 3
iv[6] ^= 1
iv[7] ^= 7
iv[8] ^= 1
iv[9] ^= 3
iv[10] ^= 1
iv[11] ^= 15
iv = bytes(iv)

print(message)

res = server.verify_transfer((message, (last_block, iv)))
print(res)

