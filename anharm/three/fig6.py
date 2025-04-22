# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap
import numpy as np
from matplotlib import pyplot as plt
from jobmanager.util import collect_jobs
from anharm.Hamiltonian import Hamil
from matplotlib import colors

H = Hamil(3, 4, "triang")
e = H.zzexpr("101")
e = H.split_deltas(e)
f, vars = H.lambdify_expr(e)
alpha = -1
g12 = 0.2
g23 = 0.2
g13 = 0.05

# dd13 = np.arange(-10, 10, 0.1)
# d2prim = np.arange(-10, 10, 0.1)
dd13 = np.linspace(-8, 8, 500)
o2prims = np.linspace(-10, 10, 500)
# translate

vals = np.zeros((len(dd13), len(o2prims)))
dd13_grid, d2prim_grid = np.meshgrid(dd13, o2prims)
d12_grid = np.zeros(dd13_grid.shape)
d23_grid = np.zeros(dd13_grid.shape)

for i in range(dd13_grid.shape[0]):
    for j in range(dd13_grid.shape[1]):
        d23_grid[i, j] = d2prim_grid[i, j] + dd13_grid[i, j] / 2
        d12_grid[i, j] = dd13_grid[i, j] - d23_grid[i, j]

vals = f(alpha, alpha, alpha, g12, g23, g13, d12_grid, d23_grid)
plt.pcolormesh(d2prim_grid, dd13_grid, vals, norm=colors.SymLogNorm(1e-5, vmin=-1e-1, vmax=1e-1), cmap=OrBu_colormap())
plt.title(f"ZZ13 [alpha] g12={g12} g23={g23} g13={g13} alpha={alpha}")
plt.ylabel("delta13")
plt.xlabel("omega2 prim")
plt.colorbar()
plt.show()
