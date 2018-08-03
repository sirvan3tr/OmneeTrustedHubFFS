modulus = 77
a = 71
QR = 0

for b in range(1,((modulus-1)/2) + 1):
    if (b ** 2) % modulus == a:
        QR = 1

if (QR == 1):
    print "{} is a QR mod {}".format(a, modulus)
else:
    print "{} is a QNR mod {}".format(a, modulus)
    
for i in range(0,modulus):
    for b in range(1,((modulus-1)/2) + 1):
        if (b ** 2) % modulus == i:
            print i