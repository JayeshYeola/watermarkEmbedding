import rsa
from PIL import Image
import pywt
import numpy

T = []      # WaterMarked Image
X = [0.24]  # Random Scrambling Sequence
u = 3.72    # System Parameter for Scrambling
alpha = 71  # Amplification Factor
beta = 37   # Amplification Factor
B = []      # Scrambled Watermark
C = numpy.ndarray(62500)    # Host Image
Bw = numpy.ndarray(62500)   # Watermark
C.shape = (250,250)
Bw.shape = (250,250)

def RSAEncryption(X,u):
    (pubkey,privkey) = rsa.newkeys(512)
    message = str(X[0])+' '+str(u)
    R = rsa.encrypt(message, pubkey)
    # print "Encrypted Scrambling Parameters :" + R
    decrypt = rsa.decrypt(R, privkey)
    # print decrypt


def ReadWatermarkImage():
    im = Image.open('whatermark2.png')  # Can be many different formats.
    pix = im.load()
    ht,wdt = im.size
    print ht, wdt
    x = 0
    y = 0
    while x < ht:
        y = 0
        while y < wdt:
            # print pix[x,y]
            T.append(pix[x,y][0])
            y += 1
        x += 1
    print len(T)
    return T


def ReadHostImage():
    hm = Image.open('host_image.png')  # Can be many different formats.
    pix = hm.load()
    x = 0
    y = 0
    ht, wdt = hm.size
    print ht, wdt
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
    print len(Temp)

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
    im = Image.open('whatermark2.png')  # Can be many different formats.
    pix = im.load()
    x = 0
    y = 0
    ht, wdt = im.size
    print ht, wdt
    Temp2 = numpy.ndarray(ht*wdt)
    Temp2.shape = (ht,wdt)
    while i < len(T):
        # print(X[i])
        # print (X[i] ^ T[i][0])
        element = X[i] ^ T[i] # [0], X[i] ^ T[i][1], X[i] ^ T[i][2]]
        # print element, X[i], T[i]
        B.append(element)
        i += 1
    x = 0
    y = 0
    count = 0
    hm2 = Image.new(im.mode,im.size)
    pixil = hm2.load()
    while x < ht:
        y = 0
        while y < wdt:
            # Bw[x,y] = B[count]
            pixil[x,y] = tuple([B[count],B[count],B[count]])
            count += 1
            y += 1
        x += 1
    # print(Bw)
    hm2.save('updated_watermark.png')
    return Temp2


def DWTofImage():
    coeffs = pywt.dwt2(C, 'haar')
    print "coeff"
    # print coeffs
    #     cA, (cH, cV, cD) = coeffs
    '''| cA(LL) | cH(LH) |
    | cV(HL) | cD(HH)
    '''
    return coeffs

def main():
    RSAEncryption(X, u)
    ReadWatermarkImage()
    ReadHostImage()
    GenerateScramblingSequence()
    GenScrambledWatermark()
    coeff = DWTofImage()
    return coeff
