from scipy import linalg
import SendereEnd
import numpy as np
#m, n = 9, 6
#a = np.random.randn(m, n) + 1.j*np.random.randn(m, n)
#print "a"
#print a
LL=SendereEnd.DWTofImage()
Uc, Sc, Vc = linalg.svd(LL)
#print "shape"
#print Uc,Sc,Vc
Snew=Sc+SendereEnd.alpha*SendereEnd.T
Uw,Sw,Vw = linalg.svd(Snew)

