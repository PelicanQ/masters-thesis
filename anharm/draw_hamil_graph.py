from graphviz import Graph
import numpy as np
import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt
from anharm.util import proc, subspace, proc_subspace
from anharm.Hgen import Hgen
from pyvis import network as pvn
import pathlib

# Draw RWA hamiltonain graphs


def plot3d(G: nx.Graph):
    # Generate 3D positions for nodes (using spring layout)
    pos = nx.spring_layout(G, dim=3)

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    # Draw the nodes
    x_vals = [pos[node][0] for node in G.nodes()]
    y_vals = [pos[node][1] for node in G.nodes()]
    z_vals = [pos[node][2] for node in G.nodes()]

    ax.scatter(x_vals, y_vals, z_vals, c="r", marker="o")

    # Draw the edges
    for edge in G.edges(data=True):
        x1, y1, z1 = pos[edge[0]]
        x2, y2, z2 = pos[edge[1]]
        ax.plot([x1, x2], [y1, y2], [z1, z2], c="b")
        ax.text(x1, y1, z1, edge[0])
        ax.text(x2, y2, z2, edge[1])
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    # Show the plot
    plt.show()


# matrix has to be in order i.e. (0,0) (0,1) (0,2) (1,0) (1,1) (1,2) ...

N = 4  # number of qubits
statesperbit = 4
mat, symbols = Hgen(N, statesperbit, "4")

# file = pathlib.Path("hamil_square4_5.csv").resolve()
# statesperbit = round(mat.shape[0] ** (1 / N))  # num states per qubit
# mat = pd.read_csv(file, index_col=None, header=None).to_numpy()


exc = 2
submat, adjecency, subspace_names, idx_map = proc_subspace(mat, exc, N, statesperbit)
g: nx.Graph = nx.Graph()

for i in range(adjecency.shape[0]):
    g.add_node(subspace_names[i])
    for j in range(i + 1, adjecency.shape[1]):
        if adjecency[i, j]:
            g.add_edge(subspace_names[i], subspace_names[j])


def trim(graph, state):
    """Remove nodes which are separated by more than 2"""
    todel = set()
    for n in list(graph.nodes):
        todel.add(n)

    # remove double neighbors
    for n in graph.neighbors(state):
        todel.discard(n)
        for nn in graph.neighbors(n):
            todel.discard(nn)
    for n in todel:
        graph.remove_node(n)


# trim(g, "1110")
plane, embedding = nx.check_planarity(g)
print("Is planar?", plane)
embedding: nx.PlanarEmbedding = embedding
# labeldict = dict([(i, name) for i, name in enumerate(subspace_names)])
# poses = nx.combinatorial_embedding_to_pos(embedding, False)
# ll = ["003", "030"]
# ff = dict([(a, poses[a]) for a in ll])
# poses = nx.(g)
# poses = nx.spring_layout(g, pos=poses)
# nx.draw_networkx(g)
# plt.show()
net = pvn.Network(notebook=True)
net.from_nx(g)
net.force_atlas_2based()
net.show("graph.html")


# draw with graphviz, probably useful for pretty visual using lattice vectors on graphs where it works
# def draw():
#     nodes = []
#     g = Graph(format="png", engine="neato")
#     nodes.extend(subspace(0, -1j, 0.5))
#     nodes.extend(subspace(1, 4, 0.5))
#     nodes.extend(subspace(2, 1j, 0.5))
#     nodes.extend(subspace(3, 4 + 1j, 0.5))
#     nodes.extend(subspace(4, 2j, 0.5))

#     for node in nodes:
#         pos = node[1]
#         g.node(
#             node[0],
#             pos=f"{np.real(pos)},{np.imag(pos)}!",
#             shape="box",
#             width="0.1",
#             height="0.05",
#         )
#     # g.save("graph")
#     # G: nx.Graph = nx.nx_agraph.read_dot("graph")

#     for i in range(mat.shape[0]):  # upper triangular part
#         for j in range(i + 1, mat.shape[1]):
#             print(basisnames[i], basisnames[j])
#             if mat[i, j] == "0":
#                 continue
#             g.edge(basisnames[i], basisnames[j], label="a")

#     g.render("graph")
