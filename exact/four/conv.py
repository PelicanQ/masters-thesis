# Here I will gather what I need to make the decision on N and M
from exact.four.hamil import eig
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors

NN = np.arange(8, 18, 1)
MM = np.arange(10, 26, 2)
C = 100
# # order Ej1 Ej2 Ej3 Eint12 Eint23 Eint13

# points = [
#     (50, 50, 50, 50, 0.3, 0.3, 0.3, 0.3),
#     (50, 50, 50, 50, 0.4, 0.4, 0.4, 0.4),
#     (50, 55, 60, 45, 0.3, 0.3, 0.3, 0.3),
#     (50, 55, 60, 45, 0.4, 0.4, 0.4, 0.4),
#     (40, 60, 70, 50, 0.3, 0.3, 0.3, 0.3),
#     (40, 60, 70, 50, 0.4, 0.4, 0.4, 0.4),
# ]
# num_levels = 34  # number of levels above ground
# relative_errs = np.zeros((len(points), len(NN), len(MM), num_levels))
# for p_i, p in enumerate(points):
#     v = np.zeros((len(NN), len(MM), num_levels))
#     for i, N in enumerate(NN):
#         for j, M in enumerate(MM):
#             print(p_i, N, M)
#             vals = eig(*p, only_energy=True, N=N, M=M, C=C)
#             v[i, j, :] = vals[1 : num_levels + 1] - vals[0]
#     final = v[-1, -1, :]
#     relerr = (v - final) / final  # all relative to their final
#     relative_errs[p_i, :, :, :] = relerr

# maxed = np.max(np.abs(relative_errs), axis=(0, 3)) + 1e-30
# np.save("relerror4T", maxed)
# exit()
maxed = np.load("relerror4T.npy")
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
plt.title(f"Relative error in energy levels 4T, C={C}")
plt.ylabel("# Transmon eigenstates N")
plt.xlabel("Maximum total excitation M")
plt.show()
