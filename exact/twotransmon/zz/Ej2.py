from ..hamil import eig_clever
import numpy as np
from matplotlib import pyplot as plt
from ..gale_shapley import state_assignment
from sim_store.analysis.plot import grid_plot2d

Ej1s = np.arange(10, 80, 1)
k = 12
Eints = [0.01, 0.05, 0.1, 0.5]
Ej2 = 50
coll = np.zeros((len(Eints), len(Ej1s)))

for i, Eint in enumerate(Eints):
    for j, Ej1 in enumerate(Ej1s):
        levels, vecs, idx_map = eig_clever(Ej1=Ej1, k=k, Ej2=Ej2, Eint=Eint)
        bare_to_dressed_index, _ = state_assignment(eigen_states=vecs)
        btd = bare_to_dressed_index
        # for a, b in enumerate(btd):
        # if b == 3:
        # m = a // 21
        # print("Level 3: state", m, a - m * 21)
        d0 = btd[idx_map[0][0]]
        d1 = btd[idx_map[0][1]]
        d2 = btd[idx_map[1][0]]
        d3 = btd[idx_map[1][1]]

        # print(d0, d1, d2, d3)

        zz = levels[d3] - levels[d2] - levels[d1] + levels[d0]
        coll[i, j] = zz

grid_plot2d(
    xx=Ej1s,
    collection=coll,
    params=Eints,
    param_name="Eint",
    suptitle=f"ZZ vs Ej1, varying Eint, k={k}, Ej2={Ej2}",
    xlabel="Ej1 [Ec]",
    ylabel="ZZ [Ec]",
)
