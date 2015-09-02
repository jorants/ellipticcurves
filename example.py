from atacks import *
from fields import *
from groups import *
import random


p = 2
r = -1

snm1 = 2
sn = r

form = "$%i$ & $%i$ & $%i$ & $%s$ \\\\" 
for q in range(1,20):
    order = p**q + 1 - sn
    primes = factor_primes(order)
    primes = [(k, primes[k]) for k in primes.keys()]
    primes.sort(key = lambda x: x[0])
    primes = list(map(lambda x: "%i^{%i}" % x,primes))
    primes = " ".join(primes)
    print form % (q,sn,order,primes)
    sn,snm1 = r*sn - p * snm1,sn
exit(0)

"""
F = Fp(5)
P = Polynomials(F)
A = P.Xn(5) - P.Xn(1)
B = P.Xn(2)

print A.gcd(B)
print B.gcd(A)
"""

"""

F = Fpq(5,2)
print F.one().poly
"""

"""
G = random_non_smooth(32)

print G.group_order()
print factor_primes(G.group_order())
"""


""" primes
print factor_primes(1620)
print factor_primes(720720)
"""

""" Baby giant!
F = prime_group(32) #big prime group
base = F(3)
power = base ** (random.randrange(2,F.group_order()-1)) #choose some random power

print "log_%s(%s) =" % (str(base),str(power)),babyGiant(base,power)
"""

import time
from tabulate import tabulate

sum1,sum2,sum3 = 0,0,0
F = Fpq(5,3)
C = elliptic_curve(F,F.one(),F.zero())   

print C.group_order()
print factor_primes(C.group_order())

for i in range(10):
    while True:
        base = C.random()
        order = base.order()
        if  order >= C.group_order() ** 0.5: #make sure it has a large prime as suborder
            break
    t =  (random.randrange(2,base.order()-1)) #choose some random power
    power = base ** t
    t1 = time.clock()
    res1 = babyGiant(base,power)
    t2 = time.clock()
    res2 = pohligHellman_integers(base,power,False)
    t3 = time.clock()
    res3 = pohligHellman_integers(base,power,True)
    t4 = time.clock()
    sum1 += t2-t1
    sum2 += t3-t2
    sum3 += t4-t3
    print t,res1,res2,res3

print "babyGiant: ",sum1
print "PH true: ",sum2
print "PH+BG: ",sum3

"""
F = mod_p(37)

C =  elliptic_curve(F,F(-5),F(8))
P1 = C(F(6),F(3))
P2 = C(F(9),F(10))

print P1
print P2
print P1*P2
print P1*P1

F = Q()
C = elliptic_curve(F,F(-1),F(4))
P1 = C(F(0),F(2))
P2 = C(F(-1),F(-2))


print P1
print P2
print P1*P2
print P1*P1


"""
