from matplotlib import pyplot as plt
from store.stores import Store_zz3T
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# vars, zz12, zz23, zz13, zzz = Store_zz3t.line(Ec2=1, Ec3=1, Ej2=50, Ej3=50, Eint12=0.1, Eint23=0.1, Eint13=0.1)
# zz12, zz23, zz13, zzz = Store_zz3t.get_all()

Ej1s = np.arange(30, 90, 0.5)
Ej3s = np.arange(30, 70, 0.5)
zz12, zz23, zz13, zzz = Store_zz3T.plane(
    "Ej1", Ej1s, "Ej3", Ej3s, Ec2=1, Ec3=1, Ej2=50, Eint12=0.1, Eint23=0.1, Eint13=0.1
)

A = np.array([zz12, zz23, zz13, zzz])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection="3d")
scatter = ax.scatter(A[0, :], A[1, :], A[2, :], c=A[3, :])
plt.colorbar(scatter, ax=ax)
plt.show()
