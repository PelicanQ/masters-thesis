import pandas as pd
import numpy as np
from anharm.Hgen import Hgen
from exact.twotransmon.zz.zz import sweep_Ej1
import timeit

# This are the parameters which generated the file
# Ej2 = 60
# Eint = 0.15
# Ej1 = np.arange(30, 90, 0.1)

Ej2 = 60
Eint = 0.15
Ej1 = np.arange(30, 90, 0.1)


def run():
    zzs = sweep_Ej1(Ej1, Ej2=Ej2, Eint=Eint, k=14)
    np.save("./test.npy", zzs)


t = timeit.timeit(run, number=1)
print(t)
