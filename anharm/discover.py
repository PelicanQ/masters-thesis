# To easily add interactivity to a plot
# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap, my_colors
import numpy as np
from matplotlib import pyplot as plt
from jobmanager.util import collect_jobs
from anharm.Hamiltonian import Hamil
from matplotlib import colors
from sandbox.util import make_axslid, makeslid
from analysis.discover import make_hoverax_refreshable
from anharm.three.swt_zzz_only import zzzfunctions

H = Hamil(3, 4, "triang")
e = H.zzexpr("111")
e = H.split_deltas(e)
f, vars = H.lambdify_expr(e)
alpha = -1
g12 = 0.4
g23 = 0.4
g13 = 0.02

dd13 = np.linspace(-8, 8, 200)
o2prims = np.linspace(-10, 10, 200)
d2prim_grid, dd13_grid = np.meshgrid(o2prims, dd13)
d23_grid = d2prim_grid + dd13_grid / 2
d12_grid = dd13_grid - d23_grid


args = (alpha, alpha, alpha, g12, g23, g13, d12_grid, d23_grid)


@np.vectorize
def snapto0(v):
    if np.abs(v) < 1e-5:
        return 0
    return v


f01, f12, f02, f3, f4 = zzzfunctions()


def calculate(alpha, g12, g23, g13, d12, d23):
    args = (alpha, alpha, alpha, g12, g23, g13, d12, d23)

    return snapto0(f(*args)), f01(*args), f12(*args), f02(*args), f3(*args), f4(*args)


vals, vals01, vals12, vals02, vals3, vals4 = calculate(alpha, g12, g23, g13, d12_grid, d23_grid)


norm = colors.SymLogNorm(1e-5, vmin=-1e0, vmax=1e0)
cmap = OrBu_colormap()
fig = plt.figure()
((ax1, ax2, ax3), (ax4, ax5, ax6)) = fig.subplots(2, 3)
fig.suptitle(rf"Grouped contributions to ZZZ, units [-$\alpha$]")
val_dict = {
    "ZZZ": vals,
    "01": vals01,
    "12": vals12,
    "02": vals02,
    "3": vals3,
    "4": vals4,
}
c1 = make_hoverax_refreshable(d2prim_grid, dd13_grid, val_dict, "ZZZ", norm=norm, cmap=cmap, ax=ax1)
ax1.set_title("ZZZ")

fig.colorbar(c1, ax=[ax1, ax2, ax3, ax4, ax5, ax6])

ax1.set_ylabel("delta13")
ax4.set_ylabel("delta13")

ax4.set_xlabel("omega2 prim")
ax5.set_xlabel("omega2 prim")
ax6.set_xlabel("omega2 prim")

fig_control = plt.figure()
fig_control.suptitle("Controls")
axslid_g12 = make_axslid(0.15, 0.7, fig_control, 0.75)
axslid_g23 = make_axslid(0.15, 0.4, fig_control, 0.75)
axslid_g13 = make_axslid(0.15, 0.1, fig_control, 0.75)

slid_g12 = makeslid(axslid_g12, "g12", 0, 0.01, 0.5)
slid_g23 = makeslid(axslid_g23, "g23", 0, 0.01, 0.5)
slid_g13 = makeslid(axslid_g13, "g13", 0, 0.001, 0.1)


def update(val):
    global g12, g23, g13
    g12 = slid_g12.val
    g23 = slid_g23.val
    g13 = slid_g13.val
    all_vals = calculate(alpha, g12, g23, g13, d12_grid, d23_grid)
    for one_vals, c, key in zip(all_vals, [c1, c2, c3, c4, c5, c6], ["ZZZ", "01", "12", "02", "3", "4"]):
        c.set_array(one_vals)
        val_dict[key] = one_vals

    fig.canvas.draw_idle()


for s in [slid_g12, slid_g23, slid_g13]:
    s.on_changed(update)


plt.show()
