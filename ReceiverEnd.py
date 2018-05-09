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
AlphaScaling = 1
host_image = 'cat.png'
watermark_image = 'watermark_small.png'
scrambled_image = 'Scrambled.png'

def RSADecryption():
    keys = open('public_key.txt','r')
    data = keys.readline()
    print data


def ReadImage(name):
    hm = Image.open(name)  # Can be many different formats.
    pix = hm.load()
    x = 0
    y = 0
    ht, wdt = hm.size
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
    hm = Image.open(watermark_image)
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


def main():
    RSADecryption()
    C = ReadImage(host_image)
    Cw = ReadImage(scrambled_image)
    W = ReadImage(watermark_image)

    coeffs_0 = pywt.dwt2(C, 'haar')
    cA, (cH, cV, cD) = coeffs_0
    coeffs_1 = pywt.dwt2(cA, 'haar')
    cA_1, (cH_1, cV_1, cD_1) = coeffs_1
    coeffs_2 = pywt.dwt2(cA_1, 'haar')
    cA_2, (cH_2, cV_2, cD_2) = coeffs_2
    coeffs_3 = pywt.dwt2(cA_2, 'haar')
    cA_3, (cH_3, cV_3, cD_3) = coeffs_3
    coeffs_4 = pywt.dwt2(cA_3, 'haar')
    cA_4, (cH_4, cV_4, cD_4) = coeffs_4

    coeffsw_0 = pywt.dwt2(C, 'haar')
    cwA, (cwH, cwV, cwD) = coeffsw_0
    coeffsw_1 = pywt.dwt2(cwA, 'haar')
    cwA_1, (cwH_1, cwV_1, cwD_1) = coeffsw_1
    coeffsw_2 = pywt.dwt2(cwA_1, 'haar')
    cwA_2, (cwH_2, cwV_2, cwD_2) = coeffsw_2
    coeffsw_3 = pywt.dwt2(cwA_2, 'haar')
    cwA_3, (cwH_3, cwV_3, cwD_3) = coeffsw_3
    coeffsw_4 = pywt.dwt2(cwA_3, 'haar')
    cwA_4, (cwH_4, cwV_4, cwD_4) = coeffsw_4

    Ucw, Scw, Vcw = linalg.svd(cwA_2)
    Uh, Sh, Vh = linalg.svd(cA_2)
    Uw, Sw, Vw = linalg.svd(W)
    Scwdia = numpy.diagflat(Scw)
    Vw = Vw.transpose()
    LLnewt = Uw.dot(Scwdia)
    LLnew1 = LLnewt.dot(Vw)
    Wdnew = (LLnew1 - Sw)/AlphaScaling
    # print Wdnew.shape
    WriteImage(Wdnew,'Recovered')


if __name__ == '__main__':
    main()
