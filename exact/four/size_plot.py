# Here I will gather what I need to make the decision on N and M
from exact.four.hamil import eig
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors

NN = np.arange(8, 18, 1)
MM = np.arange(10, 26, 2)
C = 100
sizes = np.zeros((len(NN), len(MM)))
for i, N in enumerate(NN):
    for j, M in enumerate(MM):
        print(i, j)
        size = eig(50, 50, 50, 50, 0.1, 0.1, 0.1, 0.1, only_energy=True, N=N, M=M, C=C)
        sizes[i, j] = size

colors2 = plt.cm.Oranges(np.linspace(0, 0.75, 10))
mymap = colors.LinearSegmentedColormap.from_list("my_colormap", colors2)
plt.pcolor(MM, NN, np.zeros_like(sizes) + 1e-30, norm=colors.LogNorm(), cmap=mymap)

for i in range(len(NN)):
    for j in range(len(MM)):
        text = f"{int(round(sizes[i,j]/100))*100}"
        plt.text(MM[j], NN[i], text, ha="center", va="center", color="black")


plt.title(f"Size of matrix entering eigensolver 4T, rounded to nearest 100")
plt.ylabel("# Transmon eigenstates N")
plt.xlabel("Maximum total excitation M")
plt.show()
