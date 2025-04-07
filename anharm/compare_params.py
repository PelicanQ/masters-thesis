# how different is the clever vs the naive translation of parameters
from exact.util import omega_alphas, gconstant, Eint_to_g_Eint, Eint_to_g_Ej, gconstant
from matplotlib import pyplot as plt
import numpy as np

# here we compare different ways to translate different parameters

plt.title("Omega [Ec] comparison, Ec=1")
Ej = np.linspace(0, 80, 20)
fancyo, fancya = omega_alphas(1, Ej, True)
simpleo, simplea = omega_alphas(1, Ej, False)
plt.plot(Ej, simpleo, label="simple")
plt.plot(Ej, fancyo, label="fancy")
plt.legend()

plt.figure()
plt.title("Alpha comparison")
plt.xlabel("Ej")
plt.plot(Ej, simplea, label="simple")
plt.plot(Ej, fancya, label="fancy")

plt.figure()
plt.title("g vs Eint [Ec]=Ec1=Ec2=1")
Eints = np.linspace(0, 2, 40)
gs = Eint_to_g_Eint(50, 50, Eints)
gs_app = [gconstant(1, 50, 1, 50, Eint) for Eint in Eints]

plt.xlabel("Eint")
plt.plot(Eints, gs, marker=".", label="num")
plt.plot(Eints, gs_app, marker=".", label="approx")
plt.legend()

plt.figure()
Ej2 = 50
Eint = 0.1
plt.title(f"g vs Ej1 [Ec1=Ec2], Ej2={Ej2}, Eint={Eint}")
Ej1 = np.linspace(0, 90, 100)
gs_app = gconstant(1, Ej1, 1, Ej2, Eint)
gs = Eint_to_g_Ej(Ej1, Ej2, 0.1)
plt.plot(Ej1, gs, label="num")
plt.plot(Ej1, gs_app, label="approx")
plt.xlabel("Ej1")
plt.legend()
plt.show()
