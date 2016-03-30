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

def encrypt(e, data):
    number = int.from_bytes(data, 'big')
    encrypted = pow(number, e, n)
    return encrypted.to_bytes(512, 'big')

def decrypt(d, data):
    number = int.from_bytes(data, 'big')
    decrypted = pow(number, d, n)
    return decrypted.to_bytes(512, 'big').strip(b'\0')

assert modinv(17, 3120) == 2753


p = 0xF8B647D0B63CA97A095CF5E348E5EBBF3EF046F5F21104A8C5D4AB29C829F436D701F74124DBA2E1E70B868283745FA499833B4D8A55BB6981A7328E4C0C21C1
q = 0xD50E170E41706163F86B877F06E9062F3C262A809390ECD8E466EF38951684C13C0EE57CF1A865B3E1E5620D36613985205E5D7306FA1BA536114EF282D0F8A9
n = p * q
et = (p-1)*(q-1)
e = 3
d = modinv(e, et)

c = pow(42, e, n)
print(pow(c, d, n))

print(decrypt(d, encrypt(e, b"hello world")))
