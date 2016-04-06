from rc4 import encrypt, RC4
from base64 import b64decode
import os
from collections import Counter

secret = b64decode('QkUgU1VSRSBUTyBEUklOSyBZT1VSIE9WQUxUSU5F')

biases = [
    # Byte n, biased towards m, do 2**k requests
    (1, 0, 14),
    (15, 240, 23),  # takes approx 12 min per byte
    (31, 224, 23),

]

def oracle(request):
    key = os.urandom(16)
    return encrypt(key, request + secret)


def get_bias(byte_num):
    for bias in biases:
        if bias[0] >= byte_num:
            return bias
    assert False


def decode_byte(byte_num):
    bias_byte, bias_to, num_requests = get_bias(byte_num)

    # Get byte i on bias_byte
    counts = Counter()
    request = b'a' * (bias_byte - byte_num)
    for i in range(2**num_requests):
        cipher = oracle(request)
        cipher_byte = cipher[bias_byte]
        counts.update([cipher_byte])

    most_common = counts.most_common()
    return bytes([counts.most_common()[0][0] ^ bias_to])

result = b''
for i in range(len(secret)):
    result += decode_byte(i)
    print(result)
