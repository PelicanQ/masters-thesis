# Here I will try to expand the two transmon Hamiltonian in the charge basis
import numpy as np
import cupy as cp
from matplotlib import pyplot as plt
import scipy.linalg as spalg
from numpy.typing import NDArray


def kron(*mats):
    total = mats[0]
    for i in range(1, len(mats)):
        total = cp.kron(total, mats[i])
    return total


# this is the good one now
def eig_clever(
    Ec2, Ec3, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, only_energy=False, k=8, C=20
) -> tuple[NDArray, NDArray] | NDArray:
    """
    k: controls how many transmon eigenstates are included per qubit
    C: charge truncation
    units of Ec1
    Returns:
        eigenvalues and eigenvectors in bare basis
    """

    nstates = np.arange(-C, C + 1, step=1)
    ndiag = np.square(nstates)
    vals1, vecs1 = spalg.eigh_tridiagonal(ndiag * 4 * 1, -np.ones(2 * C) * Ej1 / 2)
    vals2, vecs2 = spalg.eigh_tridiagonal(ndiag * 4 * Ec2, -np.ones(2 * C) * Ej2 / 2)
    vals3, vecs3 = spalg.eigh_tridiagonal(ndiag * 4 * Ec3, -np.ones(2 * C) * Ej3 / 2)

    N = 2 * k + 1  # transmon trunc
    D1 = cp.diag(vals1[:N])  # vals are sorted in ascending order
    D2 = cp.diag(vals2[:N])
    D3 = cp.diag(vals3[:N])

    ndiag = np.diag(nstates)
    n1 = vecs1.T @ ndiag @ vecs1  # change into transmon bare basis
    n2 = vecs2.T @ ndiag @ vecs2
    n3 = vecs3.T @ ndiag @ vecs3

    n1 = cp.asarray(n1[:N, :N])  # truncate
    n2 = cp.asarray(n2[:N, :N])
    n3 = cp.asarray(n3[:N, :N])

    ID = cp.eye(N, N)

    Hint12 = 4 * Eint12 * kron(n1, n2, ID)
    Hint23 = 4 * Eint23 * kron(ID, n2, n3)
    Hint13 = 4 * Eint13 * kron(n1, ID, n3)

    H = kron(D1, ID, ID) + kron(ID, D2, ID) + kron(ID, ID, D3) + Hint12 + Hint23 + Hint13

    if only_energy:
        vals = cp.linalg.eigvalsh(H)
        return cp.asnumpy(vals)
    vals, vecs = cp.linalg.eigh(H)

    # return eigenvalues and vectors, order will be "kronecker counting"
    return cp.asnumpy(vals), cp.asnumpy(vecs)
