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
g12 = 0.3
g23 = 0.3
g13 = 0

dd13 = np.linspace(-8, 8, 500)
o2prims = np.linspace(-10, 10, 500)
# translate

s = H.get_subspace(3)
e1 = s.getedge("111", "021") + s.get_all_edge_corrections("111", "021")
e2 = s.getedge("111", "201") + s.get_all_edge_corrections("111", "201")
e3 = s.get_4loop_contraction("111", "021") + s.get_4loop_contraction("111", "201")
group01 = e1 + e2 + e3
e1 = s.getedge("111", "120") + s.get_all_edge_corrections("111", "120")
e2 = s.getedge("111", "102") + s.get_all_edge_corrections("111", "102")
e3 = s.get_4loop_contraction("111", "120") + s.get_4loop_contraction("111", "102")
group12 = e1 + e2 + e3
e1 = s.getedge("111", "210") + s.get_all_edge_corrections("111", "210")
e2 = s.getedge("111", "012") + s.get_all_edge_corrections("111", "012")
e3 = s.get_4loop_contraction("111", "210") + s.get_4loop_contraction("111", "012")
group02 = e1 + e2 + e3

group01 = H.split_deltas(group01)
group12 = H.split_deltas(group12)
group02 = H.split_deltas(group02)

f01, vars01 = H.lambdify_expr(group01)
f12, vars12 = H.lambdify_expr(group12)
f02, vars02 = H.lambdify_expr(group02)


dd13_grid, d2prim_grid = np.meshgrid(dd13, o2prims)

d23_grid = d2prim_grid + dd13_grid / 2
d12_grid = dd13_grid - d23_grid
args = (alpha, alpha, alpha, g12, g23, g13, d12_grid, d23_grid)
vals01 = f01(*args)
vals12 = f12(*args)
vals02 = f02(*args)

vals = f(alpha, alpha, alpha, g12, g23, g13, d12_grid, d23_grid)
plt.pcolormesh(d2prim_grid, dd13_grid, vals, norm=colors.SymLogNorm(1e-5, vmin=-1e-1, vmax=1e-1), cmap=OrBu_colormap())
plt.title(f"ZZ13 [alpha] g12={g12} g23={g23} g13={g13} alpha={alpha}")
plt.ylabel("delta13")
plt.xlabel("omega2 prim")
plt.colorbar()

plt.figure()
plt.pcolormesh(
    d2prim_grid, dd13_grid, vals01, norm=colors.SymLogNorm(1e-5, vmin=-1e-1, vmax=1e-1), cmap=OrBu_colormap()
)
plt.figure()
plt.pcolormesh(
    d2prim_grid, dd13_grid, vals12, norm=colors.SymLogNorm(1e-5, vmin=-1e-1, vmax=1e-1), cmap=OrBu_colormap()
)
plt.figure()
plt.pcolormesh(
    d2prim_grid, dd13_grid, vals02, norm=colors.SymLogNorm(1e-5, vmin=-1e-1, vmax=1e-1), cmap=OrBu_colormap()
)

plt.show()
