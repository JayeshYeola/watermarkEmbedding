from scipy import linalg
import numpy as np
m, n = 9, 6
a = np.random.randn(m, n) + 1.j*np.random.randn(m, n)
print "a"
print a
U, s, Vh = linalg.svd(a)
print "shape"
print U.shape,s.shape, Vh.shape