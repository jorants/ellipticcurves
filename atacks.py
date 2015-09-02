import math
import groups
import fields
from general import *

def babyGiant(base,power,n = None):
    if n==None:
        n = base.order() # gives the size of the class
    m = int(math.ceil(math.sqrt(n)))
    table = {}
    for j in range(m):
        baseJ = base**j
        table[str(baseJ)] = j
    AinvM = ~(base**(m))
    Y = power
    for i in range(m):
        if str(Y) in table:
            return i*m+table[str(Y)]
        Y = Y * AinvM
    return None


def pohligHellman_integers(base,power,usebg = True):
    n = base.order()
    factors = factor_primes(n)
    mods = []
    for prime,ppower in factors.iteritems():
        modp = 0
        for i in range(1,ppower+1):
            #calculate C_{i-1}
            lefthand = power**(n / (prime**i))
            lefthand /= (base ** (n/(prime**i)))**(modp)
            rhb =  base** (n/prime)
            if not usebg:
                for c in range(prime):
                    if lefthand == rhb**c:
                        modp += c* (prime**(i-1))
                        break
                else:
                    return None
            else:
                bg = babyGiant(rhb,lefthand,(prime**i))
                if bg == None:
                    return None
                modp += bg*(prime**(i-1))
        mods.append((modp,prime**ppower))
    return reverse_chineese_remainder(mods)[0]
    




def reverse_chineese_remainder(mods):

    def mod_inv(num,mod):
        s = 0
        old_s = 1
        t = 1
        old_t = 0
        r = mod
        old_r = num
        while r != 0:
            quotient = old_r / r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t
        return old_s % mod

    
    def chr_step(pair1,pair2): 
        # x = a mod k
        a  = pair1[0]
        k  = pair1[1] 
        # x = b mod l
        b  = pair2[0]
        l  = pair2[1] 
        
        # A + c1*K = B mod L
        # c1k = b-1 mod L
        c1k = (b-a) % l
        #c1 = (b-a) * k^-1 mod l
        kinv = mod_inv(k%l,l)
        c1 = (c1k*kinv) % l

        x =  (a + c1*k) % (k*l)
        return (x,k*l)

    while len(mods)>1:
        mods = mods[2:]+[chr_step(mods[0],mods[1])]
    return mods[0]


