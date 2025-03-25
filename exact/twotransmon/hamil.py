# Here I will try to expand the two transmon Hamiltonian in the charge basis
import numpy as np
import cupy as cp
from matplotlib import pyplot as plt
import cupyx
import scipy.linalg as spalg


# archived
def calc_eig(Ej, Eint=1, k=20):
    #  get eigenvalues
    # Ej same for both
    # Eint interaction energy

    N = 2 * k + 1  # size of matrix of one product transmon space
    nstates = np.arange(-k, k + 1, step=1)  # (-k .. -1, 0, 1 .. k) is our order of basis

    Ec = 1  # fixed. set to one, same for both transmons
    ng = 0  # ignore for now. Will have to add to diagonal

    H1 = (
        np.diag(-np.ones(N - 1) * Ej / 2, 1)
        + np.diag(-np.ones(N - 1) * Ej / 2, -1)
        + np.diag(np.square(nstates) * 4 * Ec)
    )

    H2 = H1.copy()  # same

    Hint = 4 * Eint * np.kron(np.diag(nstates), np.diag(nstates))
    I = np.eye(N, N)
    # Total NxN
    H = np.kron(H1, I) + np.kron(I, H2) + Hint

    H = cp.asarray(H)

    vals = cp.linalg.eigvalsh(H)
    vals = cp.asnumpy(vals)
    sorted = np.sort(vals)

    return sorted


# this is the good one now
def eig_clever(Ej1, k, Ej2, Eint, only_energy=False, ng1=0):
    # ng2=0
    # k controls how many transmon eigenstates are included per qubit
    # delta: detuning. Ec1=Ec2=1, units of Ec
    # returns eigenvalues and eigenvectors in bare basis

    C = 400  # charge trunc, I have done zero investigation to convergence wrt this param
    nstates = np.arange(-C, C + 1, step=1)

    vals1, vecs1 = spalg.eigh_tridiagonal(np.square(nstates - ng1) * 4 * 1, -np.ones(2 * C) * Ej1 / 2)
    vals2, vecs2 = spalg.eigh_tridiagonal(np.square(nstates) * 4 * 1, -np.ones(2 * C) * Ej2 / 2)

    i1 = np.sum(np.imag(vecs1))
    i2 = np.sum(np.imag(vecs1))
    if (i1 != 0) or (i2 != 0):
        raise Exception("Imaginary part of eigenvector!")

    N = 2 * k + 1  # transmon trunc
    D1 = np.diag(vals1[:N])  # vals are sorted in ascending order
    D2 = np.diag(vals2[:N])

    n1 = np.diag(nstates - ng1)
    n2 = np.diag(nstates)
    n1 = vecs1.T @ n1 @ vecs1  # change into transmon bare basis
    n2 = vecs2.T @ n2 @ vecs2
    n1 = n1[:N, :N]  # truncate
    n2 = n2[:N, :N]
    Hint = 4 * Eint * np.kron(n1, n2)

    I = np.eye(N, N)

    H = np.kron(D1, I) + np.kron(I, D2) + Hint

    H = cp.asarray(H)

    if only_energy:
        vals = cp.linalg.eigvalsh(H)
        return cp.asnumpy(vals)

    vals, vecs = cp.linalg.eigh(H)

    # index this map as map[i][j] to get H index for state |ij>
    idx_map = [[j + i * N for j in range(N)] for i in range(N)]

    # return eigenvalues and vectors, order will be "kronecker counting"
    return cp.asnumpy(vals), cp.asnumpy(vecs), idx_map
