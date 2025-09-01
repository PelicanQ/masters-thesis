from exact.three.hamil import eig_excitation_trunc
from exact.gale_shapely.gale_shapely import state_assignment
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors

# Instead of checking conv of levels, I instead check conv of ZZ here.
# This kinda failed because GS changes a lot with N and M
NN = np.arange(10, 15, 1)
MM = np.arange(10, 20, 1)

C = 100
points = [
    (50, 50, 50, 0.1, 0.1, 0.1),
    (50, 50, 50, 0.3, 0.3, 0.3),
    (50, 50, 50, 0.5, 0.5, 0.5),
    (50, 55, 60, 0.1, 0.1, 0.1),
    (50, 55, 60, 0.3, 0.3, 0.3),
    (50, 55, 60, 0.5, 0.5, 0.5),
    (40, 60, 70, 0.1, 0.1, 0.1),
    (40, 60, 70, 0.3, 0.3, 0.3),
    (40, 60, 70, 0.5, 0.5, 0.5),
]

v = []
for j, M in enumerate(MM):
    levels = eig_excitation_trunc(1, 1, *points[1], N=12, M=M, C=C, only_energy=True)
    levels = levels - levels[0]

    zzGS13 = levels[6] - levels[2] - levels[1]
    v.append(zzGS13)
plt.plot(MM, v)
plt.show()
exit()
err = np.zeros((len(points), len(NN), len(MM)))
for p_i, p in enumerate(points):
    v = np.zeros((len(NN), len(MM)))
    for i, N in enumerate(NN):
        for j, M in enumerate(MM):
            levels, vecs, index_map = eig_excitation_trunc(1, 1, *p, N=N, M=M, C=C)
            bare_to_dressed_index = state_assignment(eigen_states=vecs)
            levels = levels - levels[0]

            def gslevel(n1, n2, n3):
                return levels[bare_to_dressed_index[index_map[(n1, n2, n3)]]]

            zzGS13 = gslevel(1, 0, 1) - gslevel(1, 0, 0) - gslevel(0, 0, 1)

            v[i, j] = zzGS13

    final = v[-1, -1]
    relerr = (v - final) / final  # all relative to their final

    print(v - final, final, relerr)
    err[p_i, :, :] = relerr

maxed = np.mean(np.abs(err), axis=0) + 1e-30
colors2 = plt.cm.Oranges(np.linspace(0, 0.75, 10))
mymap = colors.LinearSegmentedColormap.from_list("my_colormap", colors2)
plt.pcolor(MM, NN, maxed, norm=colors.LogNorm(1e-12), cmap=mymap)

for i in range(len(NN)):
    for j in range(len(MM)):
        if i == len(NN) - 1 and j == len(MM) - 1:
            break
        text = f"{int(np.round(np.log10(maxed[i,j])))}"
        plt.text(MM[j], NN[i], text, ha="center", va="center", color="black")


plt.colorbar()
plt.title("Relative error ZZ13, C={C}")
plt.ylabel("# Transmon eigenstates N")
plt.xlabel("Maximum total excitation M")
plt.show()
