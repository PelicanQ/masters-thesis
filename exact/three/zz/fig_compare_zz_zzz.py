from other.colormap import OrBu_colormap, Norm
import numpy as np
from matplotlib import pyplot as plt
from store.stores3T import Store_zz3T
from exact.util import omega_alphas, to_omega_grid
from matplotlib import colors

Ej3 = 50
Ej1s = np.arange(30, 100, 1)
Ej2s = np.arange(30, 140, 1)
Eint12 = 0.04
Eint23 = 0.04
Eint13 = 0.0013
_, _, zz13, zzz = Store_zz3T.plane(
    "Ej2", Ej2s, 1, "Ej1", Ej1s, 1, Ej3=Ej3, Eint12=Eint12, Eint23=Eint23, Eint13=Eint13, Ec2=1, Ec3=1
)
Ejs_line, _, _, zz13_line, zzz_line = Store_zz3T.line(
    Ec2=1, Ec3=1, Ej1=50, Ej3=50, Eint12=Eint12, Eint23=Eint23, Eint13=Eint13
)


fig, (ax1, ax2, ax3) = plt.subplots(
    3, 1, gridspec_kw={"height_ratios": [1, 1, 0.6]}, figsize=(10, 9), constrained_layout=True, sharex=True
)
o2primgrid, detunegrid = to_omega_grid(Ej1s, Ej2s, Ej3)
# ZZ
c1 = ax1.pcolormesh(o2primgrid, detunegrid, zz13, norm=Norm(1e-0), cmap=OrBu_colormap())
ax1.set_ylabel("$\Delta_{13}$ [Ec]")

# ZZZ
ax2.pcolormesh(o2primgrid, detunegrid, zzz, norm=Norm(1e-0), cmap=OrBu_colormap())
ax2.set_ylabel("$\Delta_{13}$ [Ec]")

fig.colorbar(c1, ax=[ax1, ax2])

# Line
omega_mid, _ = omega_alphas(1, 50, True)
o2prim, _ = omega_alphas(1, Ejs_line, True)
o2prim -= omega_mid
ax3.semilogy(o2prim, np.abs(zz13_line), label="zz13")
ax3.semilogy(o2prim, np.abs(zzz_line), label="zzz")
ax3.set_ylim([1e-7, 1e0])
ax3.set_xlim(-6, 14)
plt.legend(loc="lower left")
fig.suptitle(rf"ZZZ and ZZ Ej1=Ej3=50 Eint12=Eint23={Eint23} Eint13={Eint13} [Ec]")
plt.xlabel("$\omega_2^\prime$ [Ec]")
# plt.colorbar()
plt.show()
