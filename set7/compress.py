import zlib
from Crypto.Cipher import AES
import os

def xor(a, b):
    result = []
    for la, lb in zip(a, b):
        result.append(la ^ lb)
    return bytes(result)

def cbc(plaintext):
    pad = 16 - len(plaintext) % 16
    plaintext += bytes([pad] * pad)

    iv = os.urandom(16)
    key = os.urandom(16)
    aes = AES.new(key, AES.MODE_CBC, IV=iv)
    return aes.encrypt(plaintext)

def request(P):
    request = b"""POST / HTTP/1.1
    Host: hapless.com
    Cookie: sessionid=TmV2ZXIgcmV2ZWFsIHRoZSBXdS1UYW5nIFNlY3JldCE=
    Content-Length: %d

    %s""" % (len(P), P)
    compressed = zlib.compress(request)
    encrypted = cbc(compressed)
    assert len(encrypted) % 16 == 0
    return len(encrypted)


def found_solution(candidates):
    for c in candidates:
        if len(c) > 30 and c.endswith(b'='):
            return True
    return False


candidates = [b'sessionid=']

while not found_solution(candidates):
    new_candidates = []
    for sessionid in candidates:
        base_len = request(sessionid + b'%')
        for i in b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=':
            length = request(sessionid + bytes([i]))
            if length < base_len:
                new_candidates.append(sessionid + bytes([i]))
    candidates = new_candidates
    print(candidates)
