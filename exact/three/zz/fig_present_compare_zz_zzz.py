from other.colormap import OrBu_colormap, Norm
import numpy as np
from matplotlib import pyplot as plt
from store.stores3T import Store_zz3T
from exact.util import omega_alphas, to_omega_grid
from matplotlib import colors
import initplots


Ej3 = 50
Ej1s = np.arange(30, 100, 0.2)
Ej2s = np.arange(30, 140, 0.2)
Eint = 0.04
Eint13 = 0.0013
_, _, zz13, zzz = Store_zz3T.plane(
    "Ej2", Ej2s, 1, "Ej1", Ej1s, 1, Ej3=Ej3, Eint12=Eint, Eint23=Eint, Eint13=Eint13, Ec2=1, Ec3=1
)
Ejs_line, _, _, zz13_line, zzz_line = Store_zz3T.line(
    Ec2=1, Ec3=1, Ej1=50, Ej3=50, Eint12=Eint, Eint23=Eint, Eint13=Eint13
)


fig, (ax1, ax2) = plt.subplots(
    2, 1, gridspec_kw={"height_ratios": [1, 1]}, figsize=(5.9, 5.9 * 3 / 4), constrained_layout=True, sharex=True
)
o2primgrid, detunegrid = to_omega_grid(Ej1s, Ej2s, Ej3)
# ZZ
c1 = ax1.pcolormesh(o2primgrid, detunegrid, zz13, norm=Norm(1e-0), cmap=OrBu_colormap())
ax1.set_ylabel("$\Delta_{13}$ [$E_C$]")

# ZZZ
ax2.pcolormesh(o2primgrid, detunegrid, zzz, norm=Norm(1e-0), cmap=OrBu_colormap())
ax2.set_ylabel("$\Delta_{13}$ [$E_C$]")

cbar = fig.colorbar(c1, ax=[ax1, ax2])
cbar.set_label(r"$\text{ZZ}_{13}$/ZZZ [$E_C$]")

for x in np.arange(-20, 20, 1):
    ax1.axline(xy1=(x, 0), color="lightgray", linestyle="-", linewidth=0.8, zorder=0, slope=-2)
    ax2.axline(xy1=(x, 0), color="lightgray", linestyle="-", linewidth=0.8, zorder=0, slope=-2)

# Line
ax1.set_xlim(-6, 14)
ax1.set_ylim([-4, 8])
omega_mid, _ = omega_alphas(1, 50, True)
o2prim, _ = omega_alphas(1, Ejs_line, True)
o2prim -= omega_mid
# ax3.semilogy(o2prim, np.abs(zz13_line), label=r"$|\text{ZZ}_{13}|$")
# ax3.semilogy(o2prim, np.abs(zzz_line), label=r"$|\text{ZZZ}|$")
# ax3.legend(loc="lower left")
ax2.set_xlabel("$\omega_2^\prime$ [$E_C$]")
# ax3.set_ylabel("Energy [$E_C$]")


# plt.colorbar()
plt.show()
