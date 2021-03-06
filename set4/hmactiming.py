from sha1 import sha1, Sha1Hash
from time import sleep, time
from statistics import median

blocksize = 64

def xor(ma, mb):
    return bytes([a ^ b for a, b in zip(ma, mb)])


def sha1bytes(message):
    return Sha1Hash().update(message).digest()


def hmac(key, message):
    if len(key) > blocksize:
        key = sha1(key)
    if len(key) < blocksize:
        key = key + b'\0' * (blocksize - len(key))
   
    o_key_pad = xor(b'\x5c' * blocksize, key)
    i_key_pad = xor(b'\x36' * blocksize, key)
   
    return sha1(o_key_pad + sha1bytes(i_key_pad + message))


def insecure_compare(ma, mb):
    if len(ma) != len(mb):
        return False

    for a, b in zip(ma, mb):
        if a != b:
            return False
        sleep(0.005)
    return True


with open('key.txt', 'rb') as fp:
    key = fp.read()

def validate_hmac(message, mac):
    return insecure_compare(mac, hmac(key, message))


def time_compare(message, mac):
    start = time()
    validate_hmac(message, mac)
    return time() - start


def find_character(base_mac, offset):
    durations = []
    for attempt in '3acb194560278fde':
        hmac_attempt[offset] = attempt
        times = [time_compare(subject, ''.join(hmac_attempt)) for i in range(3)]
        duration = median(times)
        durations.append((attempt, duration))
    attempt, duration = max(durations, key=lambda x: x[1])
    return attempt


if __name__ == "__main__":
    # assert hmac(b'', b'') == 'fbdb1d1b18aa6c08324b7d64b71fb76370690e1d'
    # assert hmac(b"key", b"The quick brown fox jumps over the lazy dog") == 'de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9'
    # assert insecure_compare("hello", "hello")
    # assert validate_hmac(b'msg', hmac(key, b'msg'))

    subject = b'get a valid hmac for this string'
    hmac_attempt = list('x' * 40)

    for offset in range(40):
        found = find_character(hmac_attempt, offset)
        hmac_attempt[offset] = found
        print(''.join(hmac_attempt))

    assert validate_hmac(subject, ''.join(hmac_attempt))

# correct HMAC: 53ca3c1a2fb93671acb193638953041bacba4234
