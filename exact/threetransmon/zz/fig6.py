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
print(vars)

alpha = -1
g12 = 1 / 3
g23 = 1 / 3
g13 = g12 / 30

# dd13 = np.arange(-10, 10, 0.1)
# d2prim = np.arange(-10, 10, 0.1)
dd13 = np.linspace(-1, 1, 500)
d2prims = np.linspace(-10, 10, 500)
# translate

vals = np.zeros((len(dd13), len(d2prims)))

for i, d13 in enumerate(dd13):
    for j, d2prim in enumerate(d2prims):
        d23 = d2prim + d13 / 2
        d12 = d13 - d23
        vals[i, j] = f(alpha, alpha, alpha, g12, g23, g13, d12, d23)
plt.pcolor(d2prims, dd13, vals, norm=colors.SymLogNorm(1e-6, vmin=-1e-1, vmax=1e-1), cmap=OrBu_colormap())
plt.colorbar()
plt.show()
