# Here I will test Numba's speedup for numpy operations like eig()
import numpy as np
from numba import jit
import timeit
from matplotlib import pyplot as plt
import cupy as cp

# Here we if numpy eigh() is faster with numba? Parallel?

# simple number=3 eigh on random 3000x3000 matrix
# no jit, 10.3 9.2 7.8 7.15 7.3 7.5 7.7. Last 5 average to 7.5
# with jit, 7.3 7.0 7.0 7.5 7.2 average to 7.2
# Mayybe slightly faster but numpy is already fast.


# 5000x5000
# jit, 13.1 11.9 12.6 12.0
# jit parallel, 12.1 11.8 12.1
# @jit(parallell=False)
def run(A):
    vals = cp.linalg.eigh(A)


NN = [50, 100, 500, 1000, 2000, 4000, 6000, 8000, 10000, 13000, 15000, 17000, 20000, 22000, 25000]
times = []
for N in NN:
    print("Size:", N)
    A = cp.random.rand(N, N)
    A = A + A.T
    t = timeit.timeit(lambda: run(A), lambda: run(A), number=2)
    t /= 2
    times.append(t)
    del A
    cp.get_default_memory_pool().free_all_blocks()

plt.plot(NN, times)
plt.title("Time to diagonalize cupy.linalg.eigh()")
plt.ylabel("Time seconds")
plt.xlabel("N Matrix size (NxN)")

plt.show()
# run()
# t = timeit.timeit(run, number=1)
# print(t)
