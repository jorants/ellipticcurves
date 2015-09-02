import math
import random
import groups

#HELPER FUNCTIONS
def factor_primes(n):
    current = 2
    sq = math.sqrt(n)
    primes = {}
    #handel two seperate:
    
    while n % current == 0:
        if current not in primes:
            primes[current] = 0
        n/=current
        primes[current]+=1
        sq /= math.sqrt(current) #faster since current<<n
    current = 3
    while current<= sq+1:
        while n % current == 0:
            if current not in primes:
                primes[current] = 0
            n/=current
            primes[current]+=1
            sq /= math.sqrt(current) #faster since current<<n

        current +=2 #only odd numbers

    if n in primes:
        primes[n] += 1
    elif n!=1:
        primes[n] = 1
    return primes


def iter_sublists(l):
    from itertools import combinations,chain
    res = []
    for i in range(len(l)+1):
        res = chain(res,combinations(l,i))
    return res

def all_dividers(prime_factors):
    outroll = []
    for key in prime_factors:
        outroll += [key for i in range(prime_factors[key])]
    return list(set([reduce(lambda x,y: x*y,l,1) for l in iter_sublists(outroll)]))



def is_prob_prime(p,k = 100):
    G = groups.ZpZ(p)
    for t in range(k):
        test = random.randrange(2,p)
        ell = G(test)
        if ell**(p-1) != G.identety():
            return False
    return True

def generate_prime(bits):
    while True:
        p = random.randrange(2**(bits-1)+1, 2**bits)|1
        if is_prob_prime(p):
            return p

