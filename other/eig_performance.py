import numpy as np
from matplotlib import pyplot as plt
import cupy as cp
import timeit

sizes = np.round(np.logspace(1, 4, 10, base=10)).astype(int)
times = []


def run(size: int):
    A = cp.random.rand(size, size)
    cp.linalg.eigh(A)
    return


for size in sizes:
    t = timeit.timeit(lambda: run(size), setup=lambda: run(size), number=1)
    times.append(t)
plt.semilogy(sizes, times)
plt.ylabel("Time (s)")
plt.xlabel("Matrix size")
plt.title("Time to diagonalize with CuPy on laptop")
plt.show()
