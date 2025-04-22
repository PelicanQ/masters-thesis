import scipy.special as spec
import numpy as np
import scipy.linalg as spalg
from matplotlib import pyplot as plt
from exact.onetransmon.hamil import calc_eigs
from exact.util import index_map2T


def interaction_term(Ej1, Ej2):
    """Interaction Hamiltonian for 2T"""
    C = 50  # charge trunc
    nstates = np.arange(-C, C + 1, step=1)

    _, vecs1 = spalg.eigh_tridiagonal(np.square(nstates) * 4 * 1, -np.ones(2 * C) * Ej1 / 2)
    _, vecs2 = spalg.eigh_tridiagonal(np.square(nstates) * 4 * 1, -np.ones(2 * C) * Ej2 / 2)

    n1 = np.diag(nstates)
    n2 = np.diag(nstates)
    # change into transmon bare basis
    n1 = vecs1.T @ n1 @ vecs1
    n2 = vecs2.T @ n2 @ vecs2

    trunc = 2  # transmon trunc
    n1 = n1[:trunc, :trunc]  # truncate
    n2 = n2[:trunc, :trunc]
    interact = np.kron(n1, n2)
    # return the interaction matrix between 00 01 10 11
    return interact


def Eint_to_g_Ej(Ej1s: np.ndarray, Ej2, Eint):
    gs = np.zeros(Ej1s.shape)
    imap = index_map2T(2)
    for i in range(len(Ej1s)):
        Hint = interaction_term(Ej1s[i], Ej2)
        gs[i] = 4 * Eint * Hint[imap[0][1], imap[1][0]]
    # absolute because signs may flip. Keep in mind for larger systems when sign of g can matter
    return np.abs(gs)


def Eint_to_g_Eint(Ej1, Ej2, Eints: np.ndarray):
    Hint = interaction_term(Ej1, Ej2)
    imap = index_map2T(2)
    gs = 4 * Eints * Hint[imap[0][1], imap[1][0]]
    return np.abs(gs)
