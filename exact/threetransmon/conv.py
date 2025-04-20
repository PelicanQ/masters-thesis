# Here I will gather what I need to make the decision on N and M
from exact.threetransmon.hamil import eig_excitation_trunc
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors

NN = np.arange(8, 18, 1)
MM = np.arange(10, 26, 2)

# order Ej1 Ej2 Ej3 Eint12 Eint23 Eint13
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
num_levels = 19  # number of levels above ground
relative_errs = np.zeros((len(points), len(NN), len(MM), num_levels))
for p_i, p in enumerate(points):
    v = np.zeros((len(NN), len(MM), num_levels))
    for i, N in enumerate(NN):
        for j, M in enumerate(MM):
            vals = eig_excitation_trunc(1, 1, *p, only_energy=True, N=N, M=M, C=100)
            v[i, j, :] = vals[1 : num_levels + 1] - vals[0]
    final = v[-1, -1, :]
    relerr = (v - final) / final  # all relative to their final
    relative_errs[p_i, :, :, :] = relerr

maxed = np.max(np.abs(relative_errs), axis=(0, 3)) + 1e-30
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
plt.title("Relative error, C=100")
plt.ylabel("# Transmon eigenstates N")
plt.xlabel("Maximum total excitation M")
plt.show()
