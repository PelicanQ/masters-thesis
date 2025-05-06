from exact.four.hamil import eig
import numpy as np
from exact.gale_shapely.gale_shapely import state_assignment
import time

type StateType = tuple[int, int, int, int]


def str2state(st: str):
    return tuple(map(int, tuple(st)))


def get_bottom_states(top: str):
    bottomstates: list[StateType] = []
    for i, c in enumerate(top):
        if c == "1":
            s = [0, 0, 0, 0]
            s[i] = 1
            bottomstates.append(tuple(s))
    return bottomstates


def single_zz(Ej1, Ej2, Ej3, Ej4, Eint12, Eint23, Eint13, Eint34):
    levels, vecs, index_map = eig(Ej1, Ej2, Ej3, Ej4, Eint12, Eint23, Eint13, Eint34, N=11, M=14)
    bare_to_dressed_index = state_assignment(eigen_states=vecs)
    levels = levels - levels[0]

    def gslevel(state: StateType):
        return float(levels[bare_to_dressed_index[index_map[state]]])

    def get_zz(zzstate: str):
        top_energy = gslevel(str2state(zzstate))
        bottom_states = get_bottom_states(zzstate)
        bottom_energies = sum(map(gslevel, bottom_states))
        # print(bottom_energies)
        return top_energy - bottom_energies

    results = {
        "zz12": get_zz("1100"),
        "zz23": get_zz("0110"),
        "zz34": get_zz("0011"),
        "zz13": get_zz("1010"),
        "zz24": get_zz("0101"),
        "zz14": get_zz("1001"),
        "zzz123": get_zz("1110"),
        "zzz134": get_zz("1011"),
        "zzz124": get_zz("1101"),
        "zzz234": get_zz("0111"),
        "zzzz": get_zz("1111"),
    }
    return results


if __name__ == "__main__":
    r = single_zz(50, 50, 50, 50, 0.1, 0.1, 0.1, 0.1)
    print(r)
    pass
