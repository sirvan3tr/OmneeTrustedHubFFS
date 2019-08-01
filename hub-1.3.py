'''
 Author: Sirvan Almasi @ Imperial College London
 August 2018
 Dissertation Project

 This code represents a trusted organisation with the knowledge
 of p and q, factors of n, thus enabling them to create secret 
 keys for everyone using the same n.
'''

from functions3 import *
import os
import hmac, hashlib, random, csv

#16 bit primes, generated using openssl
#not to be used for production
p = 56999 # Secret
q = 58403 # Secret
n = p*q
nHex = hex(n)
k = 4 # number of keys


idRaw = 'Sirvan Almasi || 26/01/1992 || Saqqez || Sirvan3tr@gmail.com'

jIndices = [] # indices for our supposed pseudorandom functino
publicKeys = [] # the final public keys
secretKeys = [] # secret keys generated

'''
 GENERATE PUB KEY
'''
def genPubKey(idRaw):
    # this bit of the code has to be reviewed
    randInt = random.randint(0, n)
    digest_maker = hmac.new(
        bytes(str(randInt), 'latin-1'),
        bytes(str(idRaw), 'latin-1'),
        hashlib.sha256).hexdigest()
    pubHatInt = int(digest_maker, 16) % n
    pubKey = egcd(pubHatInt, n)[1] % n
    try:
        # Check for sqrt modulus
        c1 = tonelli(pubHatInt,p)
        c2 = tonelli(pubHatInt,q)
        return randInt, pubKey
    except:
        return False, False

# Generate k keys
kMax = 0
while(kMax < k):
    j, v = genPubKey(idRaw)
    if (j):
        jIndices.append(j)
        publicKeys.append(v)
        kMax += 1

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
    
    # Square root signs
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


for v in publicKeys:
    secretKeys.append(genSecretKey(v, p, q, n))

os.system('color a')
print("##Printing public Keys:")
print(publicKeys)

print("##Printing Secret Keys:")
print(secretKeys)

print("##Printing j indices:")
print(jIndices)

print("##Printing n:")
print(n)

print("##Printing I:")
print(idRaw)



'''
ofile  = open('keys.csv', "wb")
writer = csv.writer(ofile, delimiter=',')

writer.writerow(['Public Keys', 'Secret Keys', 'j', 'n', 'I'])
writer.writerow(publicKeys)
writer.writerow([])
writer.writerow(secretKeys)
writer.writerow([])
writer.writerow(jIndices)
writer.writerow([])
writer.writerow([n])
writer.writerow([])
writer.writerow([idRaw])

ofile.close()
'''

