import sys

if len(sys.argv) == 2:
    with open(sys.argv[1]) as fp:
        plain = fp.read()
else:
    plain = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

cipher = "ICE"

result = ''
i = 0
for letter in plain:
    result += chr(ord(letter) ^ ord(cipher[i]))
    i = (i + 1) % len(cipher)

print(result.encode('hex'))
