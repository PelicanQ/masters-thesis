# Here I will try to expand the two transmon Hamiltonian in the charge basis
import numpy as np
import cupy as cp
from matplotlib import pyplot as plt
import scipy.linalg as spalg
from numpy.typing import NDArray
import itertools
import time
from exact.util import kron_sparse, kron, kron_cp
from cupyx.scipy import sparse


def excitation_trunc_indices_keep(statesperbit: int, max_excitation: int):
    """Return Hamiltonian indices of states with acceptable excitation"""
    indices = []
    N = statesperbit
    for i, j, k, l in itertools.product(range(N), repeat=4):
        if i + j + k + l <= max_excitation:
            indices.append(i + j * N + k * N**2 + l * N**3)
    return indices


# def sorted_vals(vals1, vals2, vals3):
#     """Only for eig visualize"""
#     levels = []
#     for comb in itertools.product(range(5), repeat=3):
#         sortvals1 = np.sort(vals1)
#         sortvals2 = np.sort(vals2)
#         sortvals3 = np.sort(vals3)
#         sortvals1 = sortvals1 - sortvals1[0]
#         sortvals2 = sortvals2 - sortvals2[0]
#         sortvals3 = sortvals3 - sortvals3[0]
#         if sum(comb) < 4:
#             levels.append((comb, sortvals1[comb[0]] + sortvals2[comb[1]] + sortvals3[comb[2]]))
#     levels = sorted(levels, key=lambda item: item[1])
#     return levels


# def eig_clever_vis(
#     Ec2, Ec3, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, only_energy=False, k=8, C=20, M=30
# ) -> tuple[NDArray, NDArray] | NDArray:
#     """
#     k: controls how many transmon eigenstates are included per qubit
#     C: charge truncation
#     units of Ec1
#     Returns:
#         eigenvalues and eigenvectors in bare basis
#     """
#     nstates = np.arange(-C, C + 1, step=1)
#     ndiag = np.square(nstates)
#     vals1, vecs1 = spalg.eigh_tridiagonal(ndiag * 4 * 1, -np.ones(2 * C) * Ej1 / 2)
#     vals2, vecs2 = spalg.eigh_tridiagonal(ndiag * 4 * Ec2, -np.ones(2 * C) * Ej2 / 2)
#     vals3, vecs3 = spalg.eigh_tridiagonal(ndiag * 4 * Ec3, -np.ones(2 * C) * Ej3 / 2)
#     sorted_bare_levels = sorted_vals(vals1, vals2, vals3)
#     N = 2 * k + 1  # transmon trunc
#     D1 = cp.diag(vals1[:N])  # vals are sorted in ascending order
#     D2 = cp.diag(vals2[:N])
#     D3 = cp.diag(vals3[:N])

#     ndiag = np.diag(nstates)
#     n1 = vecs1.T @ ndiag @ vecs1  # change into transmon bare basis
#     n2 = vecs2.T @ ndiag @ vecs2
#     n3 = vecs3.T @ ndiag @ vecs3

#     n1 = cp.asarray(n1[:N, :N])  # truncate to NxN
#     n2 = cp.asarray(n2[:N, :N])
#     n3 = cp.asarray(n3[:N, :N])

#     ID = cp.eye(N, N)

#     Hint12 = 4 * Eint12 * kron(n1, n2, ID)
#     Hint23 = 4 * Eint23 * kron(ID, n2, n3)
#     Hint13 = 4 * Eint13 * kron(n1, ID, n3)

#     H = kron(D1, ID, ID) + kron(ID, D2, ID) + kron(ID, ID, D3) + Hint12 + Hint23 + Hint13

#     # now let's remove states with too large excitation sum
#     # gather indices and delete at once
#     indices = excitation_trunc_indices(N, M)
#     H = cp.delete(H, indices, axis=0)
#     H = cp.delete(H, indices, axis=1)
#     if only_energy:
#         vals = cp.linalg.eigvalsh(H)
#         return cp.asnumpy(vals), sorted_bare_levels
#     vals, vecs = cp.linalg.eigh(H)

#     # Note that with excitation trunc we get have to count differently
#     return cp.asnumpy(vals), cp.asnumpy(vecs)


caches_idx_maps: dict[(int, int), dict[tuple, int]] = {}  # global variable not the most elegant


def make_excitation_idx_map(statesperbit: int, max_excitation: int):
    idx_dict = {}
    i = 0
    # the order we use is the one after filtering itertools.product output
    for comb in itertools.product(range(statesperbit), repeat=4):
        if sum(comb) <= max_excitation:
            idx_dict[comb] = i
            i += 1
    return idx_dict


def get_excitation_idx_map(statesperbit: int, max_excitation: int):
    # index this map with 3-tuples to get the hamiltonian index of that state
    if (statesperbit, max_excitation) not in caches_idx_maps:
        caches_idx_maps[(statesperbit, max_excitation)] = make_excitation_idx_map(statesperbit, max_excitation)
    return caches_idx_maps[(statesperbit, max_excitation)]


def eig(Ej1, Ej2, Ej3, Ej4, Eint12, Eint23, Eint34, Eint14, only_energy=False, N=15, M=20):
    """
    k: controls how many transmon eigenstates are included per qubit
    All Ec are equal to 1
    units of Ec1
    Returns:
        eigenvalues and eigenvectors in bare basis
    """
    C = 20
    nstates = np.arange(-C, C + 1, step=1)
    ndiagsqr = np.square(nstates)
    vals1, vecs1 = spalg.eigh_tridiagonal(ndiagsqr * 4 * 1, -np.ones(2 * C) * Ej1 / 2)
    vals2, vecs2 = spalg.eigh_tridiagonal(ndiagsqr * 4 * 1, -np.ones(2 * C) * Ej2 / 2)
    vals3, vecs3 = spalg.eigh_tridiagonal(ndiagsqr * 4 * 1, -np.ones(2 * C) * Ej3 / 2)
    vals4, vecs4 = spalg.eigh_tridiagonal(ndiagsqr * 4 * 1, -np.ones(2 * C) * Ej4 / 2)

    # cupy sparse
    D1 = sparse.diags(vals1[:N], format="csr")
    D2 = sparse.diags(vals2[:N], format="csr")
    D3 = sparse.diags(vals3[:N], format="csr")
    D4 = sparse.diags(vals4[:N], format="csr")

    ndiag = np.diag(nstates)
    n1 = vecs1.T @ ndiag @ vecs1  # change into transmon bare basis
    n2 = vecs2.T @ ndiag @ vecs2
    n3 = vecs3.T @ ndiag @ vecs3
    n4 = vecs4.T @ ndiag @ vecs4

    n1 = cp.asarray(n1[:N, :N])  # truncate to NxN
    n2 = cp.asarray(n2[:N, :N])
    n3 = cp.asarray(n3[:N, :N])
    n4 = cp.asarray(n4[:N, :N])

    n1 = sparse.csr_matrix(n1)
    n2 = sparse.csr_matrix(n2)
    n3 = sparse.csr_matrix(n3)
    n4 = sparse.csr_matrix(n4)

    ID = sparse.eye(N, N)
    ID2 = sparse.kron(ID, ID, format="csr")  # kronecker products can take time so this optimizes a bit
    ID3 = sparse.kron(ID2, ID, format="csr")  # kronecker products can take time so this optimizes a bit
    Hint12 = 4 * Eint12 * kron_sparse(n1, n2, ID2)
    Hint23 = 4 * Eint23 * kron_sparse(ID, n2, n3, ID)
    Hint34 = 4 * Eint34 * kron_sparse(ID2, n3, n4)
    Hint14 = 4 * Eint14 * kron_sparse(n1, ID2, n4)

    Hint = Hint12 + Hint23 + Hint34 + Hint14
    D = kron_sparse(D1, ID3) + kron_sparse(ID, D2, ID2) + kron_sparse(ID2, D3, ID) + kron_sparse(ID3, D4)
    H = D + Hint
    keep_idx = excitation_trunc_indices_keep(N, M)

    H = H[:, keep_idx][keep_idx, :]

    # convery truncated cpu matrix to gpu matrix
    # Idea is that only after truncation is matrix small enough to store on GPU memory
    print(H.shape)
    H = H.toarray()
    print("start eig")
    if only_energy:
        vals = cp.linalg.eigvalsh(H)
        return cp.asnumpy(vals)
    vals, vecs = cp.linalg.eigh(H)

    # Note that with excitation trunc we get have to count differently
    return cp.asnumpy(vals), cp.asnumpy(vecs), get_excitation_idx_map(N, M)


if __name__ == "__main__":
    # A = cp.random.randint(0, 20, size=(4, 4))
    # print(A)
    # m = np.array([0, 2])
    # print(A[:, m][m, :])
    # indices = excitation_trunc_indices(3, 3)
    # mask = list(map(lambda n: n not in indices, range(3**4)))  # boolean list of which hamiltonian index to keep
    # print(mask)
    eig(50, 55, 60, 65, 0.1, 0.1, 0.1, 0.1)
