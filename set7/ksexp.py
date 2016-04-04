from multicol import C, blocks
import os

block_size = 16

def MD(message, H):
    for block in blocks(message):
        H = C(block, H)
    return H

def pad(data):
    data += b'\0' + len(data).to_bytes(8, 'big')
    pad_bytes = 16 - len(data) % 16
    data += bytes([pad_bytes] * pad_bytes)
    return data

def find_collision(k, H):
    """Find collision between a single-block message and a message of 2^(k-1)+1 blocks."""
    num_blocks = 2 ** (k-1) + 1
    long_prefix = os.urandom(block_size * (num_blocks - 1))
    long_prefix_hash = MD(long_prefix, H)

    long_hashes = {}

    while True:
        long_end_block = os.urandom(block_size)
        long_hash = C(long_end_block, long_prefix_hash)
        long_hashes[long_hash] = long_end_block

        short_block = os.urandom(block_size)
        short_hash = MD(short_block, H)

        if short_hash in long_hashes:
            long_blocks = long_prefix + long_hashes[short_hash]
            assert len(long_blocks) == block_size * num_blocks
            assert MD(long_blocks, H) == short_hash
            return (short_block, long_blocks, short_hash)


with open('paper-preimages.pdf', 'rb') as fp:
    data = fp.read()

data = pad(data)

intermediates = []
H = 0x3fe4
for block in blocks(data):
    intermediates.append(H)
    H = C(block, H)

data_hash = H

expandable = []
H = 0x3fe4
for i in range(16):
    (m1, m2, H) = find_collision(16 - i, H)
    expandable.append((i, m1, m2, H))

# This sometimes fails. If it does, just run it again.
assert H in intermediates
index = intermediates.index(H)
assert index > len(expandable)

# We have 16 blocks of expandable, that collide with block `index` in data. Expand expandable to be index blocks.
T = index - 16
S = bin(T)[2:].rjust(16, '0')
M = b''
for i in range(16):
    if S[i] == '1':
        M += expandable[i][2]
    else:
        M += expandable[i][1]

assert len(M) == index * 16

collision_message = M + data[index*16:]
assert collision_message != data
assert len(collision_message) == len(data)
assert MD(collision_message, 0x3fe4) == MD(data, 0x3fe4)

print("Found collision")
