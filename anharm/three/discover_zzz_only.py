# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap, my_colors
import numpy as np
from matplotlib import pyplot as plt
from jobmanager.util import collect_jobs
from anharm.Hamiltonian import Hamil
from matplotlib import colors
from sandbox.util import make_axslid, makeslid
from analysis.discover import make_discover

H = Hamil(3, 4, "triang")
e = H.zzexpr("111")
e = H.split_deltas(e)
f, vars = H.lambdify_expr(e)
alpha = -1
g12 = 0.19
g23 = 0.19
g13 = 0.003

dd13 = np.linspace(-8, 8, 200)
o2prims = np.linspace(-8, 8, 200)
o2_grid, d13_grid = np.meshgrid(o2prims, dd13)
d23_grid = o2_grid + d13_grid / 2
d12_grid = d13_grid - d23_grid


def calculate(a1, a2, g12, g23, g13):
    return f(a1, a2, -1, g12, g23, g13, d12_grid, d23_grid)


norm = colors.SymLogNorm(1e-6, vmin=-1e0, vmax=1e0)
cmap = OrBu_colormap()


ax = make_discover(["g12", "g23", "g13", "a1", "a2"], [g12, g23, g13, -1, -1], o2_grid, d13_grid, calculate, norm, cmap)
plt.show()
