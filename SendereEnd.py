import rsa
from PIL import Image


X = []
X.append('0')
u = '1'

def RSAEncryption(X,u):
    (pubkey,privkey) = rsa.newkeys(1024)
    message = X[0]+' '+u
    R = rsa.encrypt(message,pubkey)
    print R
    print 'TODO: Implement'
    decrypt = rsa.decrypt(R,privkey)
    print decrypt


def ReadImage():
    im = Image.open('watermark.png')  # Can be many different formats.
    pix = im.load()
    x = 250
    y = 250
    print im.size  # Get the width and hight of the image for iterating over
    print pix[x, y]  # Get the RGBA Value of the a pixel of an image
    # pix[x, y] = value  # Set the RGBA Value of the image (tuple)
    # im.save('watermark2.png')

# RSAEncryption(X,u)
ReadImage()