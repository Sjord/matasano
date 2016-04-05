import os
from collections import defaultdict
from random import randrange
from Crypto.Cipher import AES
from multicol import blocks

def pad(data):
    data += b'\0' + len(data).to_bytes(8, 'big') + b'\0' * 7
    return data

def C(block, H):
    key = H.to_bytes(16, 'big')
    aes = AES.new(key, AES.MODE_CBC, IV=b'\0' * 16)
    cipher = aes.encrypt(block)
    cipher_num = int.from_bytes(cipher, 'big')
    return cipher_num % 0xffff


def MD(message):
    H = 0xde98
    for block in blocks(pad(message)):
        H = C(block, H)
    return H



from_index = defaultdict(list)
to_index = defaultdict(list)

hashes = []
for i in range(2**18):
    block = os.urandom(16)
    H = i
    hash = C(block, H)
    # H -> hash using block
    hashes.append((H, block, hash))
    from_index[H].append((H, block, hash))
    to_index[hash].append((H, block, hash))



root_attempts = []
for hash, nodes in to_index.items():
    if len(nodes) > 10:
        root_attempts.append(nodes)
        
best_root = (0, [], 0, [])
for roots in root_attempts:
    leaves = roots
    all_nodes = {node[0]: node for node in roots}

    for i in range(10):
        new_leaves = []
        for leaf in leaves:
            new_leaves.extend(to_index[leaf[0]])
        leaves = new_leaves

        for node in leaves:
            all_nodes[node[0]] = node

        if len(leaves) > best_root[0]:
            best_root = (len(leaves), roots, i + 2, leaves, all_nodes)


len_leaves, roots, glue_num, leaves, all_nodes = best_root
# Our length: glue_num blocks, 64 for the message, one glue block
end_block = b'\0' + (glue_num * 16 + 64 + 16).to_bytes(8, 'big') + b'\0' * 7
end_hash = roots[0][2]
print('Root block hash', end_hash)
end_hash = C(end_block, end_hash)

print('Prediction with hash: %d' % end_hash)

message = b'A Tesla will be able to drive itself across the country in 2018.'
assert len(message) == 64

H = 0xde98
for block in blocks(message):
    H = C(block, H)

print('H of message', H)

leaf_index = {}
for leaf in leaves:
    leaf_index[leaf[0]] = leaf

# Find a block that map from H to anything in leaf_index
while True:
    block = os.urandom(16)
    glued_h = C(block, H)
    if glued_h in leaf_index:
        break

print('H after glue', glued_h)

total_message = message + block
from_hash = glued_h
for i in range(glue_num):
    leaf = all_nodes[from_hash]
    total_message += leaf[1]
    from_hash = leaf[2]
    print('H after block', i, from_hash)

print(total_message)
print(MD(total_message))
