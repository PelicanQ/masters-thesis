# Here I will try to expand the two transmon Hamiltonian in the charge basis
import numpy as np
import cupy as cp
from matplotlib import pyplot as plt
import scipy.linalg as spalg
from numpy.typing import NDArray
import itertools
import time


def kron(*mats):
    total = mats[0]
    for i in range(1, len(mats)):
        total = cp.kron(total, mats[i])
    return total


def excitation_trunc_indices(statesperbit: int, max_excitation: int):
    """Return Hamiltonian indices of states with too high excitation"""
    indices = []
    N = statesperbit
    for i, j, k in itertools.product(range(N), repeat=3):
        if i + j + k > max_excitation:
            indices.append(i + j * N + k * N**2)
    return indices


def sorted_vals(vals1, vals2, vals3):
    levels = []
    for comb in itertools.product(range(5), repeat=3):
        sortvals1 = np.sort(vals1)
        sortvals2 = np.sort(vals2)
        sortvals3 = np.sort(vals3)
        sortvals1 = sortvals1 - sortvals1[0]
        sortvals2 = sortvals2 - sortvals2[0]
        sortvals3 = sortvals3 - sortvals3[0]
        if sum(comb) < 4:
            levels.append((comb, sortvals1[comb[0]] + sortvals2[comb[1]] + sortvals3[comb[2]]))
    levels = sorted(levels, key=lambda item: item[1])
    return levels


def eig_clever_vis(
    Ec2, Ec3, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, only_energy=False, k=8, C=20, M=30
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
    sorted_bare_levels = sorted_vals(vals1, vals2, vals3)
    N = 2 * k + 1  # transmon trunc
    D1 = cp.diag(vals1[:N])  # vals are sorted in ascending order
    D2 = cp.diag(vals2[:N])
    D3 = cp.diag(vals3[:N])

    ndiag = np.diag(nstates)
    n1 = vecs1.T @ ndiag @ vecs1  # change into transmon bare basis
    n2 = vecs2.T @ ndiag @ vecs2
    n3 = vecs3.T @ ndiag @ vecs3

    n1 = cp.asarray(n1[:N, :N])  # truncate to NxN
    n2 = cp.asarray(n2[:N, :N])
    n3 = cp.asarray(n3[:N, :N])

    ID = cp.eye(N, N)

    Hint12 = 4 * Eint12 * kron(n1, n2, ID)
    Hint23 = 4 * Eint23 * kron(ID, n2, n3)
    Hint13 = 4 * Eint13 * kron(n1, ID, n3)

    H = kron(D1, ID, ID) + kron(ID, D2, ID) + kron(ID, ID, D3) + Hint12 + Hint23 + Hint13

    # now let's remove states with too large excitation sum
    # gather indices and delete at once
    indices = excitation_trunc_indices(N, M)
    H = cp.delete(H, indices, axis=0)
    H = cp.delete(H, indices, axis=1)
    if only_energy:
        vals = cp.linalg.eigvalsh(H)
        return cp.asnumpy(vals), sorted_bare_levels
    vals, vecs = cp.linalg.eigh(H)

    # Note that with excitation trunc we get have to count differently
    return cp.asnumpy(vals), cp.asnumpy(vecs)


caches_idx_maps: dict[(int, int), dict[tuple, int]] = {}  # global variable not the most elegant


def make_excitation_idx_map(statesperbit: int, max_excitation: int):
    idx_dict = {}
    i = 0
    # the order we use is the one after filtering itertools.product output
    for comb in itertools.product(range(statesperbit), repeat=3):
        if sum(comb) <= max_excitation:
            idx_dict[comb] = i
            i += 1
    return idx_dict


def get_excitation_idx_map(statesperbit: int, max_excitation: int):
    # index this map with 3-tuples to get the hamiltonian index of that state
    if (statesperbit, max_excitation) not in caches_idx_maps:
        caches_idx_maps[(statesperbit, max_excitation)] = make_excitation_idx_map(statesperbit, max_excitation)
    return caches_idx_maps[(statesperbit, max_excitation)]


def eig_excitation_trunc(
    Ec2, Ec3, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, only_energy=False, k=8, M=30
) -> tuple[NDArray, NDArray] | NDArray:
    """
    k: controls how many transmon eigenstates are included per qubit
    units of Ec1
    Returns:
        eigenvalues and eigenvectors in bare basis
    """
    C = 20
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

    n1 = cp.asarray(n1[:N, :N])  # truncate to NxN
    n2 = cp.asarray(n2[:N, :N])
    n3 = cp.asarray(n3[:N, :N])

    ID = cp.eye(N, N)

    Hint12 = 4 * Eint12 * kron(n1, n2, ID)
    Hint23 = 4 * Eint23 * kron(ID, n2, n3)
    Hint13 = 4 * Eint13 * kron(n1, ID, n3)
    ID2 = kron(ID, ID)  # kronecker products can take time so this optimizes a bit
    H = kron(D1, ID2) + kron(ID, D2, ID) + kron(ID2, D3) + Hint12 + Hint23 + Hint13

    # now let's remove states with too large excitation sum
    indices = excitation_trunc_indices(N, M)
    H = cp.delete(H, indices, axis=0)
    H = cp.delete(H, indices, axis=1)

    if only_energy:
        vals = cp.linalg.eigvalsh(H)
        return cp.asnumpy(vals), get_excitation_idx_map(N, M)
    vals, vecs = cp.linalg.eigh(H)

    # Note that with excitation trunc we get have to count differently
    return cp.asnumpy(vals), cp.asnumpy(vecs), get_excitation_idx_map(N, M)


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


if __name__ == "__main__":
    start = time.perf_counter()
    for _ in range(3):
        eig_clever(1, 1, 50, 55, 60, 0.2, 0.4, 0.6, k=10)
    end = time.perf_counter()
    print(f"eig_clever execution time: {end - start:.4f} seconds")

    start = time.perf_counter()
    for _ in range(3):
        eig_excitation_trunc(1, 1, 50, 55, 60, 0.2, 0.4, 0.6, k=10)
    end = time.perf_counter()
    print(f"eig_excitation_trunc execution time: {end - start:.4f} seconds")
