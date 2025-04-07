import numpy as np
from matplotlib import pyplot as plt
from exact.onetransmon.hamil import calc_eigs
from exact.util import exact_energy_a, exact_energy_b

# how different are the SWT energies and exact numeric for one qubit?
Ejs = np.arange(1, 70, 10)
k = 60
num_levels = 10
exact = np.zeros((len(Ejs), num_levels))
for i, Ej in enumerate(Ejs):
    vals = calc_eigs(Ej, ng=0, k=k)
    exact[i, :] = vals[:num_levels]

ma = [exact_energy_a(m, 1, Ejs) for m in range(5)]
mb = [exact_energy_b(m, 1, Ejs) for m in range(5)]
colors = ["b", "r", "g", "magenta", "orange"]
plt.gca().set_prop_cycle(color=colors)
plt.plot(Ejs, exact)

plt.gca().set_prop_cycle(color=colors)
for i in range(len(ma)):
    plt.plot(Ejs, ma[i], lw=0, marker="|", label=f"M a")
    plt.plot(Ejs, mb[i], lw=0, marker=".", label=f"M b")

plt.title(f"One transmon energies from matrix eigenvalue (solid), |=Mathieu a values, dot=|=Mathieu b values, k={k}")
plt.xlabel("Ej [Ec]")
plt.ylabel("En [Ec]")
plt.show()
