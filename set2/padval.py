
class InvalidPaddingException(RuntimeError):
    pass

def validate_padding(data):
    pad_length = data[-1]
    for i in range(pad_length):
        if data[-i-1] != pad_length:
            raise InvalidPaddingException()
    return data[0:-pad_length]


assert validate_padding(b"ICE ICE BABY\x04\x04\x04\x04")
# assert not validate_padding(b"ICE ICE BABY\x05\x05\x05\x05")
# assert not validate_padding(b"ICE ICE BABY\x01\x02\x03\x04")
assert validate_padding(b"ICE ICE BABY\x04\x04\x04\x04") == b"ICE ICE BABY"

