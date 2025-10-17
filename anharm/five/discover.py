from other.colormap import OrBu_colormap
import numpy as np
from matplotlib import pyplot as plt
from anharm.Hamiltonian import Hamil
from matplotlib import colors
from sandbox.util import make_axslid, makeslid
from anharm.Cacher import Cacher
from matplotlib.widgets import Slider


def create_zz_functions():
    H = Hamil(5, 4, "triang")

    expr02 = H.zzexpr("10100")
    expr02 = H.split_deltas(expr02)
    func02, vars02 = H.lambdify_expr(expr02)
    print(vars02)  # alpha0, alpha1, alpha2, g01, g12, g02, g23, g24, Delta01, Delta12, Delta23, Delta34

    expr024 = H.zzexpr("10101")
    expr024 = H.split_deltas(expr024)
    func024, vars024 = H.lambdify_expr(expr024)
    print(vars024)  # alpha0 alpha1 alpha2 alpha3 alpha4 g01 g12 g02 g23 g34 g24 Delta01, Delta12, Delta23, Delta34

    Cacher.savezz(func02, "10100", 4, "triang")
    Cacher.savezz(func024, "10101", 4, "triang")


# if __name__ == "__main__":
# create_zz_functions()
# exit()

zz02_func = Cacher.getzz("10100", 4, "triang")
zzz024_func = Cacher.getzz("10101", 4, "triang")

# inital parameters alphas, g's and deltas
a0_init = -1.0
a1_init = -1.0
a2_init = -1.0
a3_init = -1.0
a4_init = -1.0

g01_init = 0.2
g12_init = 0.2
g02_init = 0.005
g23_init = 0.04  # start with weaker couplings to the spectators to reproduce familiar ZZ plot
g34_init = 0.04
g24_init = 0.004

d23_init = 4.2
d24_init = 3.4

# set up grid which we plot in
delta02 = np.linspace(-8, 8, 200)
omega1prime = np.linspace(-10, 10, 200)
omega1prime_grid, delta02_grid = np.meshgrid(omega1prime, delta02)
delta12_grid = omega1prime_grid + delta02_grid / 2
delta01_grid = delta02_grid - delta12_grid


# initial vallues
d34_init = d24_init - d23_init
# alpha0, alpha1, alpha2, g01, g12, g02, g23, g24, Delta01, Delta12, Delta23, Delta34
inital_zz02 = zz02_func(
    a0_init,
    a1_init,
    a2_init,
    g01_init,
    g12_init,
    g02_init,
    g23_init,
    g24_init,
    delta01_grid,
    delta12_grid,
    d23_init,
    d34_init,
)
# alpha0 alpha1 alpha2 alpha3 alpha4 g01 g12 g02 g23 g34 g24 Delta01, Delta12, Delta23, Delta34
inital_zzz024 = zzz024_func(
    a0_init,
    a1_init,
    a2_init,
    a3_init,
    a4_init,
    g01_init,
    g12_init,
    g02_init,
    g23_init,
    g34_init,
    g24_init,
    delta01_grid,
    delta12_grid,
    d23_init,
    d34_init,
)

# create 2D ZZ plots
norm = colors.SymLogNorm(1e-6, vmin=-1e0, vmax=1e0)
cmap = OrBu_colormap()

fig02, ax02 = plt.subplots()
fig02.suptitle(f"ZZ02")
quadmesh02 = ax02.pcolormesh(omega1prime_grid, delta02_grid, inital_zz02, norm=norm, cmap=cmap)
fig02.colorbar(quadmesh02)
ax02.set_xlabel(r"$\omega_1'$")
ax02.set_ylabel(r"$\Delta_{0,2}$")

fig024, ax024 = plt.subplots()
fig024.suptitle(f"ZZZ024")
quadmesh024 = ax024.pcolormesh(omega1prime_grid, delta02_grid, inital_zzz024, norm=norm, cmap=cmap)
fig024.colorbar(quadmesh024)
ax024.set_xlabel(r"$\omega_1'$")
ax024.set_ylabel(r"$\Delta_{0,2}$")


i = len(delta02) // 2  # start in a middle point
(cutmarker02,) = ax02.plot(
    [omega1prime[0], omega1prime[-1]], [delta02[i], delta02[i]], color="gray", linestyle=":"
)  # reference line for 1d cut
(cutmarker024,) = ax024.plot([omega1prime[0], omega1prime[-1]], [delta02[i], delta02[i]], color="gray", linestyle=":")

# create 1D cut plot
figcut, axcut = plt.subplots()
plt.subplots_adjust(0.16)
figcut.suptitle(r"Cut along $\omega_1'$")
ax_d02 = figcut.add_axes((0.03, 0.1, 0.03, 0.65))
slider_d02 = Slider(ax_d02, "d02", -8, 8, valinit=delta02[i], valstep=delta02, orientation="vertical")
(line02,) = axcut.plot(omega1prime, inital_zz02[i, :], label="zz02")
(line024,) = axcut.plot(omega1prime, inital_zzz024[i, :], label="zzz024")
axcut.set_ylim([-1, 1])
axcut.set_yscale("symlog", linthresh=1e-5)
axcut.legend()


# create qubit spectrum plot for 1D plot
def omegas_from_deltas(d02, d23, d34):
    omega2 = 0.0  # middle qubit is reference
    omega0 = d02 + omega2
    omega3 = omega2 - d23
    omega4 = omega3 - d34
    return omega0, omega2, omega3, omega4


omega0, omega2, omega3, omega4 = omegas_from_deltas(delta02[i], d23_init, d34_init)
figspec, ax_spec = plt.subplots()
# qbuit 1 is swept in 1D cut
(qline0,) = ax_spec.plot([0, 1], [omega0, omega0], color="b")
(qline2,) = ax_spec.plot([2, 3], [omega2, omega2], color="g")
(qline3,) = ax_spec.plot([3, 4], [omega3, omega3], color="r")
(qline4,) = ax_spec.plot([4, 5], [omega4, omega4], color="c")

(aline0_p, aline0_m) = ax_spec.plot(
    [[0, 0], [1, 1]],
    [[omega0 + a0_init, omega0 - a0_init], [omega0 + a0_init, omega0 - a0_init]],
    color="b",
    linestyle=":",
)
(aline2_p, aline2_m) = ax_spec.plot(
    [[2, 2], [3, 3]],
    [[omega2 + a2_init, -omega2 - a2_init], [omega2 + a2_init, omega2 - a2_init]],
    color="g",
    linestyle=":",
)
(aline3_p, aline3_m) = ax_spec.plot(
    [[3, 3], [4, 4]],
    [[omega3 + a3_init, omega3 - a3_init], [omega3 + a3_init, omega3 - a3_init]],
    color="r",
    linestyle=":",
)
(aline4_p, aline4_m) = ax_spec.plot(
    [[4, 4], [5, 5]],
    [[omega4 + a4_init, omega4 - a4_init], [omega4 + a4_init, omega4 - a4_init]],
    color="c",
    linestyle=":",
)

ax_spec.set_ylim([-10, 10])
ax_spec.set_title("Qubit spectrum for 1D cut. Dashed: alpha")
ax_spec.set_ylabel(r"$\omega$")


def create_controls():
    fig_control = plt.figure(figsize=(12, 6))
    fig_control.suptitle("Controls")

    alpha_mid = -1
    alpha_step = 0.01
    alpha_range = 0.5

    g_mid = 0
    g_step = 0.01
    g_range = 0.2

    delta_mid = 0
    delta_step = 0.1
    delta_range = 8

    slider_width = 0.25
    x1 = 0.03
    x2 = x1 + slider_width + 0.08
    x3 = x2 + slider_width + 0.08

    ax_a0 = make_axslid(x1, 0.9, fig_control, slider_width)
    ax_a1 = make_axslid(x1, 0.8, fig_control, slider_width)
    ax_a2 = make_axslid(x1, 0.7, fig_control, slider_width)
    ax_a3 = make_axslid(x1, 0.6, fig_control, slider_width)
    ax_a4 = make_axslid(x1, 0.5, fig_control, slider_width)

    ax_g01 = make_axslid(x2, 0.9, fig_control, slider_width)
    ax_g12 = make_axslid(x2, 0.8, fig_control, slider_width)
    ax_g02 = make_axslid(x2, 0.7, fig_control, slider_width)
    ax_g23 = make_axslid(x2, 0.6, fig_control, slider_width)
    ax_g34 = make_axslid(x2, 0.5, fig_control, slider_width)
    ax_g24 = make_axslid(x2, 0.4, fig_control, slider_width)

    ax_d23 = make_axslid(x3, 0.9, fig_control, slider_width)
    ax_d24 = make_axslid(x3, 0.8, fig_control, slider_width)

    slide_a0 = makeslid(ax_a0, "a0", alpha_mid, alpha_step, alpha_range, a0_init)
    slide_a1 = makeslid(ax_a1, "a1", alpha_mid, alpha_step, alpha_range, a1_init)
    slide_a2 = makeslid(ax_a2, "a2", alpha_mid, alpha_step, alpha_range, a2_init)
    slide_a3 = makeslid(ax_a3, "a3", alpha_mid, alpha_step, alpha_range, a3_init)
    slide_a4 = makeslid(ax_a4, "a4", alpha_mid, alpha_step, alpha_range, a4_init)

    slide_g01 = makeslid(ax_g01, "g01", g_mid, g_step, g_range, g01_init)
    slide_g12 = makeslid(ax_g12, "g12", g_mid, g_step, g_range, g12_init)
    slide_g02 = makeslid(ax_g02, "g02", g_mid, 0.001, 0.02, g02_init)
    slide_g23 = makeslid(ax_g23, "g23", g_mid, g_step, g_range, g23_init)
    slide_g34 = makeslid(ax_g34, "g34", g_mid, g_step, g_range, g34_init)
    slide_g24 = makeslid(ax_g24, "g24", g_mid, 0.001, 0.02, g24_init)

    slide_d23 = makeslid(ax_d23, "d23", delta_mid, delta_step, delta_range, d23_init)
    slide_d24 = makeslid(ax_d24, "d24", delta_mid, delta_step, delta_range, d24_init)

    alpha_sliders = [slide_a0, slide_a1, slide_a2, slide_a3, slide_a4]
    g_sliders = [slide_g01, slide_g12, slide_g02, slide_g23, slide_g34, slide_g24]
    delta_sliders = [slide_d23, slide_d24]
    return alpha_sliders, g_sliders, delta_sliders


alpha_sliders, g_sliders, delta_sliders = create_controls()


def update(val):
    a0, a1, a2, a3, a4 = [slider.val for slider in alpha_sliders]
    g01, g12, g02, g23, g34, g24 = [slider.val for slider in g_sliders]
    d23, d24 = [slider.val for slider in delta_sliders]
    d02 = slider_d02.val  # for 1D plot

    d34 = d24 - d23

    # alpha0, alpha1, alpha2, g01, g12, g02, g23, g24, Delta01, Delta12, Delta23, Delta34
    zz02 = zz02_func(a0, a1, a2, g01, g12, g02, g23, g24, delta01_grid, delta12_grid, d23, d34)
    # alpha0 alpha1 alpha2 alpha3 alpha4 g01 g12 g02 g23 g34 g24 Delta01, Delta12, Delta23, Delta34
    zzz024 = zzz024_func(a0, a1, a2, a3, a4, g01, g12, g02, g23, g34, g24, delta01_grid, delta12_grid, d23, d34)

    quadmesh02.set_array(zz02)
    quadmesh024.set_array(zzz024)

    # update 1D cut plot
    i = np.argmin(np.abs(delta02 - d02))
    selected_d02 = delta02[i]
    cutmarker02.set_ydata([selected_d02, selected_d02])
    cutmarker024.set_ydata([selected_d02, selected_d02])
    line02.set_ydata(zz02[i, :])
    line024.set_ydata(zzz024[i, :])

    # handle qubit spectrum
    # All zz expressions depend only on deltas under RWA so we need to choose one omega to set the reference

    omega0, omega2, omega3, omega4 = omegas_from_deltas(selected_d02, d23, d34)
    qline0.set_ydata([omega0, omega0])
    # qubit 2 is swept in frequency in the 1D plot
    qline2.set_ydata([omega2, omega2])
    qline3.set_ydata([omega3, omega3])
    qline4.set_ydata([omega4, omega4])

    aline0_p.set_ydata([omega0 + a0, omega0 + a0])
    aline2_p.set_ydata([omega2 + a2, omega2 + a2])
    aline3_p.set_ydata([omega3 + a3, omega3 + a3])
    aline4_p.set_ydata([omega4 + a4, omega4 + a4])

    aline0_m.set_ydata([omega0 - a0, omega0 - a0])
    aline2_m.set_ydata([omega2 - a2, omega2 - a2])
    aline3_m.set_ydata([omega3 - a3, omega3 - a3])
    aline4_m.set_ydata([omega4 - a4, omega4 - a4])

    # update canvases
    fig02.canvas.draw_idle()
    fig024.canvas.draw_idle()
    figcut.canvas.draw_idle()
    figspec.canvas.draw_idle()


for slider in alpha_sliders + g_sliders + delta_sliders + [slider_d02]:
    # set event listener to update plots
    slider.on_changed(update)


plt.show()
