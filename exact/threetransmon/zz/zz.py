from exact.threetransmon.hamil import eig_clever
import numpy as np
from exact.gale_shapely import state_assignment
from exact.util import index_map3T
import time

def single_zz(Ec2, Ec3, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13,k=12):
    N = 2 * k + 1  # transmon states per subspace
    idx_map = index_map3T(N)
    levels, vecs = eig_clever(Ec2, Ec3, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, k=k)
    bare_to_dressed_index, _ = state_assignment(eigen_states=vecs)
    btd = bare_to_dressed_index  # maps bare hamil index to index in vecs/levels of dressed state

    def gslevel(n1, n2, n3):
        return levels[btd[idx_map[n1][n2][n3]]]

    zzGS12 = gslevel(1,1,0) - gslevel(1,0,0) - gslevel(0,1,0) + gslevel(0,0,0)
    zzGS23 = gslevel(0,1,1) - gslevel(0,1,0) - gslevel(0,0,1) + gslevel(0,0,0)
    zzGS13 = gslevel(1,0,1) - gslevel(1,0,0) - gslevel(0,0,1) + gslevel(0,0,0)
    zzzGS = gslevel(1,1,1) - (gslevel(1,0,0)+gslevel(0,1,0)+gslevel(0,0,1)) + 2*gslevel(0,0,0)

    return zzGS12, zzGS23, zzGS13, zzzGS

if __name__ == "__main__":
    t1 = time.time()
    single_zz(1,1,50,50,50,0.1,0.1,0.1,10)
    t2 = time.time()
    print(t2-t1)