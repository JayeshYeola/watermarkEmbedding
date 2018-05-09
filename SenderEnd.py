import rsa
from Crypto.PublicKey import RSA
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
AlphaScaling = 1
host_image = 'cat.png'
watermark_image = 'watermark_small.png'


def RSAEncryption(X,u):
    key = RSA.generate(1024)
    f = open('mykey.pem', 'w')
    f.write(key.export_key('PEM'))
    f.close()

    f = open('mykey.pem', 'r')
    key = RSA.import_key(f.read())
    (pubkey,privkey) = rsa.newkeys(512)

    message = str(X[0])+' '+str(u)
    R = rsa.encrypt(message, pubkey)
    # print "Encrypted Scrambling Parameters :" + R
    decrypt = rsa.decrypt(R, privkey)
    keys = open('public_key.txt','w')
    data = 'Size: 512,text: '+R+'}\n'
    keys.write(data)
    keys.close()
    # print decrypt


def ReadWatermarkImage():
    im = Image.open(watermark_image)  # Can be many different formats.
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
    hm = Image.open(host_image)  # Can be many different formats.
    pix = hm.load()
    x = 0
    y = 0
    ht, wdt = hm.size
    # print 'Host Image: ', ht, wdt
    Temp = numpy.ndarray(ht*wdt)
    Temp.shape = (ht,wdt)
    while x < ht:
        y = 0
        while y < wdt:
            Temp[x, y] = pix[x, y][0]
            y += 1
        x += 1
    return Temp


def WriteImage(pixels, name):
    hm = Image.open(host_image)
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

    im = Image.open(watermark_image)  # Can be many different formats.
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
    return cA_4

def main():
    RSAEncryption(X, u)
    ReadWatermarkImage()
    C = ReadHostImage()
    GenerateScramblingSequence()
    Bw = GenScrambledWatermark()
    coeff = DWTofImage(C)
    cA, (cH, cV, cD) = coeff
    coeffs_1 = pywt.dwt2(cA, 'haar')
    cA_1, (cH_1, cV_1, cD_1) = coeffs_1
    coeffs_2 = pywt.dwt2(cA_1, 'haar')
    cA_2, (cH_2, cV_2, cD_2) = coeffs_2
    coeffs_3 = pywt.dwt2(cA_2, 'haar')
    cA_3, (cH_3, cV_3, cD_3) = coeffs_3
    coeffs_4 = pywt.dwt2(cA_3, 'haar')
    cA_4, (cH_4, cV_4, cD_4) = coeffs_4

    Uc, Sc, Vc = linalg.svd(cA_4)
    # Scdia = numpy.diagflat(Sc)
    Uwd, Swd, Vwd = linalg.svd(Bw)
    # Swddia = numpy.diagflat(Swd)
    size = Sc.shape
    sizeswd = Swd.shape
    if sizeswd[0] < size[0]:
        Sc[:sizeswd[0]] = Sc[:sizeswd[0]] + AlphaScaling * Swd[:sizeswd[0]]
    else:
        Sc[:size[0]] = Sc[:size[0]] + AlphaScaling * Swd[:size[0]]
    Snewdia = numpy.diagflat(Sc)

    Uw, Sw, Vw = linalg.svd(Snewdia)
    ht= Sw.shape
    # print ht
    # Swdia = numpy.diagflat(Sw)
    Swdia = numpy.eye(ht[0])
    # print Swdia
    VcT = Vc.transpose()

    LLtemp = Uc.dot(Swdia)
    LLnew = LLtemp.dot(VcT)

    mad = LLnew, (cH_4, cV_4, cD_4)
    LLmod = InvDWTofImage(mad)
    mod = LLmod, (cH_3, cV_3, cD_3)
    LLnet = InvDWTofImage(mod)
    # print LLnet.shape
    mod_co = LLnet, (cH_2, cV_2, cD_2)
    LLn = InvDWTofImage(mod_co)
    mod_coeff = LLn, (cH_1, cV_1, cD_1)
    LLImage = InvDWTofImage(mod_coeff)
    coeff_img = LLImage, (cH, cV, cD)
    Cw = InvDWTofImage(coeff)
    # print Cw.shape
    WriteImage(Cw,'Scrambled')

if __name__ == '__main__':
    main()
