from graphviz import Graph
import numpy as np
import itertools
import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt
from util import proc, subspace, proc_subspace
from pyvis import network as pvn
import pathlib
from sympy import Symbol, pprint

# input a symbolic hamiltonian. Output analytic terms by either order or process

# convert hamiltonian into graph format
# find simple 2 3 or 4 cycles
# use edge weights attributes to get expression I guess, or refer back to hamiltonian.
# the graph format is more about finding paths

N = 3  # num qubits
file = pathlib.Path("hamil_line3_5.tsv").resolve()
mat = pd.read_csv(file, index_col=None, header=None, delimiter="\t").to_numpy()

statesperbit = round(mat.shape[0] ** (1 / N))  # num states per qubit

g: nx.Graph = nx.Graph()
exc = 3
submat, adjecency, subspace_names, idx_map = proc_subspace(mat, exc, N, statesperbit)
exit()
for i in range(adjecency.shape[0]):
    g.add_node(subspace_names[i])
    for j in range(i + 1, adjecency.shape[1]):
        if adjecency[i, j]:
            g.add_edge(subspace_names[i], subspace_names[j])

# single edge
for n in nx.neighbors(g, "111"):
    # create one edge
    gconst = Symbol(submat[idx_map["111"], idx_map[n]])
    delta = Symbol(submat[idx_map["111"], idx_map["111"]]) - Symbol(
        submat[idx_map[n], idx_map[n]]
    )
    print(gconst**2 / delta)
    # print(submat[idx_map["111"], idx_map[n]])

# legs
for n in nx.neighbors(g, "111"):
    for nn in nx.neighbors(g, n):
        if nn == "111":  # no cycle
            continue
        # create leg between these
        print(n, nn)

cycles = nx.simple_cycles(g)

# cycles = [*filter(lambda c: c[0] == "111", cycles)]
# print(list(cycles))
