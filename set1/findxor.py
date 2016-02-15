from xorcipher import text_score, xor, crack_single_xor

best_all = []
with open('4.txt') as fp:
    for line in fp:
        line = line.strip().decode('hex')
        best = crack_single_xor(line)
        best_all.append(best)

print max(best_all, key=text_score)
