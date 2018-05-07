from scipy import linalg
import SendereEnd
import numpy
import pywt

coef = SendereEnd.main()
cA, (cH, cV, cD) = coef
# LL=SendereEnd.DWTofImage()
print 'cA is : '
print cA.shape
LL = cA
Uc, Sc, Vc = linalg.svd(LL)
print "Sc :"
print Sc.shape,
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
Snew = type(Wfinal)
Snew=Sc+Alpha*Wfinal
print '------------------------------------------------'
print 'SNew Shape:' , Snew.shape
Uw,Sw,Vw = linalg.svd(Snew)
print Sw
print Sw.shape, 'Uc shape', Uc.shape
Temp = numpy.ndarray(125*125)
Temp.shape = (125,125)

print 'Temp Shape is :', Temp.shape
Vcdash = Vc.transpose()
print 'Vcdash shape is :', Vcdash.shape,  type(Vcdash)
Temp = numpy.matmul(Uc, Sw)
print '------------------------------------------------'
print 'Temp is :' , Temp.shape
LLnew = numpy.matmul(Temp,Vcdash)
print LLnew
print '------------------------------------------------'
print type(LLnew), LLnew.shape, cH.shape, cV.shape, cD.shape
# print LLnew
# LLnew.reshape(125,125)
# print cH
coeffs = LLnew, (cH, cV, cD)
# print coeffs
iamge = pywt.idwt2(coeffs,'haar')
print iamge
