import fields
import general
import pprint
fp = open("irr.txt")
data = eval(fp.read())
fp.close()

t = 2
last = None
try:
    while True:
        t+=1
        f = general.factor_primes(t)
        if len(f) == 1 and f[f.keys()[0]]>1:
            p = f.keys()[0]
            q = f[f.keys()[0]]
            if p in data and q in data[p]:
                continue
            F = fields.Fpq(p,q)
            print p,q," :: ",F.one().poly.coefs
except KeyboardInterrupt:
    fp = open("irr.txt","w")
    s = pprint.pformat(data)
    fp.write(s)
    fp.close()
    
print last
