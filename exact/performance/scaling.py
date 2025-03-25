import cupy as cp
import numpy as np
import timeit
import pandas as pd
from matplotlib import pyplot as plt

# here I will see how time of eigvalsh scales with matrix size for cupy (still time~size^4?)
#


def r(A: cp.ndarray):
    return cp.linalg.eigvalsh(A)


NN = np.concatenate(
    [
        # np.arange(10, 200, step=2),
        # np.arange(200, 400, step=4),
        # np.arange(400, 600, step=8),
        # np.arange(600, 800, step=10),
        # np.arange(800, 1200, step=14),
        # np.arange(1200, 1400, step=16),  # end A
        # np.arange(1400, 2000, step=14),  # B
        # np.arange(2000, 6000, step=500),  # C
        # np.arange(6000, 10000, step=1000),  # D
        # np.arange(10000, 16000, step=2000),  # E
        np.arange(16000, 20000, step=2000),  # F
    ]
)
NN = NN.astype(int, casting="safe")
# warmup. The first run is extra slow, probably due to caching of compiled code
r(cp.random.rand(10, 10))
times = []
for N in NN:
    A = np.random.rand(N, N)
    A = A + A.T
    A = cp.asarray(A)
    t = timeit.timeit(lambda: r(A), number=1)
    times.append(t)

print(times)
df = pd.DataFrame((NN, times))
df.to_csv("./gpu_timeF.csv", header=False, index=False)
plt.plot(NN, times, marker=".")
plt.show()
