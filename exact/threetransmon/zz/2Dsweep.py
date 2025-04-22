import matplotlib.pyplot as plt
from exact.twotransmon.zz.zz import single_zz
import numpy as np
from store.stores import Store_zz3T
from other.colormap import OrBu_colormap, Norm

Ejs = np.arange(30, 80, 0.2)
Eints = np.arange(0, 0.5, 0.01)
zz12, zz23, zz13, zzz = Store_zz3T.plane(
    "Ej1", Ejs, 1, "Eint12", Eints, 2, Ej2=50, Ej3=60, Eint23=0.2, Eint13=0, Ec2=1, Ec3=1
)
plt.pcolor(Ejs, Eints, zz12, cmap=OrBu_colormap(), norm=Norm(1e1))
plt.xlabel("Ej1")
plt.ylabel("Eint12")
plt.title("ZZ12, Eint23=0.2, Eint13=0, Ej2=50 Ej3=60")
plt.colorbar()
plt.show()
