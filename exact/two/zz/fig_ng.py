from ..hamil import eig_clever
import numpy as np
from matplotlib import pyplot as plt
from ..gale_shapley import state_assignment

dd = np.arange(-4, 4, 0.1)
ngs = np.arange(-2, 2, 0.1)
res = np.zeros((len(ngs), len(dd)))  # zz grid
zerorow = np.abs(ngs - 0).argmin()  # which row is ng=0?
k = 9
omega2 = 5
N = 2 * k + 1  # transmon states per subspace
for i, ng in enumerate(ngs):
    for j, d in enumerate(dd):
        levels, vecs, idx_map = eig_clever(d, k=k, ng1=ng, w2=omega2)
        bare_to_dressed_index, _ = state_assignment(eigen_states=vecs)
        btd = bare_to_dressed_index  # maps bare hamil index to index in vecs/levels of dressed state
        d0 = btd[idx_map[0][0]]
        d1 = btd[idx_map[0][1]]
        d2 = btd[idx_map[1][0]]
        d3 = btd[idx_map[1][1]]

        # print(d0, d1, d2, d3)

        zz = levels[d3] - levels[d2] - levels[d1] + levels[d0]
        res[i, j] = zz
res = res - res[zerorow, :]
plt.imshow(res, extent=[dd[0], dd[-1], ngs[-1], ngs[0]], aspect="auto")
plt.title(f"ZZ [g], $\omega_2$={omega2}, k={k}")
plt.xlabel("delta [g]")
plt.ylabel("ng")
plt.colorbar()
plt.show()
