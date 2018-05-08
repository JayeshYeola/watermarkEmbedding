import rsa
from PIL import Image
import pywt
import numpy
from scipy import linalg

T = []      # WaterMarked Image
X = [0.24]  # Random Scrambling Sequence
u = 3.72    # System Parameter for Scrambling
alpha = 71  # Amplification Factor
beta = 37   # Amplification Factor
B = []      # Scrambled Watermark
AlphaScaling = 0.2
host_image = 'panda'
watermark_image = 'watermark'
# C = numpy.ndarray(62500)    # Host Image
# Bw = numpy.ndarray(62500)   # Watermark
# C.shape = (250,250)
# Bw.shape = (250,250)
# Wfinal = numpy.ndarray(125 * 125)  # Watermark
# Wfinal.shape = (125, 125)
# SCactual = numpy.ndarray(125 * 125)
# SCactual.shape = (125, 125)


def RSAEncryption(X,u):
    (pubkey,privkey) = rsa.newkeys(512)
    message = str(X[0])+' '+str(u)
    R = rsa.encrypt(message, pubkey)
    # print "Encrypted Scrambling Parameters :" + R
    decrypt = rsa.decrypt(R, privkey)
    # print decrypt


def ReadWatermarkImage():
    im = Image.open(watermark_image+'.png')  # Can be many different formats.
    pix = im.load()
    ht,wdt = im.size
    print 'Water Mark Image: ', ht, wdt
    x = 0
    y = 0
    while x < ht:
        y = 0
        while y < wdt:
            # print pix[x,y]
            T.append(pix[x,y][0])
            y += 1
        x += 1
    return T


def ReadHostImage():
    hm = Image.open(host_image+'.jpg')  # Can be many different formats.
    pix = hm.load()
    x = 0
    y = 0
    ht, wdt = hm.size
    print 'Host Image: ', ht, wdt
    Temp = numpy.ndarray(ht*wdt)
    Temp.shape = (ht,wdt)
    # C.resize(Temp.size)
    # C.reshape(Temp.shape)
    # print C.shape, C.size
    while x < ht:
        y = 0
        while y < wdt:
            Temp[x, y] = pix[x, y][0]  # pix[x,y]
            # C.append(pix[x,y])
            y += 1
        x += 1
    # print Temp
    return Temp


def WriteImage(pixels, name):
    hm = Image.open(host_image+'.jpg')
    pix = hm.load()
    x = 0
    y = 0
    ht, wdt = hm.size

    wim = Image.new(hm.mode, hm.size)
    pixs = wim.load()
    while x < ht:
        y = 0
        while y < wdt:
            color = round(pixels[x,y])
            color = int(color%256)
            # print color
            pixs[x,y] = tuple([color,color,color])
            y += 1
        x += 1
    wim.save(name+'.png')


def GenerateScramblingSequence():
    i = 1
    while i < len(T):
        X.append(u*X[i-1]*(1-X[i-1]))
        # print X[i]
        i+=1
    # print max(X), min(X)
    # Normalize X
    j = 0
    while j < len(X):
        if round(beta * X[j]) < (beta * X[j]):
            X[j] = int((round(alpha*(beta*X[j]-round(beta*X[j])))) % 256)
        elif round(beta * X[j]) > (beta * X[j]):
            X[j] = int((round(alpha * (1 - beta * X[j] - round(beta * X[j])))) % 256)
        j += 1

def GenScrambledWatermark():
    i = 0

    while i < len(T):
        element = X[i] ^ T[i]  # [0], X[i] ^ T[i][1], X[i] ^ T[i][2]]
        B.append(element)
        i += 1

    im = Image.open(watermark_image+'.png')  # Can be many different formats.
    pix = im.load()
    ht, wdt = im.size
    x = 0
    y = 0
    count = 0
    hm2 = Image.new(im.mode,im.size)
    pixil = hm2.load()

    Bw = numpy.ndarray(ht * wdt)
    Bw.shape = (ht, wdt)

    while x < ht:
        y = 0
        while y < wdt:
            pixil[x,y] = tuple([B[count],B[count],B[count]])
            Bw[x,y] = B[count]
            count += 1
            y += 1
        x += 1
    hm2.save('scrambled_watermark.png')
    return Bw


def DWTofImage(C):
    coeffs = pywt.dwt2(C, 'haar')
    # print "coeff"
    # print coeffs
    #     cA, (cH, cV, cD) = coeffs
    '''| cA(LL) | cH(LH) |
    | cV(HL) | cD(HH)
    '''
    return coeffs

def InvDWTofImage(coeffs):
    Img = pywt.idwt2(coeffs,'haar')
    return Img

def DWTofCoeffImage(cA):
    coeffs_1 = pywt.dwt2(cA, 'haar')
    cA_1, (cH_1, cV_1, cD_1) = coeffs_1
    coeffs_2 = pywt.dwt2(cA_1, 'haar')
    cA_2, (cH_2, cV_2, cD_2) = coeffs_2
    coeffs_3 = pywt.dwt2(cA_2, 'haar')
    cA_3, (cH_3, cV_3, cD_3) = coeffs_3
    coeffs_4 = pywt.dwt2(cA_3, 'haar')
    cA_4, (cH_4, cV_4, cD_4) = coeffs_4
    return cA_1

# # Wfinal = Wt[:125]
# i = 0
# while i < 125:
#     j = 0
#     while j < 125:
#         Wfinal[i, j] = Wt[i, j]
#         if i == j:
#             SCactual[i, j] = Sc[i]
#         else:
#             SCactual[i, j] = 0
#         j += 1
#     i += 1
# print '------------------------------------------------'
# print len(Wfinal[0]), len(Wfinal)
# Snew = Sc + Alpha * Wfinal
# Uw, Sw, Vw = linalg.svd(Snew)
# SWactual = numpy.ndarray(125 * 125)
# SWactual.shape = (125, 125)
# i = 0
# while i < 125:
#     j = 0
#     while j < 125:
#         Wfinal[i, j] = Wt[i, j]
#         if i == j:
#             SWactual[i, j] = Sw[i]
#         else:
#             SWactual[i, j] = 0
#         j += 1
#     i += 1
# # print SWactual
# VTemp = Vc.transpose()
# LLnew = numpy.matmul(numpy.matmul(Uc, SWactual), VTemp)
# # print(LLnew)
# print '------------------------------------------------'
# print LLnew.shape
# coefficient = LLnew, (cH, cV, cD)
#
# ImageArray = pywt.idwt2(coefficient, 'haar')
# Image2 = numpy.ndarray(125 * 125, int)
# Image2.shape = (125, 125)
# i = 0
# while i < 125:
#     j = 0
#     while j < 125:
#         temp = round(ImageArray[i, j])
#         temp2 = temp % 256
#         # print temp,temp2
#         Image2[i, j] = temp2
#         j += 1
#     i += 1
# # print Image2
# i = 0
# while i < 125:
#     j = 0
#     while j < 125:
#         temp = round(ImageArray[i, j])
#         temp2 = temp % 256
#         # print temp,temp2
#         Image2[i, j] = temp2
#         j += 1
#     i += 1
#
# hm2 = Image.open('host_image.png')  # Can be many different formats.
# pix = hm2.load()
# x = 0
# y = 0
# while x < 125:
#     y = 0
#     while y < 125:
#         pix[x, y] = tuple([Image2[x, y], Image2[x, y], Image2[x, y]])  # pix[x,y]
#         # pix[x,y][1] = Image2[x, y]
#         # pix[x,y][2] = Image2[x, y]
#         y += 1
#     x += 1
# hm2.save('updated_host.png')
#

def main():
    RSAEncryption(X, u)
    print 'Completed 1'
    ReadWatermarkImage()
    print 'Completed 2'
    C = ReadHostImage()
    print 'Completed 3'
    GenerateScramblingSequence()
    print 'Completed 4'
    Bw = GenScrambledWatermark()
    print 'Completed 4'
    coeff = DWTofImage(C)
    print 'Completed 6'
    cA, (cH, cV, cD) = coeff
    coeffs_1 = pywt.dwt2(cA, 'haar')
    cA_1, (cH_1, cV_1, cD_1) = coeffs_1
    coeffs_2 = pywt.dwt2(cA_1, 'haar')
    cA_2, (cH_2, cV_2, cD_2) = coeffs_2
    coeffs_3 = pywt.dwt2(cA_2, 'haar')
    cA_3, (cH_3, cV_3, cD_3) = coeffs_3
    coeffs_4 = pywt.dwt2(cA_3, 'haar')
    cA_4, (cH_4, cV_4, cD_4) = coeffs_4

    Uc, Sc, Vc = linalg.svd(cA_3)
    # Scdia = numpy.diagflat(Sc)
    Uwd, Swd, Vwd = linalg.svd(Bw)
    # Swddia = numpy.diagflat(Swd)
    print Sc.shape, Swd.shape
    Snew = Sc + AlphaScaling * Swd[:20]
    Snewdia = numpy.diagflat(Snew)

    Uw, Sw, Vw = linalg.svd(Snewdia)
    ht= Sw.shape
    print ht
    # Swdia = numpy.diagflat(Sw)
    Swdia = numpy.identity(ht[0])
    VcT = Vc.transpose()

    LLtemp = Uc.dot(Swdia)
    LLnew = LLtemp.dot(VcT)

    mod = LLnew, (cH_3, cV_3, cD_3)
    LLnet = InvDWTofImage(mod)
    print LLnet.shape
    mod_co = LLnet, (cH_2, cV_2, cD_2)
    LLn = InvDWTofImage(mod_co)
    mod_coeff = LLn, (cH_1, cV_1, cD_1)
    LLImage = InvDWTofImage(mod_coeff)
    coeff_img = LLImage, (cH, cV, cD)
    Cw = InvDWTofImage(coeff_img)
    print Cw.shape
    WriteImage(Cw,'Scrambled')

if __name__ == '__main__':
    main()
