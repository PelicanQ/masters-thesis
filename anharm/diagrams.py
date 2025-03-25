import networkx as nx
from util import proc, subspace, proc_subspace
from hamil import Hgen
from pyvis import network as pvn
from sympy import Symbol, Matrix
import sympy as sp
import itertools
from typing import Generator, Literal
import pandas as pd

# MAT_CACHE_DIR = "__hamilcache__"


class Hamil:
    def __init__(self, numbits, statesperbit, layout: Literal["line", "triang", "grid"]):
        self.layout = layout
        self.numbits = numbits
        self.statesperbit = statesperbit
        mat, hamil_symbols = Hgen(numbits, statesperbit, layout)

        self.mat = mat  # symbolic matrix, no special truncation yet other than total excitation < statesperbit
        self._spaces: list[Subspace] = [None] * statesperbit
        deltas = []
        for comb in itertools.combinations(range(self.numbits), 2):
            delta = Symbol(rf"\Delta_{{{comb[0]},{comb[1]}}}")
            deltas.append(delta)

        # this list defines an order to symbols
        self.symbols = hamil_symbols.copy()
        self.symbols_extended = hamil_symbols.copy()
        self.symbols_extended.extend(deltas)

    def lambdify(self):
        """Return matrix as function which parameters in the saved order. Print .symbols to see order"""
        # subs_dict = dict([(s, vals[i]) for i, s in enumerate(self.symbols)])
        return sp.lambdify(self.symbols, self.mat, modules="numpy")

    def get_subspace(self, i):
        # lazily create subspaces to unburden constructor
        if self._spaces[i] == None:
            self._spaces[i] = self.make_subspace(i)
            return
        else:
            return self._spaces[i]

    def make_subspace(self, excitation: int):
        return Subspace(self.mat, self.numbits, self.statesperbit, excitation)

    def to_delta(self, expr: sp.Expr):
        # substitute differences of omegas with deltas (qubit frequency detuning)
        replace_pairs = []
        # important, we use the "combination" order here
        for comb in itertools.combinations(range(self.numbits), 2):
            delta = Symbol(rf"\Delta_{{{comb[0]},{comb[1]}}}")
            pair = (Symbol(rf"\omega_{comb[0]}") - Symbol(rf"\omega_{comb[1]}"), delta)
            replace_pairs.append(pair)

        return expr.subs(replace_pairs)

    def symbols_in_expr(self, expr: sp.Expr):
        # self.symbols gives the order of symbols. This extract symbols in expression following that order
        return list(filter(lambda symbol: symbol in expr.free_symbols, self.symbols_extended))

    def zzexpr(self, state: str, order: None | int = None):
        # assume we only care about states with 1 and 0
        strlen = len(state)
        if strlen > self.numbits:
            raise Exception("State does not exist")
        n = state.count("1")
        topspace = self.get_subspace(n)

        bottomspace = self.get_subspace(1)
        bottomstates = []
        for i, c in enumerate(state):
            if c == "1":
                bottomstates.append(("0" * i) + "1" + ("0" * (strlen - i - 1)))

        def getterms(space: Subspace, state: str):
            if order == 2:
                return space.getorder2(state)
            elif order == 3:
                return space.getorder3(state)
            elif order == 4:
                return space.getorder4(state)
            else:
                return space.getall(state)

        toplevel = getterms(topspace, state)
        botlevel = sp.sympify(0)
        for stat in bottomstates:
            botlevel += getterms(bottomspace, stat)

        # think about the relative energy!!
        return toplevel - botlevel


class Subspace:
    def __init__(self, mat: sp.Matrix, numbits, statesperbit, total_excitation):
        self.numbits = numbits
        self.statesperbit = statesperbit

        mat, adjecency, subspace_names, idxmap = proc_subspace(mat, total_excitation, numbits, statesperbit)
        self.mat = mat
        self.adjecency = adjecency
        self.basisnames = subspace_names
        self.idxmap = idxmap

        self.statemat = pd.DataFrame(self.mat, index=self.basisnames, columns=self.basisnames)
        graph: nx.Graph = nx.Graph()
        for i in range(self.adjecency.shape[0]):
            graph.add_node(self.basisnames[i])
            for j in range(i + 1, self.adjecency.shape[1]):
                if self.adjecency[i, j]:
                    graph.add_edge(self.basisnames[i], self.basisnames[j])
        self.graph = graph

    def getorder2(self, state):
        # get total SW energy expression
        return self.getedges(state, order=2)

    def getorder3(self, state):
        # get total SW energy expression
        return self.get3cycles(state)

    def getorder4(self, state):
        # get total SW energy expression
        return self.get4cycles(state) + self.getlegs(state) + self.getbirds(state) + self.getedges(state, order=4)

    def getall(self, state):
        # get total SW energy expression
        return (
            self.getedges(state)
            + self.getlegs(state)
            + self.getbirds(state)
            + self.get3cycles(state)
            + self.get4cycles(state)
        )

    def getedges(self, state, order: None | int = None):
        """If order not given: both 2nd 4th order terms"""
        totalexc = sp.sympify(0)
        num = 0
        for n in nx.neighbors(self.graph, state):
            # create one edge
            gconst = self.statemat.loc[state, n]
            delta = self.statemat.loc[state, state] - self.statemat.loc[n, n]

            # print("delta", self.statemat.loc[state, state], self.statemat.loc[n, n])
            if order == 2:
                ex = gconst**2 / delta
            elif order == 4:
                ex = -(gconst**4) / delta**3
            else:
                ex = gconst**2 / delta * (1 - (gconst / delta) ** 2)

            totalexc += ex
            num += 1
        # print("# single edges: ", num)
        return totalexc

    # def get2edge(self, state):

    def getlegs(self, state):
        totalexc = sp.sympify(0)
        num = 0
        for n in nx.neighbors(self.graph, state):
            for nn in nx.neighbors(self.graph, n):
                if nn == state:  # no cycle
                    continue
                num += 1
                # create leg between these
                g1 = self.statemat.loc[state, n]
                g2 = self.statemat.loc[n, nn]

                # delta1 = Symbol(rf"\Delta_{{{state},{n}}}")
                # delta2 = Symbol(rf"\Delta_{{{n},{nn}}}")
                delta1 = self.statemat.loc[state, state] - self.statemat.loc[n, n]
                delta2 = self.statemat.loc[n, n] - self.statemat.loc[nn, nn]
                ex = -(g1**2) / delta1 / 4 * (g2 / delta2) ** 1 + 3 * g2**2 / delta2 / 4 * (g1 / delta1) ** 1
                totalexc += ex
        # print("# legs: ", num)
        return totalexc

    def getbirds(self, state):
        totalexc = sp.sympify(0)
        num = 0
        for n1, n2 in itertools.combinations(nx.neighbors(self.graph, state), 2):
            num += 1
            g1 = self.statemat.loc[state, n1]
            g2 = self.statemat.loc[state, n2]
            delta1 = self.statemat.loc[state, state] - self.statemat.loc[n1, n1]
            delta2 = self.statemat.loc[state, state] - self.statemat.loc[n2, n2]
            # delta1 = Symbol(rf"\Delta_{{{state},{n1}}}")
            # delta2 = Symbol(rf"\Delta_{{{state},{n2}}}")
            ex = -(g1**2) / delta1 * (g2 / delta2) ** 2 - g2**2 / delta2 * (g1 / delta1) ** 2
            totalexc += ex

        # print("# birds: ", num)
        return totalexc

    def get3cycles(self, state):
        total = sp.sympify(0)

        cycles: Generator[list[str], None, None] = nx.simple_cycles(self.graph, length_bound=3)
        filt = list(filter(lambda c: state in c, cycles))
        three = list(filter(lambda c: len(c) == 3, filt))
        # print("# 3-cycles: ", len(three))
        for c_in in three:
            c = c_in.copy()
            while c[0] != state:  # permute unitil desired state is first
                c.insert(0, c.pop())
            n1, n2 = c[1:]
            g1 = self.statemat.loc[state, n1]
            g2 = self.statemat.loc[n1, n2]
            g3 = self.statemat.loc[state, n2]
            delta1 = self.statemat.loc[state, state] - self.statemat.loc[n1, n1]
            delta2 = self.statemat.loc[state, state] - self.statemat.loc[n2, n2]
            # delta1 = Symbol(rf"\Delta_{{{state},{n1}}}")
            # delta2 = Symbol(rf"\Delta_{{{state},{n2}}}")
            ex = 2 * g1 * g2 * g3 / (delta1 * delta2)
            total += ex
        return total

    def get4cycles(self, state):
        total = sp.sympify(0)
        cycles: Generator[list[str], None, None] = nx.simple_cycles(self.graph, length_bound=4)
        filt = list(filter(lambda c: state in c, cycles))
        four = list(filter(lambda c: len(c) == 4, filt))
        # print("# 4-cycles: ", len(four))

        for c_in in four:
            c = c_in.copy()
            while c[0] != state:  # permute unitil desired state is first
                c.insert(0, c.pop())
            n1, n2, n3 = c[1:]
            g1 = self.statemat.loc[state, n1]
            g2 = self.statemat.loc[n1, n2]
            g3 = self.statemat.loc[n2, n3]
            g4 = self.statemat.loc[state, n3]
            delta1 = self.statemat.loc[state, state] - self.statemat.loc[n1, n1]
            delta2 = self.statemat.loc[n1, n1] - self.statemat.loc[n2, n2]
            delta3 = self.statemat.loc[n2, n2] - self.statemat.loc[n3, n3]
            delta4 = self.statemat.loc[state, state] - self.statemat.loc[n3, n3]
            # delta1 = Symbol(rf"\Delta_{{{state},{n1}}}")
            # delta2 = Symbol(rf"\Delta_{{{n1},{n2}}}")
            # delta3 = Symbol(rf"\Delta_{{{n2},{n3}}}")
            # delta4 = Symbol(rf"\Delta_{{{state},{n3}}}")
            ex = (
                g1 * g2 * g3 * g4 / (delta2 * delta3 * delta4) / 4
                + g1 * g2 * g3 * g4 / (delta1 * delta2 * delta3) / 4
                - 3 * g1 * g2 * g3 * g4 / (delta1 * delta3 * delta4) / 4
                + 3 * g1 * g2 * g3 * g4 / (delta1 * delta2 * delta4) / 4
            )
            total += ex
        return total
