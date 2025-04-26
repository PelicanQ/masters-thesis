from exact.threetransmon.hamil import eig_clever_vis
import numpy as np
from matplotlib import pyplot as plt

Ms = np.arange(10, 30, 1)
L = 40
Es = np.zeros((len(Ms), L))
for i, M in enumerate(Ms):
    levels = eig_clever_vis(1, 1, 50, 40, 50, 0.6, 0.7, 0.8, M=M, only_energy=True)
    Es[i, :] = levels[:L]

for i in [7, 17, 23, 31]:
    plt.plot(Ms, Es[:, i] - Es[-1, i], label=f"{i}")
plt.xlabel("max excitation")
plt.ylabel("Level [Ec1]")
plt.title("Levels 7,17,23,31 relative their final value [Ec1]")
plt.legend()
plt.show()
