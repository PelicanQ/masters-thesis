# We will find the lowest energy levels of the DC-SQUID by numerically solving the Hamiltonian given different values of parameter n_g

import numpy as np
import cupy as cp
from scipy import linalg
from matplotlib import pyplot as plt

# matrix for DC-SQUID in basis of number operator eigenbasis

def Hgen(ng, ratio, k=60):
    nstates = np.arange(-k, k + 1, step=1)  # (-k .. -1, 0, 1 .. k) is our order of basis
    Ec = 1
    # this matrix is normalized to Ec (Ec must equal 1)
    Ej = Ec * ratio
    return (
        np.diag(-np.ones(2 * k) * Ej / 2, 1)
        + np.diag(-np.ones(2 * k) * Ej / 2, -1)
        + np.diag(np.square(nstates - ng) * 4 * Ec)
    )


def calc_eigs(ratio, ng, k=60):
    # return only eigenvalues

    H = Hgen(ng, ratio, k)
    eig = linalg.eigvalsh_tridiagonal(H.diagonal(), H.diagonal(1))
    sorted = np.sort(eig)

    return sorted

if __name__ == "__main__":
    Ejs = np.arange(30,90,1)
    alphas = []
    for Ej in Ejs:
        vals = calc_eigs(Ej, 0, 60)
        vals = vals - vals[0]
        alphas.append((vals[2]-2*vals[1]))
    
    plt.plot(Ejs, alphas)
    plt.xlabel("Ej")
    plt.ylim([-2,0])
    plt.show()


def calc_cond(ng, Ej, k):
    H = Hgen(ng, Ej, k)
    return np.linalg.cond(H)


# eigs
N = 101  # resolution of ng scan. Has to be odd to include ng=0
ngs = np.linspace(-2, 2, N)  # list of ng values


def ng_sweep(ratio, k=60):
    # return eigenvalues vs ng
    evals = np.empty(shape=(2 * k + 1, N))  # column = ng value, row = n:th eig. 0th row should be smallest eigenvalue

    for i, ng in enumerate(ngs):
        H = Hgen(ng, ratio, k)
        H = cp.asarray(H)
        vals = cp.linalg.eigvalsh(H)
        vals = cp.asnumpy(vals)
        sorted = np.sort(vals)
        # If I want states, use argsort
        evals[:, i] = sorted

    return evals
