from exact.twotransmon.hamil import eig_clever
import numpy as np
from matplotlib import pyplot as plt
from exact.twotransmon.gale_shapley import state_assignment
from exact.util import index_map


def single_zz(Ec2, Ej1, Ej2, Eint, k=15):
    N = 2 * k + 1  # transmon states per subspace
    idx_map = index_map(N)
    levels, vecs = eig_clever(Ej1=Ej1, Ej2=Ej2, Eint=Eint, Ec2=Ec2, k=k, ng1=0)
    bare_to_dressed_index, _ = state_assignment(eigen_states=vecs)
    btd = bare_to_dressed_index  # maps bare hamil index to index in vecs/levels of dressed state
    d0 = btd[idx_map[0][0]]
    d1 = btd[idx_map[0][1]]
    d2 = btd[idx_map[1][0]]
    d3 = btd[idx_map[1][1]]

    zz = levels[4] - (levels[1] + levels[2]) + levels[0]
    zzGS = levels[d3] - (levels[d2] + levels[d1]) + levels[d0]  # ZZ after gale shapely state assignment
    return zz, zzGS


def sweep_Eint(Ej1, Ej2, Eints, k):
    zzs = np.zeros(shape=(len(Eints),))
    zzsGS = np.zeros(shape=(len(Eints),))
    N = 2 * k + 1  # transmon states per subspace
    idx_map = index_map(N)
    for j, Eint in enumerate(Eints):
        levels, vecs = eig_clever(Ej1=Ej1, k=k, Ej2=Ej2, Eint=Eint)
        bare_to_dressed_index, _ = state_assignment(eigen_states=vecs)
        btd = bare_to_dressed_index  # maps bare hamil index to index in vecs/levels of dressed state
        # for q in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        #     for a, b in enumerate(btd):
        #         # look for the q level. (levels is ordered)
        #         if b == q:
        #             # a is the bare being mapped to the third level/state
        #             m = a // N
        #             print(f"|{m} {a - m * N}>  ", end="")
        # print(" ")
        d0 = btd[idx_map[0][0]]
        d1 = btd[idx_map[0][1]]
        d2 = btd[idx_map[1][0]]
        d3 = btd[idx_map[1][1]]

        zz = levels[4] - (levels[1] + levels[2]) + levels[0]
        zzGS = levels[d3] - (levels[d2] + levels[d1]) + levels[d0]  # ZZ after gale shapely state assignment
        zzs[j] = zz
        zzsGS[j] = zzGS
    return zzs, zzsGS


def sweep_Ej1(Ej1s, Ej2, Eint, k):
    zzs = np.zeros(shape=(len(Ej1s),))
    zzsGS = np.zeros(shape=(len(Ej1s),))
    N = 2 * k + 1  # transmon states per subspace
    idx_map = index_map(N)
    for j, Ej1 in enumerate(Ej1s):
        levels, vecs = eig_clever(Ej1=Ej1, k=k, Ej2=Ej2, Eint=Eint)
        bare_to_dressed_index, _ = state_assignment(eigen_states=vecs)
        btd = bare_to_dressed_index  # maps bare hamil index to index in vecs/levels of dressed state
        # for q in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        #     for a, b in enumerate(btd):
        #         # look for the q level. (levels is ordered)
        #         if b == q:
        #             # a is the bare being mapped to the third level/state
        #             m = a // N
        #             print(f"|{m} {a - m * N}>  ", end="")
        # print(" ")
        d0 = btd[idx_map[0][0]]
        d1 = btd[idx_map[0][1]]
        d2 = btd[idx_map[1][0]]
        d3 = btd[idx_map[1][1]]

        # print(d0, d1, d2, d3)

        zz = levels[4] - levels[2] - levels[1] + levels[0]
        zzGS = levels[d3] - levels[d2] - levels[d1] + levels[d0]
        zzs[j] = zz
        zzsGS[j] = zzGS
    return zzs, zzsGS


if __name__ == "__main__":

    # sweep Ej1
    Ej1s = np.arange(40, 130, 2)
    Ej2 = 80
    Eint = 0.15
    k = 10
    zzs = sweep_Ej1(Eint=Eint, Ej1s=Ej1s, Ej2=Ej2, k=k)
    plt.plot(Ej1s, zzs, marker=".")
    plt.title(f"ZZ, k={k}, Ej2={Ej2}, Eint={Eint}")
    plt.xlabel("Ej1 [Ec]")
    plt.ylabel("ZZ [Ec]")
    plt.show()
