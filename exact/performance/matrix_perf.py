# Here I will test Numba's speedup for numpy operations like eig()
import numpy as np
from numba import jit
import timeit

# Here we if numpy eigh() is faster with numba? Parallel?
N = 5000

# simple number=3 eigh on random 3000x3000 matrix
# no jit, 10.3 9.2 7.8 7.15 7.3 7.5 7.7. Last 5 average to 7.5
# with jit, 7.3 7.0 7.0 7.5 7.2 average to 7.2
# Mayybe slightly faster but numpy is already fast.


# 5000x5000
# jit, 13.1 11.9 12.6 12.0
# jit parallel, 12.1 11.8 12.1
# @jit(parallell=False)
def run():
    A = np.random.rand(N, N)
    A = A + A.T
    A = np.array(A, order="F")

    vals = np.linalg.eigh(A)


# run()
# t = timeit.timeit(run, number=1)
# print(t)
