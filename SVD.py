from scipy import linalg
import SendereEnd
import numpy

LL = SendereEnd.main()
# LL=SendereEnd.DWTofImage()
Uc, Sc, Vc = linalg.svd(LL)
print "Sc :"
# print len(Sc), Sc[0]
Alpha = 0.1
Wt= SendereEnd.Bw
Wfinal = numpy.ndarray(125*125)   # Watermark
Wfinal.shape = (125,125)
# Wfinal = Wt[:125]
i = 0
while i < 125:
    j=0
    while j < 125:
        Wfinal[i,j] = Wt[i,j]
        j += 1
    i += 1
print '------------------------------------------------'
print len(Wfinal[0]), len(Wfinal)
Snew = type(Sc)
Snew=Sc+Alpha*Wfinal
print '------------------------------------------------'
print Snew
Uw,Sw,Vw = linalg.svd(Snew)
LLnew = linalg
