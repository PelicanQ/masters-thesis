from hamil import calc_eig
import numpy as np
import cupy as cp
import pandas as pd
from matplotlib import pyplot as plt
import time


# this data informs running time of 2 transmon calc function given size k

d = pd.read_csv("./calc_time.csv", header=None, index_col=False).to_numpy()

kk = d[0, :]
t = d[1, :]
p2 = np.polyfit(kk, t, deg=2)
p3 = np.polyfit(kk, t, deg=3)
p4 = np.polyfit(kk, t, deg=4)
xx = np.arange(np.min(kk), np.max(kk), step=0.2)
pvals2 = np.polyval(p2, xx)
pvals3 = np.polyval(p3, xx)
pvals4 = np.polyval(p4, xx)

plt.plot(kk, t, label="time", marker="o", linewidth=0)
plt.plot(xx, pvals2, label="fit2")
plt.plot(xx, pvals3, label="fit3")
plt.plot(xx, pvals4, label="fit4")

plt.xlabel("truncation size k")
plt.ylabel("time (seconds)")
plt.title("Time to calc eigenvals of 2 transmon matrix vs truncation k")
plt.legend()
plt.show()

# to generate data
# kk = np.concatenate([[45, 55, 65]])
# times = []
# vals = calc_eig(10, 20)  # warm up for accurate data
# for k in kk:
#     t1 = time.time()
#     vals = calc_eig(
#         10, Eint=0.2, k=k
#     )  # I dont expect Ej or Eint to impact running time
#     t2 = time.time()
#     times.append(t2 - t1)

# df = pd.DataFrame((kk, times))
# df.to_csv("./calc_time2.csv", header=False, index=False)

# plt.plot(kk, times)
# plt.ylabel("time seconds")
# plt.xlabel("k")
# plt.show()
