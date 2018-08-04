from functions import *
import hmac, hashlib, random



#16 bit primes, generated using openssl
#not to be used for production
p = 56999
q = 58403
n = p*q
nHex = hex(n)
k = 1 # number of keys

idRaw = 'Sirvan Almasi || 26/01/1992 || Saqqez || Sirvan3tr@gmail.com'

jIndices = []
publicKeys = []

'''
k = 0
for i in range(0,5):
    print i
    digest_maker = hmac.new(str(i), idRaw, hashlib.sha256)
    digest = digest_maker.hexdigest()
    try:
        c1 = tonelli(int(digest,16),p)
        c2 = tonelli(int(digest,16),q)
        jIndices.append(i)
        publicKeys.append(digest)
        print digest.hex()
        if k == 5:
            break
        k += 1
    except:
        continue

print jIndices

hash = 1
idRawHex = idRaw.encode('hex')
for i in range(0, len(idRawHex)):
    hash = hash*11 + int(idRawHex[i], 16)

# HexByte with : sep'
":".join("{:02x}".format(ord(c)) for c in idRaw)

print "my hash: "
print hash % n
'''

'''
 GENERATE PUB KEY
'''
def genPubKey(idRaw):
    randInt = random.randint(0, n)
    digest_maker = hmac.new(str(randInt), idRaw, hashlib.sha256)
    digest = digest_maker.hexdigest()
    digestInt = int(digest, 16) % n
    try:
        # Check for sqrt modulus
        c1 = tonelli(digestInt,p)
        c2 = tonelli(digestInt,q)
        return randInt
    except:
        return False

# Generate k keys
kMax = 0
while(kMax < k):
    jind = genPubKey(idRaw)
    if (jind):
        jIndices.append(jind)
        kMax += 1

'''
 GET PUB KEYS
    from the j indices, which we generated above, get the
    respected pub key

    idRaw = string of users identity
    j = indices determined on creation of public key
'''
def getPubKey(idRaw, j, n):
    digest_maker = hmac.new(str(j), idRaw, hashlib.sha256)
    digest = digest_maker.hexdigest()
    pubHatInt = int(digest, 16) % n
    pubKey = egcd(pubHatInt, n)[1] % n
    return pubKey

for i in jIndices:
    publicKeys.append(getPubKey(idRaw,i,n))

print "---- Printing Public Keys ----"
print publicKeys

'''
 GENERATE SECRET KEY
    v = public key
    p and q = secret factors of n
    n = modulus, product of p & q
'''
def genSecretKey(v, p, q, n):
    v = egcd(v, n)[1] % n
    b1 = tonelli(v % p, p)
    b2 = tonelli(v % q, q) 

    a = [b1, b2, b1, b2*-1, b1*-1, b2*-1, b1*-1, b2]
    j = 0
    smallest = -1
    for i in range(0,4):
        n = [p, q]
        c = [a[j], a[j+1]]
        cr = chinese_remainder(n, c)
        if (smallest<0):
            smallest = cr
        elif(cr < smallest):
            smallest = cr
        j +=2

    return smallest

print "---- Printing Secret Keys ----"
for v in publicKeys:
    print genSecretKey(v, p, q, n)