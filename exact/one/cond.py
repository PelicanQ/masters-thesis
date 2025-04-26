# here we see if condition numner correlates with the slower convergence at higher Ej
from matplotlib import pyplot as plt
from .hamil import calc_cond
import numpy as np

Ejs = np.logspace(0, 3, num=100, base=10)
kk = [5, 10, 20, 30, 40]
d = np.zeros(shape=(len(kk), len(Ejs)))  # k, Ej
conds1 = []
conds2 = []
conds3 = []
conds = []
for i, Ej in enumerate(Ejs):
    for j, k in enumerate(kk):
        c = calc_cond(ng=0, Ej=Ej, k=k)
        d[j, i] = c

for i, k in enumerate(kk):
    plt.loglog(Ejs, d[i, :], label=f"k={k}")

plt.xlabel("Ej")
plt.ylabel("Condition number")
plt.title("Condition number of 1T Hamiltonian vs Ej, ng=0")
plt.legend()
plt.show()
