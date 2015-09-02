from general import *


#Base classes
class Group():

    order_dividers = None
    def __init__(self):
        pass

    @classmethod
    def __iter__(cls):
        return cls.all()

    def __div__(self,other):
        return (self * (~other))

    def order(self):
        if self.order_dividers == None:
            n = self.group_order()
            primes = factor_primes(n)
            dividers = all_dividers(primes)
            dividers.sort()
            self.order_dividers = dividers
        else:
            dividers = self.order_dividers
        for d in dividers:
            if (self**d) == self.identety():
                return d
        return -1
    
    def __pow__(self,other):
        if other < 0:
            return ~(self**(-other)) #minus powers just inverse
        binrep = bin(other)[2:][::-1]

        res = self.identety()

        power = self
        for bit in binrep:
            if bit == "1":
                res*= power
            power  = power * power
        return res

    def __eq__(self,other):
        if other.__class__ != self.__class__:
            return False

        keys = self.__dict__.keys()
        for attr in keys:
            if attr in dir(self.__class__):
                continue #only instance variables
            if getattr(self,attr) != getattr(other,attr):
                return False
        return True


    def __ne__(self,other):
        return not(self == other)

    def __repr__(self):
        return str(self)


    #To write for a new group
    def __mul__(self):
        pass

    def __inverse__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def identety(cls):
        pass

    @classmethod
    def random(cls):
        pass

    #if finite:
    @classmethod
    def all(cls):
        return
        yield
    
    
class Field(Group):
    def __sub__(self,other):
        return self+(-other)

    def __pow__(self,other):
        if other < 0:
            return ~(self**(-other)) #minus powers just inverse
        binrep = bin(other)[2:][::-1]
        res = self.one()
        power = self
        for bit in binrep:
            if bit == "1":
                res*= power
            power  = power * power
        return res

    
    #To write for a new field (all of group, plus)
    def __add__(self):
        pass

    def __neg__(self):
        pass

    @classmethod
    def one(cls):
        pass

    @classmethod
    def zero(cls):
        pass
