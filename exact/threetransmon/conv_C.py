# It's time I investigate convergence of levels wrt charge basis truncation
import numpy as np
from exact.threetransmon.hamil import eig_clever
from analysis.plot import plot
from matplotlib import pyplot as plt

k = 10
Ej1 = 60
Ej2 = 45
Ej3 = 30
Eint12 = 0.5
Eint23 = 1
Eint13 = 0.8

level_select = np.arange(0, 41, 1)
Cs = np.arange(12, 30, 2)
Es = np.zeros((len(Cs), len(level_select)))
for i in range(len(Cs)):
    print(i)
    levels = eig_clever(
        Ec2=1,
        Ec3=1,
        Ej1=Ej1,
        Ej2=Ej2,
        Ej3=Ej3,
        Eint12=Eint12,
        Eint23=Eint23,
        Eint13=Eint13,
        only_energy=True,
        k=k,
        C=Cs[i],
    )
    Es[i, :] = levels[level_select]
# Es = Es - Es[-1, :]
for i in [1, 4, 10, 40]:
    plt.figure()
    plt.plot(Cs, Es[:, i] - Es[:, 0])
    plt.title(f"Level {i} (rel), k={k}")
    plt.xlabel("C")
plt.show()
