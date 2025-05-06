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


def excitation_trunc_indices_keep(statesperbit: int, max_excitation: int):
    """Return Hamiltonian indices of states with acceptable excitation"""
    indices = []
    N = statesperbit
    for i, j, k, l in itertools.product(range(N), repeat=4):
        if i + j + k + l <= max_excitation:
            indices.append(i + j * N + k * N**2 + l * N**3)
    return indices


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
    # index this map with tuples to get the hamiltonian index of that state
    if (statesperbit, max_excitation) not in caches_idx_maps:
        caches_idx_maps[(statesperbit, max_excitation)] = make_excitation_idx_map(statesperbit, max_excitation)
    return caches_idx_maps[(statesperbit, max_excitation)]


def eig(Ej1, Ej2, Ej3, Ej4, E12, E23, E13, E34, only_energy=False, N=11, M=14, C=30):
    """
    When M and N are small enough so sparse is not needed during matrix construction
    k: controls how many transmon eigenstates are included per qubit
    All Ec are equal to 1
    units of Ec1
    Returns:
        eigenvalues and eigenvectors in bare basis
    """
    t1 = time.perf_counter()

    nstates = np.arange(-C, C + 1, step=1)
    ndiagsqr = np.square(nstates)
    vals1, vecs1 = spalg.eigh_tridiagonal(ndiagsqr * 4 * 1, -np.ones(2 * C) * Ej1 / 2)
    vals2, vecs2 = spalg.eigh_tridiagonal(ndiagsqr * 4 * 1, -np.ones(2 * C) * Ej2 / 2)
    vals3, vecs3 = spalg.eigh_tridiagonal(ndiagsqr * 4 * 1, -np.ones(2 * C) * Ej3 / 2)
    vals4, vecs4 = spalg.eigh_tridiagonal(ndiagsqr * 4 * 1, -np.ones(2 * C) * Ej4 / 2)

    # cupy sparse
    D1 = cp.diag(vals1[:N])
    D2 = cp.diag(vals2[:N])
    D3 = cp.diag(vals3[:N])
    D4 = cp.diag(vals4[:N])

    ndiag = np.diag(nstates)
    n1 = vecs1.T @ ndiag @ vecs1  # change into transmon bare basis
    n2 = vecs2.T @ ndiag @ vecs2
    n3 = vecs3.T @ ndiag @ vecs3
    n4 = vecs4.T @ ndiag @ vecs4

    n1 = cp.asarray(n1[:N, :N])  # truncate to NxN
    n2 = cp.asarray(n2[:N, :N])
    n3 = cp.asarray(n3[:N, :N])
    n4 = cp.asarray(n4[:N, :N])

    ID = cp.eye(N, N)
    ID2 = cp.eye(N**2, N**2)
    Hint1 = 4 * E12 * kron_cp(n1, n2, ID)
    Hint1 += 4 * E23 * kron_cp(ID, n2, n3)
    Hint1 += 4 * E13 * kron_cp(n1, ID, n3)
    Hint1 = kron_cp(Hint1, ID)

    keep_idx = excitation_trunc_indices_keep(N, M)

    Hint = Hint1 + 4 * E34 * kron_cp(ID2, n3, n4)

    D = kron_cp(kron_cp(D1, ID) + kron_cp(ID, D2), ID2)
    D += kron_cp(ID2, kron_cp(D3, ID) + kron_cp(ID, D4))

    H = D + Hint
    H = H[:, keep_idx][keep_idx, :]

    print(H.shape)
    t2 = time.perf_counter()

    if only_energy:
        vals = cp.linalg.eigvalsh(H)
        return cp.asnumpy(vals)
    vals, vecs = cp.linalg.eigh(H)
    t3 = time.perf_counter()
    print(t2 - t1, t3 - t2)

    # Note that with excitation trunc we get have to count differently
    return cp.asnumpy(vals), cp.asnumpy(vecs), get_excitation_idx_map(N, M)


def eig_sparse(Ej1, Ej2, Ej3, Ej4, E12, E23, E13, E34, only_energy=False, N=11, M=14, C=30):
    """
    k: controls how many transmon eigenstates are included per qubit
    All Ec are equal to 1
    units of Ec1
    Returns:
        eigenvalues and eigenvectors in bare basis
    """
    t1 = time.perf_counter()

    nstates = np.arange(-C, C + 1, step=1)
    ndiagsqr = np.square(nstates)
    vals1, vecs1 = spalg.eigh_tridiagonal(ndiagsqr * 4 * 1, -np.ones(2 * C) * Ej1 / 2)
    vals2, vecs2 = spalg.eigh_tridiagonal(ndiagsqr * 4 * 1, -np.ones(2 * C) * Ej2 / 2)
    vals3, vecs3 = spalg.eigh_tridiagonal(ndiagsqr * 4 * 1, -np.ones(2 * C) * Ej3 / 2)
    vals4, vecs4 = spalg.eigh_tridiagonal(ndiagsqr * 4 * 1, -np.ones(2 * C) * Ej4 / 2)

    # cupy sparse
    D1 = sparse.diags(vals1[:N], format="dia")
    D2 = sparse.diags(vals2[:N], format="dia")
    D3 = sparse.diags(vals3[:N], format="dia")
    D4 = sparse.diags(vals4[:N], format="dia")

    ndiag = np.diag(nstates)
    n1 = vecs1.T @ ndiag @ vecs1  # change into transmon bare basis
    n2 = vecs2.T @ ndiag @ vecs2
    n3 = vecs3.T @ ndiag @ vecs3
    n4 = vecs4.T @ ndiag @ vecs4

    n1 = cp.asarray(n1[:N, :N])  # truncate to NxN
    n2 = cp.asarray(n2[:N, :N])
    n3 = cp.asarray(n3[:N, :N])
    n4 = cp.asarray(n4[:N, :N])

    n1 = sparse.coo_matrix(n1)
    n2 = sparse.coo_matrix(n2)
    n3 = sparse.coo_matrix(n3)
    n4 = sparse.coo_matrix(n4)

    ID = sparse.eye(N, N, format="dia")
    ID2 = sparse.eye(N**2, N**2, format="dia")
    ID3 = sparse.eye(N**3, N**3, format="dia")
    format = "coo"
    Hint1 = 4 * E12 * kron_sparse(n1, n2, ID, format=format)
    Hint1 += 4 * E23 * kron_sparse(ID, n2, n3, format=format)
    Hint1 += 4 * E13 * kron_sparse(n1, ID, n3, format=format)

    Hint2 = 4 * E34 * kron_sparse(n3, n4, format=format)

    cp.get_default_memory_pool().free_all_blocks()

    keep_idx = excitation_trunc_indices_keep(N, M)

    # convert CuPy sparse into scipy sparse
    Hint1 = kron_sparse(Hint1, ID, format="coo")

    # truncate
    Hint1_cpu = sparse.coo_matrix.get(Hint1).asformat("csr")[:, keep_idx][keep_idx, :]
    # clear up GPU memory
    del Hint1
    cp.get_default_memory_pool().free_all_blocks()

    Hint2 = kron_sparse(ID2, Hint2, format="coo")
    Hint2_cpu = sparse.coo_matrix.get(Hint2).asformat("csr")[:, keep_idx][keep_idx, :]

    del Hint2
    cp.get_default_memory_pool().free_all_blocks()

    Hint_cpu = Hint1_cpu + Hint2_cpu

    D = kron_sparse(D1, ID3, format="csr")
    D += kron_sparse(ID, D2, ID2, format="csr")
    D += kron_sparse(ID2, D3, ID, format="csr")
    D += kron_sparse(ID3, D4, format="csr")
    D_cpu = sparse.csr_matrix.get(D)[:, keep_idx][keep_idx, :]

    del D
    cp.get_default_memory_pool().free_all_blocks()

    H_cpu = D_cpu + Hint_cpu

    # now that Hamiltonian is small enough to keep on GPU we can bring it into CuPy
    H = sparse.csr_matrix(H_cpu).toarray()
    print(H.shape)
    t2 = time.perf_counter()

    cp.get_default_memory_pool().free_all_blocks()

    if only_energy:
        vals = cp.linalg.eigvalsh(H)
        return cp.asnumpy(vals)
    vals, vecs = cp.linalg.eigh(H)
    t3 = time.perf_counter()
    print(t2 - t1, t3 - t2)
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
    NN = np.arange(8, 15)
    MM = np.arange(8, 20)
    eig(50, 55, 60, 65, 0.1, 0.1, 0.01, 0.1)
    eig(50, 55, 60, 65, 0.1, 0.1, 0.01, 0.1)
    eig(50, 55, 60, 65, 0.1, 0.1, 0.01, 0.1)
    eig(50, 55, 60, 65, 0.1, 0.1, 0.01, 0.1)
