import matplotlib.pyplot as plt
from exact.twotransmon.zz.zz import single_zz
import numpy as np

Ejs = np.arange(30, 90, 1)
Eints = np.arange(0, 1, 0.1)
p = np.zeros((len(Eints), len(Ejs)))
for i, Eint in enumerate(Eints):
    for j, Ej in enumerate(Ejs):  
        zz, zzGS = single_zz(1, Ej, 50, Eint, k=8)
        p[i, j] = zzGS

plt.pcolor(Ejs, Eints, p)
plt.xlabel("Ej")
plt.ylabel("Eint")
plt.colorbar()
plt.show()