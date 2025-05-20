# how different is the clever vs the naive translation of parameters
from exact.util import omega_alphas, gconstant, Eint_to_g
from matplotlib import pyplot as plt
import numpy as np

# here we compare different ways to translate different parameters

Ej = np.linspace(0, 150, 40)
fancyo, fancya = omega_alphas(1, Ej, True)
simpleo, _ = omega_alphas(1, Ej, False)

# Omega
plt.title("Omega from fancy mathieu or sqrt approx, Ec=1")
plt.plot(Ej, simpleo, label="simple approx")
plt.plot(Ej, fancyo, label="fancy")
plt.xlabel("Ej [Ec]")
plt.legend()

# Alpha
plt.figure()
plt.title("Alpha from matheiu energies Ec=1")
plt.xlabel("Ej")
plt.ylabel("alpha")
plt.plot(Ej, fancya)

# g
Ej1 = 50
Ej2 = 50
Eints = np.linspace(0, 0.6, 40)
gs_fancy = [Eint_to_g(Ej1, Ej2, Eint) for Eint in Eints]
gs_approx = [gconstant(1, Ej1, 1, Ej2, Eint) for Eint in Eints]

plt.figure()
plt.xlabel("Eint")
plt.title(f"g from approx or fancy numeric Ec1=Ec2=1 Ej1={Ej1} Ej2={Ej2}")
plt.plot(Eints, gs_fancy, label="Fancy num")
plt.plot(Eints, gs_approx, label="Approx model")
plt.legend()

# g again
Ej2 = 50
Eint = 0.1
Ejs = np.linspace(0, 100, 100)
gs_fancy = [Eint_to_g(Ej1, Ej2, Eint) for Ej1 in Ejs]
gs_approx = [gconstant(1, Ej1, 1, Ej2, Eint) for Ej1 in Ejs]

plt.figure()
plt.xlabel("Ej1")
plt.title(f"g from approx or fancy numeric Ec1=Ec2=1 Eint={Eint} Ej2={Ej2}")
plt.plot(Ejs, gs_fancy, label="Fancy num")
plt.plot(Ejs, gs_approx, label="Approx model")
plt.legend()
plt.show()
