import matplotlib.pyplot as plt
from exact.twotransmon.zz.zz import single_zz
import numpy as np
from store.stores import Store_zz2T

Ejs = np.arange(30, 90, 0.2)
Eints = np.arange(0, 0.8, 0.02)
zz, zzGS = Store_zz2T.plane("Ej1", Ejs, "Eint", Eints, Ej2=50, Ec2=1)
plt.pcolor(Ejs, Eints, zzGS)
plt.xlabel("Ej1")
plt.ylabel("Eint")
plt.colorbar()
plt.title("ZZ Ej2=50")
plt.show()
