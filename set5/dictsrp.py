from random import SystemRandom
from Crypto.Cipher import AES
import os
import hashlib
import hmac

randrange = SystemRandom().randrange


N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2
k = 3
I = b'sjoerd@example.com'
P = b'Hunter2'

def convert_to_bytes(items):
    result = []
    for item in items:
        try:
            result.append(item.to_bytes(512, 'big'))
        except AttributeError:
            result.append(item)
    return result


def sha256(*items):
    data = b''.join(convert_to_bytes(items))
    s = hashlib.sha256()
    s.update(data)
    return s.digest()

def sha256int(*items):
    return int.from_bytes(sha256(*items), 'big')


def hmac256(key, *items):
    h = hmac.new(key, digestmod='sha256')
    data = b''.join(convert_to_bytes(items))
    h.update(data)
    return h.digest()
    

class Client:
    def __init__(self, network):
        self._network = network.subscribe(self)

    def connect(self):
        self.a = randrange(0, N)
        A = pow(g, self.a, N)
        self.A = A
        self._network.send(self, [0, I, A])

    def receive(self, msg):
        if msg[0] == 1:
            _, salt, B = msg
            u = sha256int(self.A, B)
            x = sha256int(salt + P)
            S = pow(B, self.a + u * x, N)
            K = sha256(S)
            self._network.send(self, [2, hmac256(K, salt)])



class Server:
    def __init__(self, network):
        self._network = network.subscribe(self)

        self._salt = os.urandom(16)
        x = sha256int(self._salt + P)
        self.v = pow(g, x, N)

    def receive(self, msg):
        if msg[0] == 0:
            _, I, A = msg
            b = randrange(0, N)
            B = pow(g, b, N)
            u = sha256int(A, B)
            S = pow(A * pow(self.v, u, N), b, N)
            self.K = sha256(S)
            self._network.send(self, [1, self._salt, B])
        if msg[0] == 2:
            _, theirs = msg
            mine = hmac256(self.K, self._salt)
            if theirs == mine:
                print("OK")
            else:
                print("NOK")



class Mitm:
    """
    If g=2, B=2:
    A = 2 ** a
    S = 2 ** (a + u * x) = A * 2 ** (u + x)
    """

    passwords = [
        b'letmein',
        b'password',
        b'12345678',
        b'Hunter2',
        b'apple',
        b'qwerty',
    ]

    def intercept(self, sender, msg):
        if msg[0] == 0:
            _, _, self.A = msg

        if msg[0] == 1:
            n, salt, old_b = msg
            return [n, b'', 2]

        if msg[0] == 2:
            _, mac = msg
            print("MAC", mac)

            u = sha256int(self.A, 2)
            salt = b''
            for pw in self.passwords:
                x = sha256int(pw)
                S = (self.A * pow(2, u * x, N)) % N
                K = sha256(S)
                if mac == hmac256(K, salt):
                    print(pw)
                    break
            else:
                print("Failed")

        return msg



class Network:
    def __init__(self, mitm=None):
        self._listeners = []
        self._mitm = mitm

    def subscribe(self, listener):
        self._listeners.append(listener)
        return self

    def send(self, sender, msg):
        if self._mitm:
            msg = self._mitm.intercept(sender, msg)
        for listener in self._listeners:
            if listener != sender:
                listener.receive(msg)
        

mitm = Mitm()
network = Network(mitm=mitm)
c = Client(network)
s = Server(network)

c.connect()
