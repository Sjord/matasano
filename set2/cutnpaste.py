from Crypto.Cipher import AES
from collections import OrderedDict

def pad(data):
    pad_length = 16 - len(data) % 16
    return data + bytearray(pad_length * [pad_length])

def unpad(data):
    pad_length = data[-1]
    if pad_length < 16:
        data = data[:-pad_length]
    return data


def parse(qs):
    result = OrderedDict()
    pairs = qs.split('&')
    for pair in pairs:
        key, value = pair.split('=')
        result[key] = value
    return result

def escape(value):
    return value.replace('&', 'and').replace('=', 'is')

def unparse(values):
    pairs = []
    for key, value in values.items():
        pairs.append(escape(key) + '=' + escape(str(value)))
    return '&'.join(pairs)

def profile_for(email):
    return unparse(OrderedDict([
        ('email', email),
        ('user_id', 10),
        ('role', 'user')
    ]))

def encrypted_profile_for(email):
    return encrypt(profile_for(email))


def encrypt(data):
    data = bytearray(data, 'utf-8')
    with open('key.txt', 'rb') as fp:
        key = fp.read()
    assert len(key) == 16
    padded = pad(data)
    return AES.new(key, AES.MODE_ECB).encrypt(bytes(padded))

def decrypt(data):
    with open('key.txt', 'rb') as fp:
        key = fp.read()
    assert len(key) == 16
    return unpad(AES.new(key, AES.MODE_ECB).decrypt(data))

def decrypt_profile(encrypted):
    return parse(decrypt(encrypted).decode('utf-8', 'ignore'))
    


qs = 'foo=bar&baz=qux&zap=zazzle'
print(parse(qs))

print(profile_for("foo@bar.com"))
print(profile_for("foo@bar.com&admin=yes"))

print(decrypt_profile(encrypted_profile_for('test@foo.com')))
print(profile_for('hello@world.com'))

# email=h@old.com&user_id=10&role=user
# ================================
ends_in_role_is = encrypted_profile_for('h@old.com')[0:32]
# email=foofoofoofadmin&user_id=10&role=user
#                 ================  
has_admin = encrypted_profile_for('foofoofoofadmin')[16:32]
print(decrypt_profile(ends_in_role_is + has_admin))

