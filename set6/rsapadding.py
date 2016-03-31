import hashlib

msg = b'hi mom'


n = 145353079787925462836289263170553984565468972418163872439411413511737637850852956449522278755594369838569623748733827748082994478676418361099421661005314709817519488746924256715718773946078476749974861999510866217410931858069897692223028943600829595084429939023864351516676896138539531549488717482567305347177
e = 3
public_key = (e, n)
d = 96902053191950308557526175447035989710312648278775914959607609007825091900568637633014852503729579892379749165822551832055329652450945574066281107336876457088543674768479207822112452642608115230908553049418755692245646544317554349821456948948599173569725547836213690795199860641980627483611670389126448115371
private_key = (d, n)


def iroot(k, n):
    u, s = n, n+1
    while u < s:
        s = u
        t = (k-1) * s + n // pow(s, k-1)
        u = t // k
    return s


def decrypt(d, n, data):
    number = int.from_bytes(data, 'big')
    decrypted = pow(number, d, n)
    return decrypted.to_bytes(128, 'big')


def sign(d, n, msg):
    hash = hashlib.sha256(msg).digest()
    padding = b'\0\1' + b'\xff' * (128 - 35) + b'\0'
    block = padding + hash
    block_num = int.from_bytes(block, 'big')
    assert block_num < n
    return pow(block_num, d, n)


def verify(e, n, signature, msg):
    block_num = pow(signature, e, n)
    block = block_num.to_bytes(128, 'big')
    assert block.startswith(b'\0\1')
    hash_start = block.index(b'\xff\0')
    sig_hash = block[hash_start+2:hash_start+34]
    real_hash = hashlib.sha256(msg).digest()
    return sig_hash == real_hash


signature = sign(*private_key, msg)
ok = verify(*public_key, signature, msg)
print(ok)

hash = hashlib.sha256(msg).digest()
forged = b'\0\1\xff\0' + hash + b'\x80' * (128 - 36)
assert len(forged) == 128
forged_root = iroot(3, int.from_bytes(forged, 'big'))
print(verify(e, n, forged_root, msg))
