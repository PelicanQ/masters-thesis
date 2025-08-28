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
zz12, zz23, zz13, zzz = Store_zz3T.plane(
    "Ej2", Ej2s, 1, "Ej1", Ej1s, 1, Ej3=Ej3, Eint12=Eint, Eint23=Eint, Eint13=Eint13, Ec2=1, Ec3=1
)
# Ejs_line, _, _, zz13_line, zzz_line = Store_zz3T.line(
#     Ec2=1, Ec3=1, Ej1=50, Ej3=50, Eint12=Eint, Eint23=Eint, Eint13=Eint13
# )


fig, (ax1, ax2) = plt.subplots(
    2,
    1,
    gridspec_kw={"height_ratios": [1, 1]},
    figsize=(5.9, 5.9 * 3 / 4),
    constrained_layout=True,
    sharex=True,
)
o2primgrid, detunegrid = to_omega_grid(Ej1s, Ej2s, Ej3)

c1 = ax1.pcolormesh(o2primgrid, detunegrid, zz12, norm=Norm(1e-0), cmap=OrBu_colormap(), rasterized=True)
ax1.set_ylabel("$\Delta_{13}$ [$E_C$]")
ax1.set_xlim([-6, 14])
ax1.set_ylim([-4, 8])

ax2.pcolormesh(o2primgrid, detunegrid, zz23, norm=Norm(1e-0), cmap=OrBu_colormap(), rasterized=True)
ax2.set_ylabel("$\Delta_{13}$ [$E_C$]")
ax2.set_xlabel("$\omega_2'$ [$E_C$]")

fig.colorbar(c1, ax=[ax1, ax2])

for x in np.arange(-20, 20, 1):
    ax1.axline(xy1=(x, 0), color="lightgray", linestyle="-", linewidth=0.8, zorder=0, slope=-2)
    ax2.axline(xy1=(x, 0), color="lightgray", linestyle="-", linewidth=0.8, zorder=0, slope=-2)

# Line

# fig.suptitle(
#     rf"$\text{{ZZ}}_{{12}}$ and $\text{{ZZ}}_{{23}}$ for $E_{{J3}}=50$, $E_{{12}}=E_{{23}}={Eint}$, $E_{{13}}={Eint13}$ units $E_C$"
# )
fig.savefig("figs/zz-12-23.pdf", dpi=300, bbox_inches="tight")


# plt.colorbar()
plt.show()
