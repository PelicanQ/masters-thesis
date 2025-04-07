# Here I will try to expand the two transmon Hamiltonian in the charge basis
import numpy as np
import cupy as cp
from matplotlib import pyplot as plt
import scipy.linalg as spalg

def kron(*mats):
    total = mats[0]
    for i in range(1, len(mats)):
        total = np.kron(total, mats[i])
    return total

# this is the good one now
def eig_clever(Ec2, Ec3, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, only_energy=False, k=12):
    """
    k controls how many transmon eigenstates are included per qubit
    units of Ec1
    Returns:
        eigenvalues and eigenvectors in bare basis
    """

    C = 200  # charge trunc, I have done zero investigation to convergence wrt this param
    nstates = np.arange(-C, C + 1, step=1)

    vals1, vecs1 = spalg.eigh_tridiagonal(np.square(nstates) * 4 * 1, -np.ones(2 * C) * Ej1 / 2)
    vals2, vecs2 = spalg.eigh_tridiagonal(np.square(nstates) * 4 * Ec2, -np.ones(2 * C) * Ej2 / 2)
    vals3, vecs3 = spalg.eigh_tridiagonal(np.square(nstates) * 4 * Ec3, -np.ones(2 * C) * Ej3 / 2)


    N = 2 * k + 1  # transmon trunc
    D1 = np.diag(vals1[:N])  # vals are sorted in ascending order
    D2 = np.diag(vals2[:N])
    D3 = np.diag(vals3[:N])

    n1 = np.diag(nstates)
    n2 = np.diag(nstates)
    n3 = np.diag(nstates)

    n1 = vecs1.T @ n1 @ vecs1  # change into transmon bare basis
    n2 = vecs2.T @ n2 @ vecs2
    n3 = vecs3.T @ n3 @ vecs3

    n1 = n1[:N, :N]  # truncate
    n2 = n2[:N, :N]
    n3 = n3[:N, :N]

    ID = np.eye(N, N)

    Hint12 = 4 * Eint12 * kron(n1, n2, ID)
    Hint23 = 4 * Eint23 * kron(ID, n2, n3)
    Hint13 = 4 * Eint13 * kron(n1, ID, n3)

    H = kron(D1, ID, ID) + kron(ID, D2, ID) + kron(ID,ID,D3) + Hint12 + Hint23 + Hint13
    
    H = cp.asarray(H)

    if only_energy:
        vals = cp.linalg.eigvalsh(H)
        return cp.asnumpy(vals)
    vals, vecs = cp.linalg.eigh(H)

    # return eigenvalues and vectors, order will be "kronecker counting"
    return cp.asnumpy(vals), cp.asnumpy(vecs)
