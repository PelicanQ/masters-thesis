import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from os import path
from sim_store.sim_store import Store

# this shows that the ground level converges but slower for larger Ej
s = Store(
    path.abspath("./sweep_store.npy"),
    path.abspath("./sweep_keys.csv"),
    calc_dim=lambda k: 2 * k + 1,
)
kk = s.kk
Ejs = s.Ejs
s.shape()

Ej_idxs = [4, 10, 15, 20, 26, 35]
for idx, j in enumerate(Ej_idxs):
    # show global convergence of ground enery level
    plt.subplot(2, 3, idx + 1)
    p = s.get_level_k(j, 0)
    plt.plot(kk, p, marker=".")
    std = np.std(p[20:])
    plt.title(f"Ej={Ejs[j]}, std=1e{np.log10(std):.0f}", fontsize=9)

plt.xlabel("k")
plt.subplot(2, 3, 1)
plt.ylabel("E0(k)")
plt.suptitle("Absolute convergence of lowest energy level for one transmon")
plt.show()
