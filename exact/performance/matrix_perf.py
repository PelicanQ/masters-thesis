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


def aa():
    N = 24000
    print("Size:", N)
    A = cp.random.rand(N, N)
    A = A + A.T
    t = benchmark(run, (A,), n_repeat=1, n_warmup=1)
    print(t)


if __name__ == "__main__":
    x = [1000, 5000, 7000, 10000, 13000, 15000, 17000, 20000, 22000, 24000, 25000, 26000]
    lap = [0.064, 2.8, 6.7, 18, 39, 59, 87, 238, 543, 718, np.nan, np.nan]
    desk = [0.044, 1.5, 3.5, 9.8, 21, 31, 99, 166, 245, 335, np.nan, np.nan]
    rt = [0.023, 0.618, 1.6, 4.0, 7.8, 12, 17, 26, 34, 43, 49, 55]
    h2 = [0.010, 0.19, 0.4, 0.9, 1.8, 2.5, 3.6, 5.6, 7.3, 9.2, 10, 12]
    plt.plot(x, lap, label="laptop")
    plt.plot(x, desk, label="desktop")
    plt.plot(x, rt, label="5090")
    plt.plot(x, h2, label="H200")
    plt.legend()

    plt.show()
