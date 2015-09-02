from fields import *
F = Fpq(5,2)
p = 5

for pp in F.all():
    print "-------------- %i" % pp.order()
    if (pp.group_order()/pp.order()) % 2 == 0:
        print pp
        print pp.sqrt()
        for k in F.all():
            if pp== k*k:
                print k
