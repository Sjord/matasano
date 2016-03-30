from random import SystemRandom
from Crypto.Cipher import AES
import os
import hashlib
import hmac
import socket
import pickle

randrange = SystemRandom().randrange


N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2
k = 3
I = b'sjoerd@example.com'
P = b''

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
        A = 0
        self.A = A
        self._network.send(self, [0, I, A])

    def receive(self, msg):
        if msg[0] == 1:
            _, salt, B = msg
            u = sha256int(self.A, B)
            x = sha256int(salt + P)
            S = 0
            K = sha256(S)
            self._network.send(self, [2, hmac256(K, salt)])
        if msg[0] == 3:
            print(msg[1])


class Network:
    def __init__(self, mitm=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 6040))
        self._listeners = []

    def subscribe(self, listener):
        self._listeners.append(listener)
        return self

    def send(self, sender, msg):
        serialized = pickle.dumps(msg)
        self.sock.sendto(serialized, ('127.0.0.1', 6039))
        self.listen_once()

    def listen_once(self):
        data, addr = self.sock.recvfrom(1024)
        msg = pickle.loads(data)
        print("Received", msg)
        for l in self._listeners:
            l.receive(msg)
        

network = Network()
c = Client(network)
c.connect()
