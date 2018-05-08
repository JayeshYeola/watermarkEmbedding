from scipy import linalg
import SendereEnd
import numpy
import pywt
from PIL import Image

coeff = SendereEnd.main()
cA, (cH, cV, cD) = coeff
# LL=SendereEnd.DWTofImage()
Uc, Sc, Vc = linalg.svd(cA)
Alpha = 0.2
Wt= SendereEnd.Bw
Wfinal = numpy.ndarray(125*125)   # Watermark
Wfinal.shape = (125,125)
SCactual = numpy.ndarray(125*125)
SCactual.shape = (125,125)

# Wfinal = Wt[:125]
i = 0
while i < 125:
    j=0
    while j < 125:
        Wfinal[i,j] = Wt[i,j]
        if i==j:
            SCactual[i,j] = Sc[i]
        else:
            SCactual[i,j] = 0
        j += 1
    i += 1
print '------------------------------------------------'
print len(Wfinal[0]), len(Wfinal)
Snew=Sc+Alpha*Wfinal
Uw,Sw,Vw = linalg.svd(Snew)
SWactual = numpy.ndarray(125*125)
SWactual.shape = (125,125)
i=0
while i < 125:
    j=0
    while j < 125:
        Wfinal[i,j] = Wt[i,j]
        if i==j:
            SWactual[i,j] = Sw[i]
        else:
            SWactual[i,j] = 0
        j += 1
    i += 1
# print SWactual
VTemp = Vc.transpose()
LLnew = numpy.matmul(numpy.matmul(Uc,SWactual),VTemp)
# print(LLnew)
print '------------------------------------------------'
print LLnew.shape
coefficient = LLnew, (cH, cV, cD)

ImageArray = pywt.idwt2(coefficient, 'haar')
Image2 = numpy.ndarray(125*125,int)
Image2.shape = (125,125)
i=0
while i < 125:
    j=0
    while j < 125:
        temp = round(ImageArray[i,j])
        temp2 = temp%256
        # print temp,temp2
        Image2[i,j] = temp2
        j += 1
    i += 1
# print Image2
i=0
while i < 125:
    j=0
    while j < 125:
        temp = round(ImageArray[i,j])
        temp2 = temp%256
        # print temp,temp2
        Image2[i,j] = temp2
        j += 1
    i += 1

hm2 = Image.open('host_image.png')  # Can be many different formats.
pix = hm2.load()
x = 0
y = 0
while x < 125:
    y = 0
    while y < 125:
        pix[x,y] = tuple([Image2[x, y], Image2[x, y], Image2[x, y]])  # pix[x,y]
        # pix[x,y][1] = Image2[x, y]
        # pix[x,y][2] = Image2[x, y]
        y += 1
    x += 1
hm2.save('updated_host.png')
