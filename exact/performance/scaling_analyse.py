import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# TODO fill up with more data, find two distinct linear regions
# compare scaling with numpy. Is numpy ^3 and cupy ^2 ?
files = [
    "timeA.csv",
    "timeB.csv",
    "timeC.csv",
    "timeD.csv",
    "timeE.csv",
    "timeF.csv",
]
xx = []
yy = []
for file in files:
    arr = pd.read_csv(file, index_col=False, header=None).to_numpy()
    xx.extend(arr[0])
    yy.extend(arr[1])

plt.plot(xx, yy, marker=".")
plt.title("Time of cupy eigvalsh()")
plt.ylabel("Time seconds")
plt.xlabel("Matrix size")
plt.show()
