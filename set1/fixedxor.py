

def xor(one, two):
    result = ''
    for a, b in zip(one, two):
        result += chr(ord(a) ^ ord(b))
    return result



assert xor('1c0111001f010100061a024b53535009181c'.decode('hex'), '686974207468652062756c6c277320657965'.decode('hex')) == '746865206b696420646f6e277420706c6179'.decode('hex')
