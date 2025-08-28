# It's time I investigate convergence of levels wrt charge basis truncation
import numpy as np
from exact.two.hamil import eig_clever
from analysis.plot import plot
from matplotlib import pyplot as plt

k = 15
Eint = 1
level_select = np.arange(0, 30, 1)
Cs = np.arange(15, 25, 1)
Es = np.zeros((len(Cs), len(level_select)))
for i in range(len(Cs)):
    levels = eig_clever(30, 60, Eint, Ec2=1, only_energy=True, ng1=0, k=k, C=Cs[i])
    Es[i, :] = levels[level_select]
# Es = Es - Es[-1, :]
for i in [1, 10, 20, 29]:
    plt.figure()
    plt.plot(Cs, Es[:, i])
    plt.title(f"Level {i} (raw), k={k}, Ej1=30, Ej2=60, Eint={Eint}")
    plt.xlabel("C")
plt.show()
