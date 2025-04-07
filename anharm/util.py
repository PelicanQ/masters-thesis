import numpy as np
import itertools
import networkx as nx
import sympy as sp
import re


def extract_subscript(text):
    """Extract subscript of a symbol name"""
    pattern = re.escape("{") + r"(.*?)" + re.escape("}")
    return re.findall(pattern, text)[0]


def num2state(i, statesperbit, numbits):
    if i >= statesperbit**numbits:
        raise Exception(f"number {i} is out of range")
    k = i
    blist = []
    for dim in range(numbits - 1, 0, -1):
        b = k // (statesperbit**dim)
        k -= b * statesperbit**dim
        blist.append(b)
    blist.append(k)
    return tuple(blist)


def proc(mat_in: sp.Matrix, numbits: int, statesperbit: int, maxsum: int):
    """
    Truncates matrix based on total excitation.
    Args:
        mat_in: sympy
        maxsum (int): The highest total excitation of a state to keep.
    Returns:
        result (tuple): A tuple containing
        - mat: numpy matrix with sympy object, truncated.
        - basisnames: names of basis states in "natural counting order".
        - exc_subspaces: index with i to get the hamiltonian indices of states with excitation i. Indices are in increasing order

    """
    mat = np.array(mat_in)
    i = numdel = 0
    while i < mat.shape[0]:
        state = num2state(i + numdel, statesperbit, numbits)
        if sum(state) > maxsum:
            # delete row and col with too high excitation sum
            mat = np.delete(mat, axis=0, obj=i)
            mat = np.delete(mat, axis=1, obj=i)
            numdel += 1
        else:
            i += 1

    basisnames = []
    exc_subspaces = [[] for _ in range(maxsum + 1)]  # element i contains hamiltonian indices for states with sum i

    for comb in itertools.product(range(statesperbit), repeat=numbits):
        # product returns with the "natural counting" order
        summ = sum(comb)
        if summ > maxsum:
            continue
        basisnames.append("".join(map(str, comb)))
        exc_subspaces[summ].append(len(basisnames) - 1)  # the latest index is added to its exc subspace

    return mat, basisnames, exc_subspaces


def proc_subspace(mat: sp.Matrix, excitation: int, numbits: int, statesperbit: int):
    """
    Process and isolate only one excitation subspace
    Returns:
        - numpy mat of subspace, sympy elements
        - adjecency
        - names of subspace states
        - map from state string to index in mat
    """
    mat, basisnames, excsubspaces = proc(mat, numbits, statesperbit, statesperbit)
    # list of indices in truncated hamiltonian for chosen subspace
    subspace_indices = excsubspaces[excitation]
    submat = mat[np.ix_(subspace_indices, subspace_indices)]  # isolated to one subspace

    # adjacency matrix indicating connection or not
    adjecency = np.vectorize(lambda obj: not obj.is_zero)(submat)

    subspace_names = [basisnames[i] for i in subspace_indices]
    # key with state to get submat hamiltonian index
    idx_map = dict([(name, i) for i, name in enumerate(subspace_names)])

    return (
        submat,
        adjecency,
        subspace_names,
        idx_map,
    )


# to be used with the graphviz code
def subspace(summ: int, mid: complex, rad: float) -> list[tuple[str, complex]]:
    # return list of all ("12", 1+1j) in an excitation subspace
    interior_angle = (N - 2) * np.pi / N
    combinations = [comb for comb in itertools.product(range(summ + 1), repeat=N) if sum(comb) == summ]
    lattice_vecs = [rad * np.exp(1j * (-interior_angle / 2 + k * 2 * np.pi / N)) for k in range(N)]
    # lattice_vecs[1] *= 1.1
    nodes = []
    for i, comb in enumerate(combinations):
        name = "".join(map(str, comb))
        pos = mid + np.dot(comb, lattice_vecs)  # |x y z> -> x*l1 + y*l2 + z*l2
        nodes.append((name, pos))
    return nodes


def is_path_graph_degree_check(G):
    """Checks if G is a single path (a line)."""
    return nx.is_tree(G) and G.number_of_edges() == G.number_of_nodes() - 1
