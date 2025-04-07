import scipy.special as spec
import numpy as np
import scipy.linalg as spalg
from matplotlib import pyplot as plt

# these functions are a bit specific at the moment


def interaction_term(Ej1, Ej2):
    # get g from matrices assuming Ec1=Ec2=1
    C = 120  # charge trunc, I have done zero investigation to convergence wrt this param
    nstates = np.arange(-C, C + 1, step=1)

    _, vecs1 = spalg.eigh_tridiagonal(np.square(nstates) * 4 * 1, -np.ones(2 * C) * Ej1 / 2)
    _, vecs2 = spalg.eigh_tridiagonal(np.square(nstates) * 4 * 1, -np.ones(2 * C) * Ej2 / 2)

    n1 = np.diag(nstates)
    n2 = np.diag(nstates)
    # change into transmon bare basis
    n1 = vecs1.T @ n1 @ vecs1
    n2 = vecs2.T @ n2 @ vecs2

    trunc = 2  # transmon trunc
    n1 = n1[:trunc, :trunc]  # truncate
    n2 = n2[:trunc, :trunc]
    interact = np.kron(n1, n2)
    # return the interaction matrix between 00 01 10 11
    return interact


def Eint_to_g_Ej(Ej1s: np.ndarray, Ej2, Eint):
    gs = np.zeros_like(Ej1s)
    imap = index_map(2)
    for i in range(len(Ej1s)):
        Hint = interaction_term(Ej1s[i], Ej2)
        gs[i] = 4 * Eint * Hint[imap[0][1], imap[1][0]]
    # absolute because signs may flip. Keep in mind for larger systems when sign of g can matter
    return np.abs(gs)


def Eint_to_g_Eint(Ej1, Ej2, Eints: np.ndarray):
    Hint = interaction_term(Ej1, Ej2)
    imap = index_map(2)
    gs = 4 * Eints * Hint[imap[0][1], imap[1][0]]
    return np.abs(gs)


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


def omega_alphas(Ec, Ej: np.ndarray, fancy: bool):
    # Ec is meant to be 1, the unit
    if fancy:
        grounds = exact_energy_a(m=0, Ec=Ec, Ej=Ej)
        omegas = exact_energy_b(m=1, Ec=Ec, Ej=Ej) - grounds
        alphas = exact_energy_a(m=1, Ec=Ec, Ej=Ej) - grounds - 2 * omegas
    else:
        omegas = np.sqrt(8 * Ec * Ej) - Ec
        alphas = np.ones_like(Ej) * (-Ec)
    return omegas, alphas  # given that Ec is unit, these also get the unit Ec


def index_map(N):
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
    idx_map = [[[j + i * N + k*N**2 for j in range(N)] for i in range(N)] for k in range(N)]
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
