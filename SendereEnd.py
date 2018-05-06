import rsa
from PIL import Image
import pywt
import numpy

T = []      # WaterMarked Image
X = [0.47]  # Random Scrambling Sequence
u = 3.72    # System Parameter for Scrambling
alpha = 68  # Amplification Factor
beta = 37   # Amplification Factor
B = []      # Scrambled Watermark
C = numpy.ndarray(62500)    # Host Image
Bw = numpy.ndarray(62500,type([0,1,2]))   # Watermark
C.shape = (250,250)
Bw.shape = (250,250)

def RSAEncryption(X,u):
    (pubkey,privkey) = rsa.newkeys(512)
    message = str(X[0])+' '+str(u)
    R = rsa.encrypt(message, pubkey)
    print "Encrypted Scrambling Parameters :" + R
    decrypt = rsa.decrypt(R, privkey)
    print decrypt


def ReadWatermarkImage():
    im = Image.open('watermark.png')  # Can be many different formats.
    pix = im.load()
    x = 0
    y = 0
    while x < 250:
        y = 0
        while y < 250:
            T.append(pix[x,y])
            y += 1
        x += 1
    print len(T)


def ReadHostImage():
    hm = Image.open('host_image.png')  # Can be many different formats.
    pix = hm.load()
    x = 0
    y = 0
    while x < 250:
        y = 0
        while y < 250:
            C[x,y] = pix[x, y][0]  # pix[x,y]
            # C.append(pix[x,y])
            y += 1
        x += 1
    print len(C)

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
        # print(X[i])
        # print (X[i] ^ T[i][0])
        element = [X[i] ^ T[i][0], X[i] ^ T[i][1], X[i] ^ T[i][2]]
        B.append(element)
        i += 1
    x = 0
    y = 0
    count = 0
    while x < 250:
        y = 0
        while y < 250:
            Bw[x,y] = B[count]
            count += 1
            y += 1
        x += 1
    print(Bw)


def DWTofImage():
    coeffs = pywt.dwt2(C, 'haar')
    cA, (cH, cV, cD) = coeffs
    print cA
    print '------------------------------------------'
    print cH
    print '------------------------------------------'
    print cV
    print '------------------------------------------'
    print cD
    print '------------------------------------------'
    '''| cA(LL) | cH(LH) |
    | cV(HL) | cD(HH)
    '''


RSAEncryption(X, u)
ReadWatermarkImage()
ReadHostImage()
GenerateScramblingSequence()
GenScrambledWatermark()
DWTofImage()