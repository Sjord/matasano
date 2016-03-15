from base64 import b64decode
from ctr import encode

plains = [
	'SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==',
	'Q29taW5nIHdpdGggdml2aWQgZmFjZXM=',
	'RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==',
	'RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=',
	'SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk',
	'T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==',
	'T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=',
	'UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==',
	'QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=',
	'T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl',
	'VG8gcGxlYXNlIGEgY29tcGFuaW9u',
	'QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==',
	'QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=',
	'QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==',
	'QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=',
	'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=',
	'VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==',
	'SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==',
	'SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==',
	'VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==',
	'V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==',
	'V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==',
	'U2hlIHJvZGUgdG8gaGFycmllcnM/',
	'VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=',
	'QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=',
	'VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=',
	'V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=',
	'SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==',
	'U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==',
	'U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=',
	'VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==',
	'QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu',
	'SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=',
	'VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs',
	'WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=',
	'SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0',
	'SW4gdGhlIGNhc3VhbCBjb21lZHk7',
	'SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=',
	'VHJhbnNmb3JtZWQgdXR0ZXJseTo=',
	'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=',
]

freqs = {
    'a':  8.167,	
    'b':  1.492,	
    'c':  2.782,	
    'd':  4.253,	
    'e':  12.702,	
    'f':  2.228,	
    'g':  2.015,	
    'h':  6.094,	
    'i':  6.966,	
    'j':  0.153,	
    'k':  0.772,	
    'l':  4.025,	
    'm':  2.406,	
    'n':  6.749,	
    'o':  7.507,	
    'p':  1.929,	
    'q':  0.095,	
    'r':  5.987,	
    's':  6.327,	
    't':  9.056,	
    'u':  2.758,	
    'v':  0.978,	
    'w':  2.361,	
    'x':  0.150,	
    'y':  1.974,	
    'z':  0.074,	
    ' ':  8,
}


def text_score(strvalue):
    score = 0
    for letter in strvalue:
        letter = chr(letter)
        score += freqs.get(letter.lower(), -100)
    return score


with open('key.txt', 'rb') as fp:
    key = fp.read()

nonce = 0
ciphers = []
for text in plains:
    text = b64decode(text)
    cipher = encode(nonce, key, text)
    ciphers.append(cipher)

stream = b''

for i in range(20):
    letters = [c[i] for c in ciphers]
    max_score = -1
    max_i = None

    for i in range(256):
        decoded = [l ^ i for l in letters]
        score = text_score(decoded)
        if score > max_score:
            max_score = score
            max_i = i

    stream += bytes([max_i])

for cipher in ciphers:
    decoded = bytearray([c ^ s for c, s in zip(cipher, stream)])
    print(decoded)
        

