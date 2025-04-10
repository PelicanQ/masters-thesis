from store.stores import Store_zz3t
import numpy as np
from matplotlib import pyplot as plt

vars, zz12, zz23, zz13, zzz = Store_zz3t.line(Ec2=1, Ec3=1, Ej2=50, Ej3=50,Eint12=0.1, Eint23=0.1, Eint13=0.1)
plt.plot(vars,zzz)
plt.show()