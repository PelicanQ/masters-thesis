import numpy as np
from matplotlib import pyplot as plt
from exact.twotransmon.zz.sweep import sweep_Ej1
from exact.util import omega_alphas, gconstant

# Ec1 = Ec2 = 1 the unit
Ej2 = 60
Eint = 0.1
Ej1 = np.arange(20, 300, 10)

gs = gconstant(1, Ej1, 1, Ej2, Eint)
omegas1, alphas1 = omega_alphas(1, Ej1, True)
omega2, alpha2 = omega_alphas(1, Ej2, True)

plt.plot(Ej1, omegas1, label="omega", color="r")
plt.legend(loc="upper left")
plt.xlabel("Ej [Ec]")
plt.ylabel("omega")
plt.title("omega and alpha of transmon1 vs Ej")
plt.twinx()
plt.plot(Ej1, alphas1, label="alpha")
plt.legend(loc="upper right")
plt.ylabel("alpha")

plt.figure()
plt.plot(Ej1, gs)
plt.title(f"g constant [Ec], Ej2={Ej2}, Eint={Eint}")
plt.xlabel("Ej1 [Ec]")
plt.show()
