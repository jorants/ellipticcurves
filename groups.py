import random
from skeleton import *



#check is a point is on the curve
CHECK_CURVE = True

def random_prime_group(bits):
    p = generate_prime(bits)
    return ZpZ(p)

def random_non_smooth(bits):
    while True:
        p = generate_prime(bits-1)
        pp = p*2+1
        if is_prob_prime(pp):
            return  ZpZ(pp)



def ZpZ(p):
    class Z_PZ(Group):
        def __init__(self,k):
            self.k = k % p
            self.p = p

        @classmethod
        def group_order(cls):
            return p-1
            
        @classmethod
        def all(cls):
            for i in range(p):
                yield cls(i)

        @classmethod
        def __iter__(cls):
            return cls.all()
                
        @classmethod
        def identety(cls):
            return cls(1)

        @classmethod
        def random(cls):
            return cls(random.randrange(1,p))
        
        def __mul__(self,other):
            if other.__class__ == Z_PZ:
                return Z_PZ(self.k*other.k)
            elif other.__class__ == int:
                return Z_PZ(self.k*other)
            
        def __invert__(self):
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
            return Z_PZ(old_s)
        
        def __str__(self):
            return str(self.k)

    return Z_PZ



#makes an eliptic curve over a field
def elliptic_curve(field,d1,d0):
    if CHECK_CURVE and (field.char() == 2 or field.char() == 3 or (d1**3)*4+(d0**2)*27 == d1.zero()):
        raise ValueException("Not a proper curve")
    
    class Point_ec(Group):
        def __init__(self,x = None ,y = None):
            self.x = x
            self.y = y
            
            if CHECK_CURVE and self.x!= None and not(self.y*self.y == self.x*self.x*self.x+self.x*d1+d0):
                raise ValueError("Not on curve: %s" % str(self))

        @classmethod
        def identety(cls):
            return cls()

        @classmethod
        def all(cls):
            for x in field.all():
                P = cls.point_for_x(x)
                if P == None:
                    continue
                if P.y != field.zero():
                    yield ~P
                yield P

        found_Gorder = None

        @classmethod
        def group_order(cls):
            if cls.found_Gorder != None:
                return cls.found_Gorder
            #tmp solution: exhaustive search:
            total = 1 #infty
            for x in field.all():

                P = cls.point_for_x(x)
                if P == None:
                    continue
                if P.y == field.zero():
                    total+=1
                if P.y != field.zero():
                    total+=2
            cls.found_Gorder = total
            return total
            pass #TODO schoof

        @classmethod
        def point_for_x(cls,x):
            y2 = x*x*x+d1*x+d0
            y = y2.sqrt()
            if None == y:
                return None
            return cls(x,y)

        @classmethod     
        def random(cls):
            x = field.random()
            p = cls.point_for_x(x)
            while None == p:
                x = field.random()
                p = cls.point_for_x(x)
            if random.randrange(0,2) == 0:
                p = ~p
            return p
        
        def __mul__(self,other):
            if self == ~other:
                return Point_ec() #infty

            neg = ~other
            
            
            if self == Point_ec(): #identtety
                return other
            
            if other == Point_ec():#identtety
                return self

            three = field.one()+ field.one() + field.one()
            two = field.one()+ field.one()

            if self == other:

                ll = (three*self.x*self.x+d1)/(two*self.y)
                v = (-self.x*self.x*self.x + d1 * self.x + two * d0)/(two*self.y)
            else:

                ll = (other.y - self.y ) / (other.x - self.x )
                v = (self.y*other.x - other.y*self.x)/(other.x - self.x)


            return Point_ec(ll*ll-self.x-other.x, -ll*ll*ll+ll*(self.x+other.x)-v )
        
        def __invert__(self):
            if self.x == None:
                return Point_ec()
            else:
                return Point_ec(self.x,-self.y)
            pass

        def __str__(self):
            if self.x == None:
                return "oo"
            return "(%s,%s)"%(str(self.x),str(self.y))

    return Point_ec


