from Crypto.Cipher import AES
import os

def mac(key, plaintext):
    while len(plaintext) % 16 != 0:
        plaintext += b'\0'

    iv = b'\0' * 16 
    aes = AES.new(key, AES.MODE_CBC, IV=iv)
    ciphertext = aes.encrypt(plaintext)
    last_block = ciphertext[-16:]
    return last_block
    
    
class Client:
    def __init__(self, key, account):
        self._key = key
        self._account = account

    def create_transfer(self, amount, to):
        message = b"from=%s&to=%s&amount=%s" % (self._account, to, amount)
        return message, mac(self._key, message)

    def create_transfers(self, transfers):
        transfer_bytes = []
        for to, amount in transfers:
            transfer_bytes.append(b"%s:%s" % (to, amount))
            
        message = b"from=%s&tx_list=%s" % (self._account, b":".join(transfer_bytes))
        return message, mac(self._key, message)


class Server:
    def __init__(self, key):
        self._key = key

    def verify_transfer(self, transfer):
        message, last_block = transfer
        good_mac = mac(self._key, message)
        return good_mac == last_block

client = Client(b'some random key.', b'1234567')
server = Server(b'some random key.')
transfer = client.create_transfers([(b'2345678', b'100')])

(message, last_block) = transfer

extension, extension_mac = client.create_transfers([(b'3456789', b'1000000')])
print(message)
print(extension)

# xor last_block with desired plaintext ourselves and let client sign it
# client only signs from=1234567tx_l
# so let last_block ^ plaintext == from=1234567tx_l

extension = bytearray(extension)
for i in range(16):
    extension[i] ^= last_block[i]
extension = bytes(extension)

extended_message = message + extension
print(extended_message)
res = server.verify_transfer((extended_message, extension_mac))
print(res)
