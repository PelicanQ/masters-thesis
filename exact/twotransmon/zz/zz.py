from exact.twotransmon.hamil import eig_clever
import numpy as np
from matplotlib import pyplot as plt
from exact.gale_shapely.gale_shapely import state_assignment
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
    levels = levels - levels[0]
    zz = levels[4] - (levels[1] + levels[2]) 
    zzGS = levels[d3] - (levels[d2] + levels[d1])  # ZZ after gale shapely state assignment
    return zz, zzGS


if __name__ == "__main__":
    pass
