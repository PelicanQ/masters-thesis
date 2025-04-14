from exact.twotransmon.hamil import eig_clever
import numpy as np
from matplotlib import pyplot as plt

# conclusion, yes k=8 is good

kk = np.arange(5,15, 1)
levels = np.zeros((len(kk), 5))
for i,k in enumerate(kk):
    vals = eig_clever(50,40, 0.5, 1, k=k,only_energy=True)
    vals = vals - vals[0]
    levels[i,:] = vals[:5]

rel = levels - levels[-1,:]
plt.plot(kk,levels, marker=".")
plt.figure()
plt.plot(kk,rel, marker=".")
plt.xlabel("k")
plt.show()