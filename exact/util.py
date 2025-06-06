import scipy.special as spec
import numpy as np
from matplotlib import pyplot as plt
import cupy as cp
import cupyx.scipy.sparse
import scipy.linalg as spalg


def getsparsegpumem(mat):
    if cupyx.scipy.sparse.isspmatrix_coo(mat):
        return mat.data.nbytes + mat.row.nbytes + mat.col.nbytes
    elif cupyx.scipy.sparse.isspmatrix_dia(mat):
        return mat.data.nbytes + mat.offsets.nbytes
    else:
        return mat.data.nbytes + mat.indices.nbytes + mat.indptr.nbytes


def kron_sparse(*mats, format: str = "csr"):
    """For CuPy sparse matrices"""
    total = mats[0]
    for i in range(1, len(mats)):
        total = cupyx.scipy.sparse.kron(total, mats[i], format=format)
        # print("kron", i, getsparsegpumem(total))
        cp.get_default_memory_pool().free_all_blocks()
    return total


def kron_cp(*mats):
    """For CuPy  matrices"""
    total = mats[0]
    for i in range(1, len(mats)):
        total = cp.kron(total, mats[i])
    return total


def kron(*mats):
    """For numpy matrices"""
    total = mats[0]
    for i in range(1, len(mats)):
        total = np.kron(total, mats[i])
    return total


def exact_energy_num(Ec, Ej, C=30):
    # m=0,1,2,3,... should give the single transmon energies in acending order
    nstates = np.arange(-C, C + 1, step=1)
    ndiag = np.square(nstates)
    vals, _ = spalg.eigh_tridiagonal(ndiag * 4 * Ec, -np.ones(2 * C) * Ej / 2)
    return vals - vals[0]


def exact_energy(m, Ec, Ej):
    # m=0,1,2,3,... should give the single transmon energies in acending order
    if m % 2 == 0:
        Eexact = Ec * spec.mathieu_a(m, -Ej / (2 * Ec))
    else:
        Eexact = Ec * spec.mathieu_b(m + 1, -Ej / (2 * Ec))
    return Eexact


def exact_energy_a(m: int, Ec: int, Ej: np.ndarray):
    Eexact = Ec * spec.mathieu_a(2 * m, -Ej / (2 * Ec))
    return Eexact


def exact_energy_b(m: int, Ec: int, Ej: np.ndarray):
    Eexact = Ec * spec.mathieu_b(2 * m, -Ej / (2 * Ec))
    return Eexact


def gconstant(Ec1, Ej1: np.ndarray, Ec2, Ej2, Eint):
    # if we feed in one of the Ec's as the unit, this g gets that unit
    g = 4 * Eint * (Ej1 * Ej2 / (32**2 * Ec1 * Ec2)) ** (1 / 4)
    return g


def Eint_to_g(Ej1, Ej2, Eint):
    """Beware of the absolute. Introduce your own sign"""
    C = 30
    nstates = np.arange(-C, C + 1, step=1)
    ndiag = np.square(nstates)
    _, vecs1 = spalg.eigh_tridiagonal(ndiag * 4 * 1, -np.ones(2 * C) * Ej1 / 2)
    _, vecs2 = spalg.eigh_tridiagonal(ndiag * 4 * 1, -np.ones(2 * C) * Ej2 / 2)

    ndiag = np.diag(nstates)
    n1 = vecs1.T @ ndiag @ vecs1  # change into transmon bare basis
    n2 = vecs2.T @ ndiag @ vecs2

    g12 = 4 * Eint * np.abs(n1[1, 0] * n2[0, 1])
    return g12


def omega_alphas(Ec, Ej: np.ndarray, fancy: bool):
    """Given exact model, translate params to omega, alpha. Ec is meant to be 1, the unit"""
    if fancy:
        grounds = exact_energy_a(m=0, Ec=Ec, Ej=Ej)
        omegas = exact_energy_b(m=1, Ec=Ec, Ej=Ej) - grounds
        alphas = exact_energy_a(m=1, Ec=Ec, Ej=Ej) - grounds - 2 * omegas
    else:
        omegas = np.sqrt(8 * Ec * Ej) - Ec
        alphas = np.ones(Ej.shape) * (-Ec)
    return omegas, alphas  # given that Ec is unit, these also get the unit Ec


def to_omega_grid(Ej1: np.ndarray, Ej2: np.ndarray, Ej3: float):
    Ej2grid, Ej1grid = np.meshgrid(Ej2, Ej1)
    o3, _ = omega_alphas(1, Ej3, True)
    o1, _ = omega_alphas(1, Ej1grid, True)
    o2, _ = omega_alphas(1, Ej2grid, True)
    o2primgrid = o2 - (o3 + o1) / 2
    detunegrid = o1 - o3
    return o2primgrid, detunegrid


def index_map2T(N):
    """
    map for two qubits.
    N: number of states per qubit
    index this map as map[i][j] to get hamiltonian index for state |ij>
    """
    idx_map = [[j + i * N for j in range(N)] for i in range(N)]
    return idx_map


def index_map3T(N):
    """
    map for 3 qubits.
    """
    idx_map = [[[j + i * N + k * N**2 for j in range(N)] for i in range(N)] for k in range(N)]
    return idx_map


if __name__ == "__main__":
    ma = [spec.mathieu_a(m, -50 / (2 * 1)) for m in range(20)]
    mb = [spec.mathieu_b(m, -50 / (2 * 1)) for m in range(20)]
    print(mb)
    plt.plot(ma, marker=".", lw=0)
    plt.plot(mb, marker=".", lw=0)
    plt.figure()
    Es = [exact_energy(m, 1, 50) for m in range(10)]
    plt.plot(Es, lw=0, marker=".")
    plt.show()
    pass
