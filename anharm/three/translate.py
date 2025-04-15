import scipy.special as spec
import numpy as np
import scipy.linalg as spalg
from matplotlib import pyplot as plt
from exact.onetransmon.hamil import calc_eigs
from exact.util import index_map2T, index_map3T, kron
from numpy.typing import NDArray
import cupy as cp


def interaction_ops(Ec2, Ec3, Ej1, Ej2, Ej3):
    """
    k: controls how many transmon eigenstates are included per qubit
    units of Ec1
    Returns:
        eigenvalues and eigenvectors in bare basis
    """
    C = 20
    nstates = np.arange(-C, C + 1, step=1)
    ndiag = np.square(nstates)
    _, vecs1 = spalg.eigh_tridiagonal(ndiag * 4 * 1, -np.ones(2 * C) * Ej1 / 2)
    _, vecs2 = spalg.eigh_tridiagonal(ndiag * 4 * Ec2, -np.ones(2 * C) * Ej2 / 2)
    _, vecs3 = spalg.eigh_tridiagonal(ndiag * 4 * Ec3, -np.ones(2 * C) * Ej3 / 2)

    N = 2  # transmon trunc. Include only 0 and 1 states

    ndiag = np.diag(nstates)
    n1 = vecs1.T @ ndiag @ vecs1  # change into transmon bare basis
    n2 = vecs2.T @ ndiag @ vecs2
    n3 = vecs3.T @ ndiag @ vecs3

    n1 = n1[:N, :N]  # truncate to NxN
    n2 = n2[:N, :N]
    n3 = n3[:N, :N]

    return n1, n2, n3


def Eints_to_g_Ej(Ej1s: np.ndarray, Ej2, Ej3, Eint12, Eint23, Eint13):
    g12 = np.zeros_like(Ej1s)
    g23 = np.zeros_like(Ej1s)
    g13 = np.zeros_like(Ej1s)
    for i in range(len(Ej1s)):
        n1, n2, n3 = interaction_ops(1, 1, Ej1s[i], Ej2, Ej3)
        g12[i] = 4 * Eint12 * np.abs(n1[1, 0] * n2[0, 1])
        g23[i] = 4 * Eint23 * np.abs(n2[1, 0] * n3[0, 1])
        g13[i] = 4 * Eint13 * np.abs(n1[1, 0] * n3[0, 1])
    # absolute because signs may flip during eig resulting in a flipping sign of g which is annoying.
    # I think this translation should make sense, that the sign of Eints and gs are the same
    return g12, g23, g13


# def Eint_to_g_Eint(Ej1s, Ej2, Ej3, Eint12, Eint23, Eint13):
#     n1, n2, n3 = interaction_ops(Ej1, Ej2)
#     gs = 4 * Eints * Hint[imap[0][1], imap[1][0]]
#     return np.abs(gs)
