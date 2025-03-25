from ..hamil import eig_clever
import numpy as np
from matplotlib import pyplot as plt
from ..gale_shapley import state_assignment

Ej1s = np.arange(40, 130, 2)
res = []
k = 10
Ej2 = 80
Eint = 0.15
N = 2 * k + 1  # transmon states per subspace
for j, Ej1 in enumerate(Ej1s):
    levels, vecs, idx_map = eig_clever(Ej1=Ej1, k=k, Ej2=Ej2, Eint=Eint)
    bare_to_dressed_index, _ = state_assignment(eigen_states=vecs)
    btd = bare_to_dressed_index  # maps bare hamil index to index in vecs/levels of dressed state
    for q in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        for a, b in enumerate(btd):
            # look for the q level. (levels is ordered)
            if b == q:
                # a is the bare being mapped to the third level/state
                m = a // N
                print(f"|{m} {a - m * N}>  ", end="")
    print(" ")
    d0 = btd[idx_map[0][0]]
    d1 = btd[idx_map[0][1]]
    d2 = btd[idx_map[1][0]]
    d3 = btd[idx_map[1][1]]

    # print(d0, d1, d2, d3)

    zz = levels[d3] - levels[d2] - levels[d1] + levels[d0]
    res.append(zz)

plt.plot(Ej1s, res, marker=".")
plt.title(f"ZZ, k={k}, Ej2={Ej2}, Eint={Eint}")
plt.xlabel("Ej1 [Ec]")
plt.ylabel("ZZ [Ec]")
plt.show()
