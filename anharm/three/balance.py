import numpy as np
from matplotlib import pyplot as plt
from analysis.discover import make_hoverax
from matplotlib import colors
import itertools
from exact.util import exact_energy, to_omega_grid
from matplotlib.ticker import MaxNLocator

# what is the net number of levels below?
Ej1s = np.arange(30, 100, 0.5)
Ej2s = np.arange(30, 140, 0.5)
Ej3 = 50
balance_zzz = np.zeros(dtype=int, shape=(len(Ej1s), len(Ej2s)))
balance_zz = np.zeros(dtype=int, shape=(len(Ej1s), len(Ej2s)))


def sorted_vals(Ej1, Ej2, Ej3):
    """Give the sorted bare energies for 3 transmons"""
    vals1 = [exact_energy(m, 1, Ej1) for m in range(4)]
    vals2 = [exact_energy(m, 1, Ej2) for m in range(4)]
    vals3 = [exact_energy(m, 1, Ej3) for m in range(4)]
    levels = []
    for comb in itertools.product(range(5), repeat=3):
        n1 = comb[0]
        n2 = comb[1]
        n3 = comb[2]
        sortvals1 = np.sort(vals1)
        sortvals2 = np.sort(vals2)
        sortvals3 = np.sort(vals3)
        sortvals1 = sortvals1 - sortvals1[0]
        sortvals2 = sortvals2 - sortvals2[0]
        sortvals3 = sortvals3 - sortvals3[0]
        if sum(comb) < 4:
            levels.append(((n1, n2, n3), sortvals1[n1] + sortvals2[n2] + sortvals3[n3]))
    levels = sorted(levels, key=lambda item: item[1])
    return levels


def conf_zzz(d12, d23):
    o3 = 0
    o2 = d23
    o1 = d12 + o2
    return [
        (2, 0, 0, 2 * o1 + alpha),
        (0, 2, 0, 2 * o2 + alpha),
        (0, 0, 2, 2 * o3 + alpha),
        (1, 0, 1, o1 + o3),
        (0, 1, 1, o2 + o3),
        (1, 1, 0, o1 + o2),
    ]


def conf_zzz(d12, d23):
    o3 = 0
    o2 = d23
    o1 = d12 + o2
    return [
        (3, 0, 0, 3 * o1 + 3 * alpha),
        (0, 3, 0, 3 * o2 + 3 * alpha),
        (0, 0, 3, 3 * o3 + 3 * alpha),
        (0, 1, 2, o2 + 2 * o3 + alpha),
        (0, 2, 1, -2 * d12 - (d12 + d23) - 2 * alpha),
        (1, 2, 0, -2 * d12 - 2 * alpha),
        (2, 1, 0, -d12 - 2 * alpha),
        (2, 0, 1, -(d12 + d23) - 2 * alpha),
        (1, 0, 2, -2 * (d12 + d23) - 2 * alpha),
        (1, 1, 1, -2 * d12 - d23 - 3 * alpha),
    ]


def count_net_below(levels, start: int, exc: int):
    above = 0
    for t in range(start + 1, len(levels)):
        if sum(levels[t][0]) == exc:
            above += 1
    below = 0
    for t in range(start - 1, -1, -1):
        if sum(levels[t][0]) == exc:
            below += 1
    return below - above


for i, Ej1 in enumerate(Ej1s):
    print(i)
    for j, Ej2 in enumerate(Ej2s):
        levels = sorted_vals(Ej1, Ej2, Ej3)

        for k in range(len(levels)):
            if levels[k][0] == (1, 1, 1):
                break
        balance_zzz[i, j] = count_net_below(levels, k, 3)

        for k in range(len(levels)):
            if levels[k][0] == (1, 0, 1):
                break
        two_below = count_net_below(levels, k, 2)

        for k in range(len(levels)):
            if levels[k][0] == (1, 0, 0):
                break
        one_below_100 = count_net_below(levels, k, 1)

        for k in range(len(levels)):
            if levels[k][0] == (0, 0, 1):
                break
        one_below_001 = count_net_below(levels, k, 1)
        balance_zz[i, j] = two_below - one_below_100 - one_below_001

o2prim_grid, d13_grid = to_omega_grid(Ej1s, Ej2s, Ej3)

colorz2 = plt.cm.Oranges(np.linspace(0.2, 1, 5))
white = [1, 1, 1, 1]
colorz = np.vstack((plt.cm.Blues_r(0.5), colorz2))
cmap = colors.ListedColormap(colorz)

# Define the boundaries between values:
bounds = np.arange(-2, 11, 2)
norm = colors.BoundaryNorm(bounds, colorz.shape[0])

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10, 6), constrained_layout=True)
c1 = make_hoverax(o2prim_grid, d13_grid, balance_zzz, cmap=cmap, norm=norm, ax=ax1)

ax1.set_xlabel("o2 prim [-alpha]")
ax1.set_ylabel("d13 [-alpha]")
ax1.set_title("E111 level balance in 3 exc")
ax1.set_xlim(-6, 14)

c2 = make_hoverax(o2prim_grid, d13_grid, balance_zz, cmap=cmap, norm=norm, ax=ax2)
ax2.set_title("E101 2 exc balance")
ax2.set_xlabel("o2 prim [-alpha]")
ax2.set_xlim(-6, 14)

cbar = fig.colorbar(c1, ax=[ax1, ax2])
cbar.set_ticks([i for i in range(-1, 10, 2)])
plt.show()
