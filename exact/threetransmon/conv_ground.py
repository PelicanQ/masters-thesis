# let's see when the ground level stablizes with k. I wanna keep k low due to slow numerics
import numpy as np
from exact.threetransmon.hamil import eig_clever
from matplotlib import pyplot as plt

kk = np.arange(5, 15, 1)
E = []
for k in kk:
    vals = eig_clever(1, 1, 50, 50, 50, 0.1, 0.1, 0.1, only_energy=True, k=k)
    E.append(vals[0])
plt.plot(kk, vals)
plt.show()
