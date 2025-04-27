import cupy as cp
import numpy as np
import timeit
import pandas as pd
from matplotlib import pyplot as plt

# here I will see how time of eigvalsh scales with matrix size for cupy (still time~size^4?)


def gpu(A: cp.ndarray):
    return cp.linalg.eigvalsh(A)


def cpu(A: np.ndarray):
    return np.linalg.eigvalsh(A)


NN = np.linspace(10, 5000, 20).astype(int)
NNe = np.linspace(5000, 10000, 4).astype(int)
NNe = np.concatenate([NN, NNe])
# # warmup. The first run is extra slow, probably due to caching of compiled code
# tC = np.zeros((len(NN),))
# tG = np.zeros((len(NN),))
# for i, N in enumerate(NN):
#     print(i)
#     A = np.random.rand(N, N)
#     C = A + A.T
#     G = cp.asarray(A)

#     t_c = timeit.timeit(lambda: cpu(C), setup=lambda: cpu(C), number=2) / 2
#     t_g = timeit.timeit(lambda: gpu(G), setup=lambda: gpu(G), number=2) / 2

#     tC[i] = t_c
#     tG[i] = t_g

# np.save("CPUe.npy", tC)
# np.save("GPUe.npy", tG)
tC = np.load("CPU.npy")
tG = np.load("GPU.npy")
tCe = np.load("CPUe.npy")
tGe = np.load("GPUe.npy")

totalC = np.concatenate([tC, tCe])
totalG = np.concatenate([tG, tGe])

plt.plot(NNe, totalC, marker=".", label="CPU")
plt.plot(NNe, totalG, marker=".", label="GPU")
plt.legend()
plt.title("Time to find eigenvalues")
plt.xlabel("Matrix size")
plt.ylabel("Time (seconds)")
plt.show()
