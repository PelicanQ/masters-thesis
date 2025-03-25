import numpy as np
import cupy as cp
import pandas as pd
import timeit

# Here I show how cupy is faster than numpy

# N = 10000
# A = np.random.random((N, N))
# A = A + A.T
# np.save("mat2.npy", A)
# Test: One fixed 6000x6000 symmetric float matrix,
# Just numpy.linalg.eigvalsh(): 15 14.4 14.0
# Just numpy.linalg.eigvalsh(): 2.2 2.2 2.3

# On the same matrix
# numpy.linalg.eigh(): 28 25 26
# cupy.linalg.eigh() 2.2 2.2 2.2

# Now 10000x10000
# numpy eigh()) 91 92
# cupy eigh()) 9.6 9.4 9.7

B = np.load("mat2.npy")
# B = cp.asarray(B)
print(B.shape)


def run():
    vals = np.linalg.eigh(B)
    # vals = cp.linalg.eigh(B)


# run()
t = timeit.timeit(run, number=1)
print(t)
