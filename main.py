import sys
from functools import reduce
sys.setrecursionlimit(1000000)  # long type,32bit OS 4B,64bit OS 8B(1bit for sign)

p = 7  
q = 11
n = p*q
v = 64

idRaw = 'Sirvan Almasi || 26/01/1992 || Saqqez || Sirvan3tr@gmail.com'
# return (g, x, y) a*x + b*y = gcd(x, y)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
 
    for n_i, a_i in zip(n, a):
        p = prod / n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a / b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

# works with py3
#Tonelli-Shanks algorithm
def legendre(a, p):
    return pow(a, (p - 1) // 2, p)
 
def tonelli(n, p):
    assert legendre(n, p) == 1, "not a square (mod p)"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

egcdR = egcd(v, n)
vHat = egcdR[1] % n
print vHat
print egcdR
b1 = 0
b2 = 0
a = 0


n = [p, q]
a = [vHat**2 % q, vHat**2 % p]
print "v and % p and q"
print vHat**2 % p
print vHat**2 % q
print "----------end of"


b1 = vHat**2 % p
b2 = vHat**2 % q

print chinese_remainder(n, a)

print "----------newww---------"
a = [b1, b2, b1, b2*-1, b1*-1, b2*-1, b1*-1, b2]
j = 0
smallest = -1
for i in range(0,4):
    n = [p, q]
    c = [a[j], a[j+1]]
    cr = chinese_remainder(n, c)
    print cr
    if (smallest<0):
        smallest = cr
    elif(cr < smallest):
        smallest = cr
    j +=2

print smallest

print "---------using tonelli method"
print "v and % p and q"
print v % p
print v % q
print "----------end of"
try:
    b1 = tonelli(v % p, p)
except:
    b1 = 0

try:
    b2 = tonelli(v % q, q)  
except:
    b2 = 0


print b1
print b2

if (b1 != 0 and b2 != 0):
    a = [b1, b2, b1, b2*-1, b1*-1, b2*-1, b1*-1, b2]
    j = 0
    smallest = -1
    for i in range(0,4):
        n = [p, q]
        c = [a[j], a[j+1]]
        cr = chinese_remainder(n, c)
        print cr
        if (smallest<0):
            smallest = cr
        elif(cr < smallest):
            smallest = cr
        j +=2

    print smallest
elif (b1 == 0):
    smallest = b2 % q
elif (b2 ==0):
    smallest = b1 % p

print smallest
