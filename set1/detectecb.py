import base64

with open('8.txt') as fp:
    for line in fp:
        data = base64.b64decode(line)
        parts = [data[i*16:(i+1)*16] for i in range(int(len(data) / 16))]
        if len(parts) != len(set(parts)):
            print(line)
