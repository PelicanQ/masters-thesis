from ..sim_store.analysis.plot import grid3d
from .hamil import eig_clever
import numpy as np
from matplotlib import pyplot as plt

# Regarding degenerate perturbation theory,
# it may be that a degeneracy is lifted to first order in lambda
# or we need second order corrections to energies to see the lift.
# I wanna see if numerics can hint at which case we have
# take two transmons and increase coupling

# now we check the lowest levels for some Eint
k = 13
num_levels = 20
Eints = np.linspace(0, 0.1, 40)  # as seen, Eint below 1 should well cover the relevant

levels = np.zeros(shape=(num_levels, len(Eints)))
for i, Eint in enumerate(Eints):
    print(i)
    vals = eig_clever(Ej1=50, Ej2=50, Eint=Eint, k=k, only_energy=True)
    levels[:, i] = vals[:num_levels]

plt.plot(Eints, levels.T)
plt.show()
