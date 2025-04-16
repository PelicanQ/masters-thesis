# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap
import numpy as np
from matplotlib import pyplot as plt
from jobmanager.util import collect_jobs
from anharm.Hamiltonian import Hamil
from matplotlib import colors
from exact.threetransmon.zz.zz import single_zz
from store.stores import Store_zz3T

Ej3 = 50
Ej1s = np.arange(30, 80, 1)
Ej2s = np.arange(30, 80, 1)
Eint12 = 0.1
Eint23 = 0.1
Eint13 = 0

zz12, zz23, zz13, zzz = Store_zz3T.plane(
    "Ej1", Ej1s, "Ej2", Ej2s, Ej3=Ej3, Eint12=Eint12, Eint23=Eint23, Eint13=Eint13, Ec2=1, Ec3=1
)
# for i, Ejdiff in enumerate(diffEjs):
#     for j, Ej2 in enumerate(Ej2s):
#         Ej3 = Ej1 + Ejdiff

#         zz12, zz23, zz13, zzz = single_zz(1, 1, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13)
#         vals[i, j] = zzz
plt.pcolor(Ej1s, Ej2s, zzz, norm=colors.SymLogNorm(1e-6, vmin=-1e-1, vmax=1e-1), cmap=OrBu_colormap())
plt.colorbar()
plt.show()
