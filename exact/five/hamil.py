# Here I will try to expand the two transmon Hamiltonian in the charge basis
import numpy as np
import cupy as cp
from matplotlib import pyplot as plt
import scipy.linalg as spalg
import scipy
from numpy.typing import NDArray
import itertools
import time
from exact.util import kron_sparse, kron, kron_cp
from cupyx.scipy import sparse
from exact.util import getsparsegpumem


def excitation_trunc_indices_keep(statesperbit: int, max_excitation: int):
    """Return Hamiltonian indices of states with acceptable excitation"""
    indices = []
    N = statesperbit
    for i, j, k, l, m in itertools.product(range(N), repeat=5):
        if i + j + k + l + m <= max_excitation:
            indices.append(i + j * N + k * N**2 + l * N**3 + m * N**4)
    return indices


caches_idx_maps: dict[(int, int), dict[tuple, int]] = {}  # global variable not the most elegant

# TODO: CORRECT wrt order
# def make_excitation_idx_map(statesperbit: int, max_excitation: int):
#     idx_dict = {}
#     i = 0
#     # the order we use is the one after filtering itertools.product output
#     for comb in itertools.product(range(statesperbit), repeat=4):
#         if sum(comb) <= max_excitation:
#             idx_dict[comb] = i
#             i += 1
#     return idx_dict


def get_excitation_idx_map(statesperbit: int, max_excitation: int):
    # index this map with 3-tuples to get the hamiltonian index of that state
    if (statesperbit, max_excitation) not in caches_idx_maps:
        caches_idx_maps[(statesperbit, max_excitation)] = make_excitation_idx_map(statesperbit, max_excitation)
    return caches_idx_maps[(statesperbit, max_excitation)]


def eig(Ej1, Ej2, Ej3, Ej4, Ej5, E12, E23, E13, E34, E45, E35, only_energy=False, N=15, M=20):
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
    vals5, vecs5 = spalg.eigh_tridiagonal(ndiagsqr * 4 * 1, -np.ones(2 * C) * Ej5 / 2)
    print("prediag")
    # cupy sparse
    D1 = sparse.diags(vals1[:N], format="dia")
    D2 = sparse.diags(vals2[:N], format="dia")
    D3 = sparse.diags(vals3[:N], format="dia")
    D4 = sparse.diags(vals4[:N], format="dia")
    D5 = sparse.diags(vals5[:N], format="dia")
    print("D")

    ndiag = np.diag(nstates)
    n1 = vecs1.T @ ndiag @ vecs1  # change into transmon bare basis
    n2 = vecs2.T @ ndiag @ vecs2
    n3 = vecs3.T @ ndiag @ vecs3
    n4 = vecs4.T @ ndiag @ vecs4
    n5 = vecs5.T @ ndiag @ vecs5
    print("n5", n5.nbytes)

    n1 = cp.asarray(n1[:N, :N])  # truncate to NxN
    n2 = cp.asarray(n2[:N, :N])
    n3 = cp.asarray(n3[:N, :N])
    n4 = cp.asarray(n4[:N, :N])
    n5 = cp.asarray(n5[:N, :N])
    print("change")
    print("n5", n5.nbytes)

    n1 = sparse.coo_matrix(n1)
    n2 = sparse.coo_matrix(n2)
    n3 = sparse.coo_matrix(n3)
    n4 = sparse.coo_matrix(n4)
    n5 = sparse.coo_matrix(n5)
    print("n5", getsparsegpumem(n5))

    ID = sparse.eye(N, N, format="dia")
    ID2 = sparse.eye(N**2, N**2, format="dia")
    ID3 = sparse.eye(N**3, N**3, format="dia")
    ID4 = sparse.eye(N**4, N**4, format="dia")
    # ID2 = sparse.kron(ID, ID, format="dia")  # kronecker products can take time so this optimizes a bit
    # ID3 = sparse.kron(ID2, ID, format="dia")
    # ID4 = sparse.kron(ID3, ID, format="dia")
    print("ID4", getsparsegpumem(ID4))
    format = "coo"
    print("Start")
    Hint1 = 4 * E12 * kron_sparse(n1, n2, ID, format=format)
    print("First")
    Hint1 += 4 * E23 * kron_sparse(ID, n2, n3, format=format)
    print("second")
    Hint1 += 4 * E13 * kron_sparse(n1, ID, n3, format=format)
    print("third")

    Hint2 = 4 * E34 * kron_sparse(n3, n4, ID, format=format)
    Hint2 += 4 * E45 * kron_sparse(ID, n4, n5, format=format)
    Hint2 += 4 * E35 * kron_sparse(n4, ID, n5, format=format)
    print("Fourth")
    cp.get_default_memory_pool().free_all_blocks()
    # Hint1.g
    keep_idx = excitation_trunc_indices_keep(N, M)

    Hint1 = kron_sparse(Hint1, ID, ID, format="coo")
    Hint1_cpu = sparse.coo_matrix.get(Hint1).asformat("csr")[:, keep_idx][keep_idx, :]
    print("Hint1", getsparsegpumem(Hint1))

    del Hint1
    cp.get_default_memory_pool().free_all_blocks()

    Hint2 = kron_sparse(ID2, Hint2, format="coo")
    Hint2_cpu = sparse.coo_matrix.get(Hint2).asformat("csr")[:, keep_idx][keep_idx, :]

    del Hint2
    cp.get_default_memory_pool().free_all_blocks()
    print("Hint2")

    Hint_cpu = Hint1_cpu + Hint2_cpu
    print("Hint")

    D = kron_sparse(D1, ID4, format="csr")
    D += kron_sparse(ID, D2, ID3, format="csr")
    D += kron_sparse(ID2, D3, ID2, format="csr")
    D += kron_sparse(ID3, D4, ID, format="csr")
    D += kron_sparse(ID4, D5, format="csr")

    D_cpu = sparse.csr_matrix.get(D)[:, keep_idx][keep_idx, :]
    print("D ")

    del D
    cp.get_default_memory_pool().free_all_blocks()

    H_cpu = D_cpu + Hint_cpu
    print("Exc")

    # convery truncated cpu matrix to gpu matrix
    # Idea is that only after truncation is matrix small enough to store on GPU memory

    print(H_cpu.shape)
    H = sparse.coo_matrix(H_cpu).toarray()
    print(H.shape)
    cp.get_default_memory_pool().free_all_blocks()
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
    eig(50, 55, 60, 65, 40, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, N=13, M=15)
