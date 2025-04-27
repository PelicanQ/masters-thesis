# Here I will test Numba's speedup for numpy operations like eig()
import numpy as np
from numba import jit
import timeit
from matplotlib import pyplot as plt
import cupy as cp
from cupyx.profiler import benchmark

# Here we if numpy eigh() is faster with numba? Parallel?

# simple number=3 eigh on random 3000x3000 matrix
# no jit, 10.3 9.2 7.8 7.15 7.3 7.5 7.7. Last 5 average to 7.5
# with jit, 7.3 7.0 7.0 7.5 7.2 average to 7.2
# Mayybe slightly faster but numpy is already fast.


def run(A):
    vals = cp.linalg.eigh(A)


N = 24000
print("Size:", N)
A = cp.random.rand(N, N)
A = A + A.T
t = benchmark(run, (A,), n_repeat=1, n_warmup=1)
print(t)
# run()
# t = timeit.timeit(run, number=1)
# print(t)
