import numpy as np
from matplotlib import pyplot as plt
from analysis.discover import make_hoverax
import itertools
from exact.util import exact_energy, omega_alphas

# what is the net number of levels below?
Ej1s = np.arange(30, 100, 1)
Ej2s = np.arange(30, 140, 1)
Ej3 = 50
balance_zzz = np.zeros(dtype=int, shape=(len(Ej1s), len(Ej2s)))
balance_zz = np.zeros(dtype=int, shape=(len(Ej1s), len(Ej2s)))


def sorted_vals(Ej1, Ej2, Ej3):
    """Give the sorted bare energies for 3 transmons"""
    vals1 = [exact_energy(m, 1, Ej1) for m in range(4)]
    vals2 = [exact_energy(m, 1, Ej2) for m in range(4)]
    vals3 = [exact_energy(m, 1, Ej3) for m in range(4)]
    levels = []
    sortvals1 = np.sort(vals1)
    sortvals2 = np.sort(vals2)
    sortvals3 = np.sort(vals3)
    sortvals1 = sortvals1 - sortvals1[0]
    sortvals2 = sortvals2 - sortvals2[0]
    sortvals3 = sortvals3 - sortvals3[0]
    ee = [[], [], []]
    for comb in itertools.product(range(3), repeat=3):
        n1 = comb[0]
        n2 = comb[1]
        n3 = comb[2]
        if sum(comb) < 3 and sum(comb) != 0:
            ee[sum(comb) - 1].append(((n1, n2, n3), sortvals1[n1] + sortvals2[n2] + sortvals3[n3]))

    etup = [None, None, None]
    for i, e in enumerate(ee):
        esort = sorted(e, key=lambda item: item[1])
        states = tuple([item[0] for item in esort])
        etup[i] = states
    etup = tuple(etup)[:-1]
    return etup


uniq: set[tuple] = set()
for i, Ej1 in enumerate(Ej1s):
    for j, Ej2 in enumerate(Ej2s):
        perm = sorted_vals(Ej1, Ej2, Ej3)
        # print(perm)
        uniq.add(perm)
print(len(uniq))
# for s in uniq:
# print(s)
# print("\n")


Ej2grid, Ej1grid = np.meshgrid(Ej2s, Ej1s)
o3, _ = omega_alphas(1, Ej3, True)
o1, _ = omega_alphas(1, Ej1grid, True)
o2, _ = omega_alphas(1, Ej2grid, True)
o2primgrid = o2 - (o3 + o1) / 2
detunegrid = o1 - o3

m = np.zeros_like(o2primgrid)
for i in range(o2primgrid.shape[0]):
    for j in range(o2primgrid.shape[1]):
        m[i, j] = o2primgrid[i, j] > abs(detunegrid[i, j] / 2)
        # perm = sorted_vals(Ej1, Ej2, Ej3)
        # uniq.add(perm)


plt.pcolormesh(o2primgrid, detunegrid, m)

plt.xlabel("o2 prim [-alpha]")
plt.ylabel("d13 [-alpha]")
plt.title("Yani")
plt.xlim(-10, 10)
plt.ylim(-8, 8)


plt.show()
