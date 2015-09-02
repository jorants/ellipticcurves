import random
from skeleton import *

def Fp(p):
    class FP(Field):
        def __init__(self,k):
            self.k = k % p
            self.p = p

        @classmethod
        def char(cls):
            return p

            
        @classmethod
        def all(cls):
            for i in range(p):
                yield cls(i)

        @classmethod
        def zero(cls):
            return cls(0)

        @classmethod
        def one(cls):
            return cls(1)

        @classmethod
        def identety(cls):
            return cls(1)

        
        @classmethod
        def random(cls):
            return cls(random.randrange(0,p))
        
        def __add__(self,other):
            return FP(self.k+other.k)

        def __mul__(self,other):
            if other.__class__ == FP:
                return FP(self.k*other.k)
            elif other.__class__ == int:
                return FP(self.k*other)
            else:
                return NotImplemented

            
        def __neg__(self):
            return FP(-self.k)

        @staticmethod
        def group_order():
            return p-1

        
        def __invert__(self):
            if self.k == 0:
                return None
            s = 0
            old_s = 1
            t = 1
            old_t = 0
            r = self.p
            old_r = self.k
            while r != 0:
                quotient = old_r / r
                old_r, r = r, old_r - quotient * r
                old_s, s = s, old_s - quotient * s
                old_t, t = t, old_t - quotient * t
            return FP(old_s)
        
        
        def __str__(self):
            return str(self.k)

        def sqrt(self):

            if self.k == 0:
                return self
            
            if (self**((p-1)/2)).k == p-1:
                return None
            
            if p %4 == 3:
                return self**((p+1)/4)
                        
            if p %8 == 5:
                d = self**((p-1)/4)
                if d.k == 1:
                    return self**((3+p)/8)
                else:
                    #d = -1
                    return (self*2)*((self*4)**((p-5)/8))
            #no direct solution is known, do it the hard way.
            #find a non residue

            n = self.k
            z = self.random()
            while (z**((p-1)/2)).k != p-1:
                z = self.random()

            Q = p-1
            S = 0

            while Q%2 == 0:
                Q/=2
                S+=1
            
            c = z**Q
            R = self**((Q+1)/2)
            t = self**Q
            M = S
            while True:
                if t.k == 1:
                    return R
                tmp = t
                for i in range(1,M):
                    if (t**(2**i)).k == 1:
                        break
                b = c**((int(2**(M-i-1))))
                R = R*b
                t = t*b*b
                c = b*b
                M = i
            return None #takes to long something wrong

    return FP


def Q():
    class fraction(Field):
        def __init__(self,a = None,b = None):
            if b == None:
                b = 1
            if a == None:
                a = 1    
            self.a = a
            self.b = b
            if self.b<0:
                self.a *= -1
                self.b *= -1
            if self.b == 0:
                raise ValueError("Can not devide by zero")    

            from fractions import gcd
            g = gcd(self.a,self.b)
            self.a /= g
            self.b /= g

                        
        @classmethod
        def char(cls):
            return 0
            
        @classmethod
        def all(cls):
            return
            yield


        @classmethod
        def zero(cls):
            return cls(0,1)

        @classmethod
        def one(cls):
            return cls(1,1)

        @classmethod
        def identety(cls):
            return cls(1,1)

        @classmethod
        def random(cls,press = 8,maximum = 10):
            b =  random.randrange(1,2**press)
            a = random.randrange(-b*maximum,b*maximum)
            return cls(a,b)
        
        def __add__(self,other):
            return fraction(self.a*other.b+self.b*other.a,other.b*self.b)

        def __mul__(self,other):
            if other.__class__ == fraction:
                return fraction(self.a*other.a,self.b*other.b)
            elif other.__class__ == int:
                return fraction(self.a*other,self.b)
            
        def __neg__(self):
            return fraction(-self.a,self.b)

        @staticmethod
        def group_order():
            return None
        
        def __invert__(self):
            if self.a == 0:
                return None
            return fraction(self.b,self.a)
        

        def sqrt(self):
            #integeronly sqrt
            def is_square(apositiveint):
                x = apositiveint
                seen = set([x])
                while x * x != apositiveint:
                    x = (x + (apositiveint // x)) // 2
                    if x in seen: return False
                    seen.add(x)
                return True
            
            if not is_square(self.a) or not  is_square(self.b):
                return None
            else:
                return fraction(int(self.a**0.5),int(self.b**0.5))
        
        def __str__(self):
            if self.b == 1:
                return str(self.a)
            return "(%i / %i)" % (self.a,self.b)

    return fraction


def Polynomials(F):
    class polyring(Field): #not really a field but we can ignore that is we overwrite divisio
        def __init__(self,coefs):
            lc = len(coefs)
            Done = True
            for i in range(lc-1,-1,-1):
                if coefs[i]!=F.zero():
                    self.coefs = coefs[:i+1]
                    Done = False
                    break
            if Done:
                self.coefs = []
            self.F = F
            if len(self.coefs)>0:
                if type(self.coefs[-1])==int:
                    raise TypeError(type(self.coefs[-1]))

        @classmethod
        def __iter__(cls):
            return cls.all()

        @classmethod
        def all(cls):
            return
            yield
            
        @classmethod
        def random(cls,degree):
            coefs = [F.random() for i in range(degree+1)]
            return cls(coefs)

        def deg(self):
            return max(len(self.coefs)-1,0)

        def lc(self):
            if len(self.coefs)==0:
                return F.zero()
            return self.coefs[-1]
        
        def polydiv(self,other):
            if other == polyring.zero():
                raise ValueError("Cant devide by zero")
            
            res1 = polyring(self.coefs)
            res2 = polyring.zero()
            while res1.deg()>=other.deg() and res1 != polyring.zero():
                factor = (res1.lc()/other.lc()) * self.Xn(res1.deg()-other.deg())
                if factor == polyring.zero():
                    break
                res1 = res1 - factor*other
                res2 = res2+factor

            return (res2,res1)
        
        @classmethod
        def Xn(cls,n):
            return cls([F.zero() for i in range(n)]+[F.one()])
        
        def __mod__(self,other):
            return self.polydiv(other)[1]

        def __div__(self,other):
            return self.polydiv(other)[0]


        def order(self):
            return None

        def __mul__(self,other):
            if type(other) == int:
                return polyring([x*other for x in self.coefs])
            if other.__class__ == F:
                other = polyring([other])

                    
            la = len(self.coefs)
            lb = len(other.coefs)
            lc = la+lb
            res = [F.zero() for i in range(lc)]
            for i in range(la):
                for j in range(lb):
                    res[i+j] += self.coefs[i]*other.coefs[j]
            return polyring(res)

        __rmul__ = __mul__
        
        def __add__(self,other):
            la = len(self.coefs)
            lb = len(other.coefs)
            lc = max(la,lb)
            res = [F.zero() for i in range(lc)]
            for i in range(lc):
                res[i] += (self.coefs[i] if i<la else F.zero()) + (other.coefs[i] if i<lb else F.zero())
            return polyring(res)
        
        def __neg__(self):
            res = [-c for c in self.coefs]
            return polyring(res)


        def __inverse__(self):
            if len(self.coefs) == 1:
                return polyring([~self.coefs[0]])
            return None
            
        def __str__(self):
            res = ""
            lc = len(self.coefs)
            for i in range(lc-1,-1,-1):
                if self.coefs[i] == F.zero():
                    continue
                if self.coefs[i] != F.one() or i == 0:
                    res += str(self.coefs[i])
                if i>1:
                    res+= " X^%i + " % i
                if i==1:
                    res+= " X + "

            if len(res.strip()) == 0:
                return "0"
            res= res.strip()
            if res[-1] == "+":
                res = res[:-1]
            return res.strip()

        def gcd(self,other):
            s = polyring.zero()
            old_s = polyring.one()
            t = polyring.one()
            old_t = polyring.zero()
            r = polyring(other.coefs)
            old_r = polyring(self.coefs)
            while r != polyring.zero():
                q,p = old_r.polydiv(r)
                quotient = old_r / r
                old_r, r = r, p
                old_s, s = s, old_s - q * s
                old_t, t = t, old_t - q * t
            return old_r

        
        @classmethod
        def one(cls):
            return cls([F.one()])

        @classmethod
        def identety(cls):
            return cls([F.one()])

        @classmethod
        def zero(cls):
            return cls([])
    return polyring


def ModPoly(poly):
    class modpoly(Field):
        def __init__(self,data):
            self.basering = poly.__class__
            if data.__class__ != self.basering:
                data = poly.__class__(data)
            self.F = poly.F
            self.k = data
            self.poly = poly
            if self.k.deg() >= poly.deg():
                self.k = (self.k % poly)


        @classmethod
        def Xn(cls,n):
            return cls([poly.F.zero() for i in range(n)]+[poly.F.one()])

                
        @classmethod
        def char(cls):
            return poly.F.char()
                
        @classmethod
        def random(cls):
            return modpoly(poly.__class__.random(poly.deg()-1))

        
        @classmethod
        def all(cls):
            import itertools
            for coefs in itertools.product(poly.F.all(),repeat=poly.deg()):
                yield modpoly(list(coefs))
            return

        @classmethod
        def zero(cls):
            return cls(poly.__class__.zero())

        @classmethod
        def one(cls):
            return cls(poly.__class__.one())

        @classmethod
        def identety(cls):
            return cls(poly.__class__.one())

        def deg(self):
            return self.k.deg()
        
        def __add__(self,other):
            return modpoly(self.k+other.k)

        def __mul__(self,other):
            if other.__class__ == self.__class__:
                return modpoly(self.k*other.k)
            else:
                return modpoly(self.k*other)
            
        def __neg__(self):
            return modpoly(-self.k)

        @staticmethod
        def group_order():
            return (poly.F.group_order()+1)**poly.deg() - 1
        
        def __invert__(self):
            if self.k == 0:
                return None
            s = poly.zero()
            old_s = poly.one()
            t = poly.one()
            old_t = poly.zero()
            r = poly
            old_r = self.k
            while r != poly.zero():
                q,p = old_r.polydiv(r)
                quotient = q
                old_r, r = r, p
                old_s, s = s, old_s - quotient * s
                old_t, t = t, old_t - quotient * t
            if old_r.deg() == 0 and old_r != poly.one():
                    ell = old_r.coefs[0]
                    ell = ~ell
                    old_r = poly.one()
                    old_s = old_s * poly.__class__([ell])
            if old_r  == poly.one():
                return modpoly(old_s)
            else:
                return None

        def __str__(self):
            return str(self.k)

        def sqrt(self):

            if self == self.zero():
                return self.zero()

            if self.deg() == 0:
                sq = self.k.coefs[0].sqrt()
                if sq != None:
                    return modpoly([sq])

            if (self.group_order()/self.order()) % 2 == 1:
                return None

            pq = self.group_order()+1
            if (pq) %4 == 3:
                return self**((pq+1)/4)

            if pq %8 == 5:
                d = self**((pq-1)/4)
                if d == self.one():
                    return self**((3+pq)/8)
                else:
                    #d = -1
                    return (self*2)*((self*4)**((pq-5)/8))
            #no direct solution is known, do it the hard way.
            #find a non residue

            n = self.k
            z = self.random()
            while (z**((pq-1)/2)) != -self.one():
                z = self.random()

            Q = pq-1
            S = 0

            while Q%2 == 0:
                Q/=2
                S+=1
            
            c = z**Q
            R = self**((Q+1)/2)
            t = self**Q
            M = S
            while True:
                
                if t == self.one():
                    return R
                tmp = t
                for i in range(1,M):
                    if (t**(2**i)) == self.one():
                        break
                b = c**((int(2**(M-i-1))))
                R = R*b
                t = t*b*b
                c = b*b
                M = i
            return None #takes to long something wrong

    return modpoly

def Fpq(p,q,from_file = True):
    if q == 1:
        return Fp(p)
    FP = Fp(p)
    P = Polynomials(FP)
    if from_file:
        #Check if the irreducable is already known, if so, load it
        data = eval(open("irr.txt","r").read())
        if p in data and q in data[p]:
            coefs = data[p][q]
            coefs = [FP(c) for c in coefs]
            poly = P(coefs)
            return ModPoly(poly)

    #irreducable not known, so calculate one (can take a while)
    while True:
        poly = P.random(q)
        if poly.deg() != q:
            continue
        #make monic
        poly.coefs[-1] = poly.F.one()
        correct = True
        xpm = poly.Xn(1)
        x = xpm
        for d in range(q/2): #check for factors up to degree q/2
            xpm = xpm**p
            master = xpm - x
            if master.gcd(poly).deg() != 0:
                correct = False
                break
        if correct: #no factors found
            break
                                

    #save for later use
    if from_file:
        if p not in data:
            data[p] = {}
        data[p][q] = poly.coefs
        fp = open("irr.txt","w")
        import pprint
        s = pprint.pformat(data)
        fp.write(s)
        fp.close()
    return ModPoly(poly)
