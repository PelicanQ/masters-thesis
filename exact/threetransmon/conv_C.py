# It's time I investigate convergence of levels wrt charge basis truncation
import numpy as np
from exact.threetransmon.hamil import eig_excitation_trunc
from analysis.plot import plot
from matplotlib import pyplot as plt

# Here we decide a reasonable C parameter
M = 28
N = 20
points = [
    (50, 50, 50, 0.1, 0.1, 0.1),
    # (50, 50, 50, 0.3, 0.3, 0.3),
    # (50, 50, 50, 0.5, 0.5, 0.5),
    # (50, 55, 60, 0.1, 0.1, 0.1),
    # (50, 55, 60, 0.3, 0.3, 0.3),
    # (50, 55, 60, 0.5, 0.5, 0.5),
    # (40, 60, 70, 0.1, 0.1, 0.1),
    # (40, 60, 70, 0.3, 0.3, 0.3),
    # (40, 60, 70, 0.5, 0.5, 0.5),
]
num_levels = 10  # number of levels above ground

Cs = np.arange(7, 30, 4)
Es = np.zeros((len(Cs), num_levels))
relative_errors = np.zeros((len(points), len(Cs), num_levels))

for p_i, point in enumerate(points):
    v = np.zeros((len(Cs), num_levels))
    for i, C in enumerate(Cs):
        levels = eig_excitation_trunc(1, 1, *point, only_energy=True, N=N, C=Cs[i])
        v[i, :] = levels[1 : num_levels + 1]
        v[i, :] = levels[1 : num_levels + 1] - levels[0]
    final = v[-1, :]
    relerr = (v - final) / final  # all relative to their final
    relative_errors[p_i, :, :] = relerr


maxed = np.max(np.abs(relative_errors), axis=(0, 2)) + 1e-30
# colors2 = plt.cm.Oranges(np.linspace(0, 0.75, 10))
# mymap = colors.LinearSegmentedColormap.from_list("my_colormap", colors2)
plt.plot(Cs, maxed)

plt.title("Relative error")
plt.ylabel("as")
plt.xlabel("C")
plt.show()
