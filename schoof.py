import fields



def div_polyset(field,polyring,d0,d1):
    y2  = polyring.Xn(3) + polyring.Xn(1)*d1 + polyring.one()*d0

    class division_poly(fields.Polynomials):
        def __init__(self,coefs,ymul = 0):
            self.field = field
            self.polyring = polyring
            self.poly = polyring(coefs)
            self.y  = ymul % 2
            y2mul = ymul/2
            if y2mul>0:
                rest = y2**y2mul
                self.poly = self.poly*rest

        def division_polys(n):
            phi = []
            phi.append(division_poly(polyring.zero()))
            phi.append(division_poly(polyring.one()))
            phi.append(division_poly(polyring.zero()))            
    return division_poly


    
