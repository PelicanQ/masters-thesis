from exact.five.hamil import eig
from exact.gale_shapely.gale_shapely import state_assignment


def single_zz(Ej1, Ej2, Ej3, Ej4, Ej5, Eint12, Eint23, Eint13, Eint34, Eint45, Eint35):
    levels, vecs, index_map = eig(Ej1, Ej2, Ej3, Ej4, Ej5, Eint12, Eint23, Eint13, Eint34, Eint45, Eint35, N=12, M=14)
    bare_to_dressed_index = state_assignment(eigen_states=vecs)
    levels = levels - levels[0]

    def gslevel(n1, n2, n3, n4, n5):
        return levels[bare_to_dressed_index[index_map[(n1, n2, n3, n4, n5)]]]

    zz13 = gslevel(1, 0, 1, 0, 0) - gslevel(1, 0, 0, 0, 0) - gslevel(0, 0, 1, 0, 0)
    zz35 = gslevel(0, 0, 1, 0, 1) - gslevel(0, 0, 1, 0, 0) - gslevel(0, 0, 0, 0, 1)
    zz15 = gslevel(1, 0, 0, 0, 1) - gslevel(1, 0, 0, 0, 0) - gslevel(0, 0, 0, 0, 1)
    zzz135 = gslevel(1, 0, 1, 0, 1) - (gslevel(1, 0, 0, 0, 0) + gslevel(0, 0, 1, 0, 0) + gslevel(0, 0, 0, 0, 1))
    return zz13, zz35, zz15, zzz135
