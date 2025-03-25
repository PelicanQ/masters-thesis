from sim_store.analysis.conv import grid3d
from .hamil import calc_eig
import numpy as np

# now we check the lowest levels for some Eint
k = 25
collection = []
level_select = [1, 2, 3, 4, 5, 6]
Ejs = [1, 10, 100]
Eints = np.arange(0, 1.5, step=0.02)

for j, Ej in enumerate(Ejs):
    levels = np.zeros(shape=(len(level_select), len(Eints)))
    levels[:] = np.nan
    for i, Eint in enumerate(Eints):
        vals = calc_eig(Ej=Ej, Eint=Eint, k=25)
        levels[:, i] = vals[level_select] - vals[0]
    collection.append(levels)

grid3d(
    xx=Eints,
    collection=collection,
    params=Ejs,
    param_name="Ej",
    suptitle=f"How do levels vary with Eint?, k={k}",
    xlabel="Eint",
    ylabel="En(k)-E0(k)",
    labels=[f"E{l}" for l in level_select],
    marker=None,
)
