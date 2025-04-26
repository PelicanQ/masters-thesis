# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap, my_colors
import numpy as np
from matplotlib import pyplot as plt
from jobmanager.util import collect_jobs
from anharm.Hamiltonian import Hamil
from matplotlib import colors
from sandbox.util import make_axslid, makeslid
from anharm.Cacher import Cacher
from analysis.discover import make_hoverax_refreshable

H = Hamil(5, 4, "triang")

# e = H.zzexpr("10100")
# e = H.split_deltas(e)  #
# f, vars = H.lambdify_expr(
#     e
# )  # \alpha_{0}, \alpha_{1}, \alpha_{2}, g_{0,1}, g_{1,2}, g_{0,2}, g_{2,3}, g_{2,4}, \Delta_{0,1}, \Delta_{1,2}, \Delta_{2,3}, \Delta_{3,4}
# Cacher.savezz(f, "10100", 4, "triang")
f = Cacher.getzz("10100", 4, "triang")
alpha = -1
g12 = 0.4
g23 = 0.4
g13 = 0.04
g34 = 0.4
g45 = 0.4
g35 = 0.04
d34 = 1.1
d45 = 1.2

dd13 = np.linspace(-8, 8, 200)
o2prims = np.linspace(-10, 10, 200)
# translate

# s = H.get_subspace(3)
# e1 = s.getedge("111", "021") + s.get_all_edge_corrections("111", "021")
# e2 = s.getedge("111", "201") + s.get_all_edge_corrections("111", "201")
# e3 = s.get_4loop_contraction("111", "021") + s.get_4loop_contraction("111", "201")
# group01 = e1 + e2 + e3
# e1 = s.getedge("111", "120") + s.get_all_edge_corrections("111", "120")
# e2 = s.getedge("111", "102") + s.get_all_edge_corrections("111", "102")
# e3 = s.get_4loop_contraction("111", "120") + s.get_4loop_contraction("111", "102")
# group12 = e1 + e2 + e3
# e1 = s.getedge("111", "210") + s.get_all_edge_corrections("111", "210")
# e2 = s.getedge("111", "012") + s.get_all_edge_corrections("111", "012")
# e3 = s.get_4loop_contraction("111", "210") + s.get_4loop_contraction("111", "012")
# group02 = e1 + e2 + e3
# group3 = s.get_3cycles("111")
# group4 = (
#     s.get_4loop_contraction("111", "003")
#     + s.get_4loop_contraction("111", "030")
#     + s.get_4loop_contraction("111", "300")
# )

# group01 = H.split_deltas(group01)
# group12 = H.split_deltas(group12)
# group02 = H.split_deltas(group02)
# group3 = H.split_deltas(group3)
# group4 = H.split_deltas(group4)

# f01, vars01 = H.lambdify_expr(group01)
# f12, vars12 = H.lambdify_expr(group12)
# f02, vars02 = H.lambdify_expr(group02)
# f3, vars3 = H.lambdify_expr(group3)
# f4, vars4 = H.lambdify_expr(group4)
# print(vars3, vars4)

d2prim_grid, dd13_grid = np.meshgrid(o2prims, dd13)

d23_grid = d2prim_grid + dd13_grid / 2
d12_grid = dd13_grid - d23_grid
args = (alpha, alpha, alpha, g12, g23, g13, g34, g35, d12_grid, d23_grid, d34, d45)
# vals01 = f01(*args)
# vals12 = f12(*args)
# vals02 = f02(*args)
# vals3 = f3(*args)
# vals4 = f4(*args)


@np.vectorize
def snapto0(v):
    if np.abs(v) < 1e-5:
        return 0.0
    return v


def calculate(alpha, g12, g23, g13, g34, g45, g35, d12, d23, d34, d45):
    args = (alpha, alpha, alpha, g12, g23, g13, g34, g35, d12, d23, d34, d45)

    return (snapto0(f(*args)), f(*args))  # , f01(*args), f12(*args), f02(*args), f3(*args), f4(*args)


# vals, vals01, vals12, vals02, vals3, vals4 = calculate(*args)
args = (alpha, g12, g23, g13, g34, g45, g35, d12_grid, d23_grid, d34, d45)

vals, _ = calculate(*args)
val_dict = {"ZZ13": vals}  # to give hover updated values

fig = plt.figure()
((ax1, ax2, ax3), (ax4, ax5, ax6)) = fig.subplots(2, 3)
fig.suptitle(f"ZZ13 [alpha] alpha={alpha}")
norm = colors.SymLogNorm(1e-5, vmin=-1e0, vmax=1e0)
cmap = OrBu_colormap()

c1 = make_hoverax_refreshable(d2prim_grid, dd13_grid, val_dict, "ZZ13", norm=norm, cmap=cmap, ax=ax1)
ax1.set_title("ZZ13")

# c2 = make_hoverax(d2prim_grid, dd13_grid, vals01, norm=norm, cmap=cmap, ax=ax2)
# ax2.set_title("01")

# c3 = make_hoverax(d2prim_grid, dd13_grid, vals12, norm=norm, cmap=cmap, ax=ax3)
# ax3.set_title("12")

# c4 = make_hoverax(d2prim_grid, dd13_grid, vals02, norm=norm, cmap=cmap, ax=ax4)
# ax4.set_title("02")

# c5 = make_hoverax(d2prim_grid, dd13_grid, vals3, norm=norm, cmap=cmap, ax=ax5)
# ax5.set_title("3loop")

# c6 = make_hoverax(d2prim_grid, dd13_grid, vals4, norm=norm, cmap=cmap, ax=ax6)
ax6.set_title("Residual 4 contractions")
fig.colorbar(c1, ax=[ax1, ax2, ax3, ax4, ax5, ax6])

ax1.set_ylabel("delta13")
ax4.set_ylabel("delta13")

ax4.set_xlabel("omega2 prim")
ax5.set_xlabel("omega2 prim")
ax6.set_xlabel("omega2 prim")

fig_control = plt.figure()
fig_control.suptitle("Controls")
axslid_g12 = make_axslid(0.06, 0.6, fig_control, 0.35)
axslid_g23 = make_axslid(0.06, 0.5, fig_control, 0.35)
axslid_g13 = make_axslid(0.06, 0.4, fig_control, 0.35)
axslid_g34 = make_axslid(0.06, 0.3, fig_control, 0.35)
axslid_g45 = make_axslid(0.06, 0.2, fig_control, 0.35)
axslid_g35 = make_axslid(0.06, 0.1, fig_control, 0.35)

axslid_d34 = make_axslid(0.55, 0.2, fig_control, 0.35)
axslid_d45 = make_axslid(0.55, 0.1, fig_control, 0.35)

slid_g12 = makeslid(axslid_g12, "g12", 0, 0.01, 0.5, g12)
slid_g23 = makeslid(axslid_g23, "g23", 0, 0.01, 0.5, g23)
slid_g13 = makeslid(axslid_g13, "g13", 0, 0.001, 0.1, g13)
slid_g34 = makeslid(axslid_g34, "g34", 0, 0.01, 0.5, g34)
slid_g45 = makeslid(axslid_g45, "g45", 0, 0.01, 0.5, g45)
slid_g35 = makeslid(axslid_g35, "g35", 0, 0.001, 0.1, g35)

slid_d34 = makeslid(axslid_d34, "d34", 0, 0.1, 10, d34)
slid_d45 = makeslid(axslid_d45, "d45", 0, 0.1, 10, d45)


def update(val):
    g12 = slid_g12.val
    g23 = slid_g23.val
    g13 = slid_g13.val
    g34 = slid_g34.val
    g45 = slid_g45.val
    g35 = slid_g35.val

    d34 = np.float64(slid_d34.val)
    d45 = np.float64(slid_d45.val)

    all_vals, aa = calculate(alpha, g12, g23, g13, g34, g45, g35, d12_grid, d23_grid, d34, d45)
    # for one_vals, c in zip(all_vals, [c1, c2, c3, c4, c5, c6]):
    for one_vals, c in zip(all_vals, [c1]):
        val_dict["ZZ13"] = aa
        c.set_array(all_vals)
    # ax1.relim()
    fig.canvas.draw_idle()


for s in [slid_g12, slid_g23, slid_g13, slid_g34, slid_g45, slid_g35, slid_d34, slid_d45]:
    s.on_changed(update)


plt.show()
