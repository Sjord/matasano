
def pad(data, length):
    pad_length = length - len(data)
    return data + pad_length * chr(pad_length)

assert(pad("YELLOW SUBMARINE", 20) == "YELLOW SUBMARINE\x04\x04\x04\x04")
