from random import randrange
from Crypto.Cipher import AES
import os
import hashlib


class Client:
    def encrypt(self, msg):
        iv = os.urandom(16)
        key = self.get_key()
        aes = AES.new(key, AES.MODE_CBC, IV=iv)
        ciphertext = aes.encrypt(msg)
        return (iv, ciphertext)

    def decrypt(self, iv, ciphertext):
        key = self.get_key()
        aes = AES.new(key, AES.MODE_CBC, IV=iv)
        return aes.decrypt(ciphertext)

    def get_key(self):
        s = hashlib.sha1()
        s.update((self.s).to_bytes(512, 'big'))
        return s.digest()[0:16]
        


class A(Client):
    p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
    g = 2

    def __init__(self, network):
        self._network = network.subscribe(self)

    def connect(self):
        self.a = randrange(0, self.p)
        A = pow(self.g, self.a, self.p)
        self._network.send(self, [0, self.p, self.g, A])

    def receive(self, msg):
        if msg[0] == 0:
            _, B = msg
            self.s = pow(B, self.a, self.p)
            iv, ciphertext = self.encrypt(b'Meet me at dawn.')
            self._network.send(self, [1, iv, ciphertext])
        else: 
            _, iv, ciphertext = msg
            plain = self.decrypt(iv, ciphertext)
            print(plain)



class B(Client):
    def __init__(self, network):
        self._network = network.subscribe(self)

    def receive(self, msg):
        if msg[0] == 0:
            _, self.p, self.g, A = msg
            b = randrange(0, self.p)
            B = pow(self.g, b, self.p)
            self.s = pow(A, b, self.p)
            self._network.send(self, [0, B])
        else:
            _, iv, ciphertext = msg
            plain = self.decrypt(iv, ciphertext)
            iv, ciphertext = self.encrypt(plain)
            self._network.send(self, [1, iv, ciphertext])





class Network:
    def __init__(self):
        self._listeners = []

    def subscribe(self, listener):
        self._listeners.append(listener)
        return self

    def send(self, sender, msg):
        for listener in self._listeners:
            if listener != sender:
                listener.receive(msg)
        

network = Network()
a = A(network)
b = B(network)

a.connect()
