from functools import reduce
from math import sqrt
from decimal import Decimal

pubkeys = [
    (3, 154958627823382507069208390231268802992828047118059847416043427510524381602930963777952242332542932981658186308917686577059626192462940290368472996044654499366893799656750126073946434791512528648971327916947008835144605551515351251090103574830002174544963960641442315064252593249886452297017340445897735515971),
    (3, 161071380196364161646915724541482273517673588291147238403343552469676215951865950137539288594943854466007129084637659887692638550083750625051675819846345887675754188953765745504361456581784825773505622642495482908014226910691334763086275841072246076025546979175892792534687111551718260226056337395242684470569),
    (3, 145353079787925462836289263170553984565468972418163872439411413511737637850852956449522278755594369838569623748733827748082994478676418361099421661005314709817519488746924256715718773946078476749974861999510866217410931858069897692223028943600829595084429939023864351516676896138539531549488717482567305347177),
]

def encrypt(e, n, data):
    number = int.from_bytes(data, 'big')
    assert number < n
    encrypted = pow(number, e, n)
    return encrypted.to_bytes(512, 'big')

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
 
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
def iroot(k, n):
    u, s = n, n+1
    while u < s:
        s = u
        t = (k-1) * s + n // pow(s, k-1)
        u = t // k
    return s
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

ciphertexts = []
for e, n in pubkeys:
    ciphertexts.append(encrypt(e, n, b'secret message that is long enough for the modulo'))

assert ciphertexts[0] != ciphertexts[1]
assert ciphertexts[0] != ciphertexts[2]
assert ciphertexts[1] != ciphertexts[2]

n = [key[1] for key in pubkeys]
a = [int.from_bytes(c, 'big') for c in ciphertexts]
number = chinese_remainder(n, a)
plain = iroot(3, number)
print(plain.to_bytes(512, 'big').strip(b'\0'))
