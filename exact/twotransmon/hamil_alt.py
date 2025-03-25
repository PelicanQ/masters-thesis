# Here I want to run diagonalization on the hamitonian in the transmon eigenstates basis
import numpy as np
import cupy as cp
import scipy.linalg as spalg
from numpy.typing import NDArray


def alt_calc_eig(Ej, Eint=1, k=20):
    #  get eigenvalues
    # Ej same for both
    # Eint interaction energy

    N = 2 * k + 1  # size of matrix of one product transmon space
    nstates = np.arange(-k, k + 1, step=1)  # (-k .. -1, 0, 1 .. k) is our order of basis

    Ec = 1  # same Ec for both transmons, we use this Ec units

    vals, vecs = spalg.eigh_tridiagonal(np.square(nstates) * 4 * Ec, -np.ones(N - 1) * Ej / 2)
    D = np.diag(vals)
    n1 = np.diag(nstates)
    n1 = vecs.T @ n1 @ vecs

    Hint = 4 * Eint * np.kron(n1, n1)
    I = np.eye(N, N)
    H = np.kron(D, I) + np.kron(I, D) + Hint

    H = cp.asarray(H)

    vals = cp.linalg.eigvalsh(H)
    vals = cp.asnumpy(vals)
    sorted = np.sort(vals)

    return sorted


# this one is outdated because it is to specific, remove if you change the dependent file to new
def clever_calc_eig(Ej, Eint=1, k=20):
    # get eigenvalues
    # Ej same for both
    # Eint interaction energy
    C = 200  # first trunc. Controls number of charge states
    nstates = np.arange(-C, C + 1, step=1)

    Ec = 1  # fixed and is our unit

    N = 2 * k + 1  # second trunc, number of bare states (from 0 to N)
    vals, vecs = spalg.eigh_tridiagonal((np.square(nstates) * 4 * Ec), (-np.ones(2 * C) * Ej / 2))
    vals = vals[:N]
    D = np.diag(vals)

    n1: NDArray = vecs.T @ np.diag(nstates) @ vecs  # change to transmon basis
    n1 = n1[:N, :N]
    n2 = n1.copy()

    Hint = 4 * Eint * np.kron(n1, n2)

    I = np.eye(N, N)
    H = np.kron(D, I) + np.kron(I, D) + Hint

    H = cp.asarray(H)
    vals = cp.linalg.eigvalsh(H)

    return cp.asnumpy(vals)
