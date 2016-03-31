n = 145353079787925462836289263170553984565468972418163872439411413511737637850852956449522278755594369838569623748733827748082994478676418361099421661005314709817519488746924256715718773946078476749974861999510866217410931858069897692223028943600829595084429939023864351516676896138539531549488717482567305347177
e = 3
public_key = (e, n)
private_key = (96902053191950308557526175447035989710312648278775914959607609007825091900568637633014852503729579892379749165822551832055329652450945574066281107336876457088543674768479207822112452642608115230908553049418755692245646544317554349821456948948599173569725547836213690795199860641980627483611670389126448115371, n)


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def encrypt(e, n, data):
    number = int.from_bytes(data, 'big')
    assert number < n
    encrypted = pow(number, e, n)
    return encrypted.to_bytes(512, 'big')

ciphertext = encrypt(e, n, b'some secret message the server can decrypt')

def decrypt(d, n, data):
    number = int.from_bytes(data, 'big')
    decrypted = pow(number, d, n)
    return decrypted.to_bytes(512, 'big').strip(b'\0')


seen = set()
def oracle(data):
    if data in seen:
        raise RuntimeError('This data has already been decrypted once')
    seen.add(data)
    d, n = private_key
    return decrypt(d, n, data)


oracle(ciphertext)

# Now decrypt ciphertext again without the oracle raising an error
S = 2
ciphernum = int.from_bytes(ciphertext, 'big')
new_ciphernum = (pow(S, e, n) * ciphernum) % n
new_ciphertext = new_ciphernum.to_bytes(512, 'big')

new_plaintext = oracle(new_ciphertext)
new_plainnum = int.from_bytes(new_plaintext, 'big')
real_plainnum = (new_plainnum * modinv(S, n)) % n
print(real_plainnum.to_bytes(512, 'big').strip(b'\0'))
