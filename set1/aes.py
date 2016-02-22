from Crypto.Cipher import AES
import base64

key = "YELLOW SUBMARINE"
aes = AES.new(key, AES.MODE_ECB)
with open('7.txt') as fp:
    print(aes.decrypt(base64.b64decode(fp.read())))
