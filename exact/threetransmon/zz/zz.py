from exact.threetransmon.hamil import eig_clever, eig_excitation_trunc
import numpy as np
from exact.gale_shapely.gale_shapely import state_assignment
import time


def single_zz_energy(Ec2, Ec3, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, k=8):
    # t1 = time.perf_counter()
    # print("start eig")
    levels = eig_clever(Ec2, Ec3, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, k=k, only_energy=True)
    # t2 = time.perf_counter()
    # print("Eig: ", t2 - t1)
    return levels


def single_zz(Ec2, Ec3, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, k=8):
    levels, vecs, index_map = eig_excitation_trunc(Ec2, Ec3, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, k=k)
    bare_to_dressed_index = state_assignment(eigen_states=vecs)
    levels = levels - levels[0]

    def gslevel(n1, n2, n3):
        return levels[bare_to_dressed_index[index_map[(n1, n2, n3)]]]

    zzGS12 = gslevel(1, 1, 0) - gslevel(1, 0, 0) - gslevel(0, 1, 0)
    zzGS23 = gslevel(0, 1, 1) - gslevel(0, 1, 0) - gslevel(0, 0, 1)
    zzGS13 = gslevel(1, 0, 1) - gslevel(1, 0, 0) - gslevel(0, 0, 1)
    zzzGS = gslevel(1, 1, 1) - (gslevel(1, 0, 0) + gslevel(0, 1, 0) + gslevel(0, 0, 1))

    return zzGS12, zzGS23, zzGS13, zzzGS


if __name__ == "__main__":
    single_zz(1, 1, 50, 50, 50, 0.1, 0.1, 0.1, 10)
