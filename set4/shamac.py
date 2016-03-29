from sha1 import sha1

class Mac:
    def __init__(self, key):
        self._key = key

    def hash(self, message):
        return sha1(self._key + message)

    def verify(self, message, hash):
        return hash == self.hash(message)


if __name__ == "__main__":
    mac = Mac(b'somesecret')
    hash = mac.hash(b'my message')
    assert mac.verify(b'my message', hash)
    assert not mac.verify(b'my messagf', hash)
    print(hash)
