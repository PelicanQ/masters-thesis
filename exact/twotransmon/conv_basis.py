# Will we see better eigenvalue convergence if we change total Hamiltonian into bare transmon basis.
# Perhaps increasing Ej wont slow down convergence anymore?
# I think strong Ej no longer will, but strong Eint will still. In that case we only need to worry about large Eint
from .hamil_alt import alt_calc_eig, clever_calc_eig
from matplotlib import pyplot as plt
import numpy as np
from sim_store.analysis.plot import grid3d

kk = [5, 7, 9, 11, 12, 15, 18, 20, 24, 28, 32, 35]
# kk = [5, 7, 9, 11, 12, 13, 14]

coll = []
Ejs = [1, 10, 500, 1000]
levels = [1, 3, 20, 40]
finalss = []
for j, Ej in enumerate(Ejs):
    E = np.zeros(shape=(4, len(kk)))
    for i, k in enumerate(kk):
        vals = clever_calc_eig(Ej=Ej, Eint=1, k=k)
        E[:, i] = vals[levels]
    finals = E[:, -1]
    finalss.append(finals)
    E = np.transpose(E.T - finals)  # every row relative to its last value
    coll.append(E)

grid3d(
    kk,
    coll,
    Ejs,
    "k",
    "En(k)",
    [f"E{level}=?" for level in levels],
    "Ej",
    "Levels 2T, clever calc, std from k=15, Eint=1",
    ".",
    std=5,
)
