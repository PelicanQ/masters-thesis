# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap
import numpy as np
from matplotlib import pyplot as plt
from jobmanager.util import collect_jobs
from anharm.Hamiltonian import Hamil
from matplotlib import colors
from exact.threetransmon.zz.zz import single_zz
from store.stores import Store_zz3T
from exact.util import omega_alphas

Ej3 = 50
Ej1s = np.arange(30, 80, 0.2)
Ej2s = np.arange(30, 80, 0.2)
Eint12 = 0.1
Eint23 = 0.1
Eint13 = 0
zz12, zz23, zz13, zzz = Store_zz3T.plane(
    "Ej2", Ej2s, "Ej1", Ej1s, Ej3=Ej3, Eint12=Eint12, Eint23=Eint23, Eint13=Eint13, Ec2=1, Ec3=1
)
# for i, Ejdiff in enumerate(diffEjs):
#     for j, Ej2 in enumerate(Ej2s):
#         Ej3 = Ej1 + Ejdiff

#         zz12, zz23, zz13, zzz = single_zz(1, 1, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13)
#         vals[i, j] = zzz
o1, _ = omega_alphas(1, Ej1s, True)
o2, _ = omega_alphas(1, Ej2s, True)
o3, _ = omega_alphas(1, Ej3, True)
ocprim = o2 - (o1 + o3) / 2
detun = o1 - o3
plt.pcolor(ocprim, detun, zz13, norm=colors.SymLogNorm(1e-6, vmin=-1e-1, vmax=1e-1), cmap=OrBu_colormap())
plt.xlabel("coupler prim [Ec]")
plt.ylabel("Detuning [Ec]")
plt.colorbar()
plt.show()
