# Let's see if ZZZ correlates with the other 3 ZZ
from store.stores import Store_zz3t
import numpy as np

vars, zz12, zz23, zz13, zzz = Store_zz3t.line(Ec2=1, Ec3=1, Ej2=50, Eint12=0.1, Eint23=0.1, Eint13=0.1)

v1 = np.array([0, 0, 0, 1])
v2 = np.array([0, 0, 1, 0])
print(res)
