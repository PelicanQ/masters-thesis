# in the case of line layout, equal Ej1,3 and good bit lower Ej2, this is the bare ordering
from exact.threetransmon.hamil import eig_excitation_trunc
import numpy as np
from matplotlib import pyplot as plt

Ejs = np.arange(40, 80, 0.5)
r12 = []
r23 = []
r13 = []
rzzz = []
for Ej in Ejs:
    levels, _ = eig_excitation_trunc(1, 1, Ej, 50, 52, 0.1, 0.1, 0.1, only_energy=True)
    levels = levels - levels[0]
    zz12 = levels[5] - (levels[1] + levels[2])
    zz23 = levels[9] - (levels[2] + levels[3])
    zz13 = levels[6] - (levels[1] + levels[3])
    zzz = levels[17] - (levels[1] + levels[2] + levels[3])
    r12.append(zz12)
    r23.append(zz23)
    r13.append(zz13)
    rzzz.append(zzz)

plt.plot(Ejs, r12, label="zz12")
plt.plot(Ejs, r23, label="zz23")
plt.plot(Ejs, r13, label="zz13")
plt.plot(Ejs, rzzz, label="zzz")
plt.title("adiabatic starting from Ej1=40 Ej2=50 Ej3=52 triang Eints=0.1")
# plt.title("adiabatic  starting from Ej2=30 Line Eints12,23=0.2 Ej1=50 Ej3=55")
plt.xlabel("Ej1")
plt.legend()
plt.show()
