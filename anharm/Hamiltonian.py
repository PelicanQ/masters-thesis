from anharm.util import proc, subspace, proc_subspace, extract_subscript
from anharm.Hgen import Hgen
from sympy import Symbol
import sympy as sp
import itertools
from typing import Literal, Generator
from functools import reduce
import networkx as nx
import pandas as pd


class Hamil:
    def __init__(self, numbits: int, statesperbit: int, layout: Literal["line", "triang", "grid"]):
        # Only use 2 or more bits. For one use Hgen directly
        self.layout = layout
        self.numbits = numbits
        self.statesperbit = statesperbit
        mat, hamil_symbols = Hgen(numbits, statesperbit, layout)

        self.mat = mat  # symbolic matrix, no special truncation yet other than total excitation < statesperbit
        self._spaces: list[Subspace] = [None] * statesperbit  # these will be RWA excitation subspaces
        deltas = []
        # we take no special care to only include deltas between coupled elements. Just list all possible deltas
        for comb in itertools.combinations(range(self.numbits), 2):
            deltas.append(Symbol(rf"\Delta_{{{comb[0]},{comb[1]}}}"))

        # this list defines an order to symbols
        self.symbols = hamil_symbols.copy()
        # symbols are those directly in the symbolic matrix
        # extended symbols also include deltas
        self.symbols_extended = hamil_symbols.copy()
        self.symbols_extended.extend(deltas)

    def lambdify_matrix(self):
        """Return matrix as function which parameters in the saved order. Print .symbols to see order"""
        # subs_dict = dict([(s, vals[i]) for i, s in enumerate(self.symbols)])
        return sp.lambdify(self.symbols, self.mat, modules="numpy")

    def lambdify_expr(self, expr):
        variables = self.symbols_in_expr(expr)
        return sp.lambdify(variables, expr, "numpy"), variables

    def symbols_in_expr(self, expr: sp.Expr):
        # self.symbols gives the order of symbols. This extract symbols in expression following that order
        return list(filter(lambda symbol: symbol in expr.free_symbols, self.symbols_extended))

    def getall(self, state, keep_second_coupling: bool):
        # get total SW energy expression. Only the correction to bare state!
        return self.state2space(state).getall(state, keep_second_coupling)

    def getorder2(self, state):
        return self.state2space(state).getorder2(state)

    def getorder3(self, state):
        return self.state2space(state).getorder3(state)

    def getorder4(self, state):
        return self.state2space(state).getorder4(state)

    def getedges(self, state, order: int | None = None):
        return self.state2space(state).getedges(state, order)

    def getsecondedges(self, state, keep_2nd_coupling: bool):
        """2nd order couplings can be kept but not lambdified"""
        return self.state2space(state).getsecondedges(state, keep_2nd_coupling)

    def getlegs(self, state):
        return self.state2space(state).getlegs(state)

    def getbirds(self, state):
        return self.state2space(state).getbirds(state)

    def get3cycles(self, state):
        return self.state2space(state).get3cycles(state)

    def get4cycles(self, state):
        return self.state2space(state).get4cycles(state)

    def get_subspace(self, excitation: int):
        # lazily create subspaces to unburden constructor
        if self._spaces[excitation] == None:
            self._spaces[excitation] = Subspace(self.mat, self.numbits, self.statesperbit, excitation)
            return self._spaces[excitation]
        else:
            return self._spaces[excitation]

    @staticmethod
    def omega_to_delta(expr):
        """Meant to combine omegas to (qubit) deltas in a simple denominator. Assumptions are made about expression"""
        # find the omegas in expression.
        nums = set()
        for s in expr.free_symbols:
            if "omega" in s.name:
                n = int(extract_subscript(s.name))
                nums.add(n)
        nums = sorted(list(nums))
        if len(nums) < 2:
            return expr
        delta = Symbol(rf"\Delta_{{{nums[0]},{nums[1]}}}")

        return expr.subs(Symbol(rf"\omega_{{{nums[0]}}}"), delta + Symbol(rf"\omega_{{{nums[1]}}}"))

    @staticmethod
    def split_deltas(expr: sp.Expr):
        """Meant for manual post processing, e.g. before lambdify"""
        for sym in expr.free_symbols:
            if "Delta" not in sym.name:
                continue
            subscr: str = extract_subscript(sym.name)
            ns = subscr.split(",")
            n1 = int(ns[0])
            n2 = int(ns[1])
            # We keep our subscripts in increasing order
            if n2 - n1 == 1:
                continue
            replacement = sp.sympify(0)
            for i in range(n1, n2):
                replacement += Symbol(rf"\Delta_{{{i},{i+1}}}")
            expr = expr.subs(sym, replacement)

        return expr

    @staticmethod
    def combine_deltas(expr: sp.Expr, pairs: list[tuple[int, int, int]]):
        """Meant for manual post processing"""
        for pair in pairs:
            delta1 = Symbol(rf"\Delta_{{{pair[0]},{pair[1]}}}")
            delta2 = Symbol(rf"\Delta_{{{pair[1]},{pair[2]}}}")
            delta3 = Symbol(rf"\Delta_{{{pair[0]},{pair[2]}}}")
            expr = expr.subs(delta1, delta3 - delta2)
        return expr

    def to_delta(self, expr: sp.Expr):
        # substitute differences of omegas with deltas (qubit frequency detuning)
        replace_pairs = []
        # important, we use the "combination" order here

        for comb in itertools.combinations(range(self.numbits), 2):
            delta = Symbol(rf"\Delta_{{{comb[0]},{comb[1]}}}")
            pair = (Symbol(rf"\omega_{{{comb[0]}}}"), delta + Symbol(rf"\omega_{{{comb[1]}}}"))
            # pair = (Symbol(rf"\omega_{{{comb[0]}}}") - Symbol(rf"\omega_{{{comb[1]}}}"), delta)
            replace_pairs.append(pair)

        return expr.subs(replace_pairs)

    def state2excitation(self, state: str):
        if len(state) > self.numbits:
            raise Exception("State does not exist")
        chars = list(state)
        excitation = reduce(lambda prev, character: int(character) + prev, chars, 0)
        return excitation

    def state2space(self, state: str):
        return self.get_subspace(self.state2excitation(state))

    def zzexpr(
        self,
        zzstate: str,
        order: None | int = None,
        keep_second_coupling: bool = False,
        type: Literal["edges", "birds", "legs", "second", "3loop", "4loop"] = None,
    ):
        # specify order OR type or neither.
        # assume we only care about states with 1 and 0
        strlen = len(zzstate)
        topspace = self.state2space(zzstate)

        bottomspace = self.get_subspace(1)
        bottomstates = []
        for i, c in enumerate(zzstate):
            if c == "1":
                bottomstates.append(("0" * i) + "1" + ("0" * (strlen - i - 1)))

        def getterms(space: Subspace, state: str):
            if order == 2:
                return space.getorder2(state)
            elif order == 3:
                return space.getorder3(state)
            elif order == 4:
                return space.getorder4(state, keep_second_coupling)
            elif type != None:
                if type == "edges":
                    return space.getedges(state)
                elif type == "legs":
                    return space.getlegs(state)
                elif type == "birds":
                    return space.getbirds(state)
                elif type == "3loop":
                    return space.get3cycles(state)
                elif type == "4loop":
                    return space.get4cycles(state)
                elif type == "second":
                    return space.getsecondedges(state, keep_second_coupling)
            else:
                return space.getall(state, keep_second_coupling)

        toplevel = getterms(topspace, zzstate)
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
        self.basisnames = subspace_names  # this also defines an order to states like 00 01 02 10 11 12 20 ...
        self.idxmap = idxmap

        # statematrix is to get matrix element by state string
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

    def getorder4(self, state, keep_second_coupling: bool):
        # get total SW energy expression
        return (
            self.get4cycles(state)
            + self.getlegs(state)
            + self.getbirds(state)
            + self.getedges(state, order=4)
            + self.getsecondedges(state, keep_second_coupling)
        )

    def getall(self, state, keep_second_coupling: bool):
        # get total SW energy expression
        return (
            self.getedges(state)
            + self.getlegs(state)
            + self.getbirds(state)
            + self.get3cycles(state)
            + self.get4cycles(state)
            + self.getsecondedges(state, keep_second_coupling)
        )

    def getedges(self, state, order: None | int = None):
        """If order not given: both 2nd 4th order terms"""
        totalexpr = sp.sympify(0)
        num = 0
        for n in nx.neighbors(self.graph, state):
            # create one edge
            gconst = self.statemat.loc[state, n]
            delta = self.statemat.loc[state, state] - self.statemat.loc[n, n]
            delta = Hamil.omega_to_delta(delta)

            if order == 2:
                ex = gconst**2 / delta
            elif order == 4:
                ex = -(gconst**4) / delta**3
            else:
                ex = gconst**2 / delta - (gconst**4 / delta**3)

            totalexpr += ex
            num += 1

        return totalexpr

    def secondcoupling(self, state: str, target: str):
        paths = nx.all_simple_paths(self.graph, state, target, 2)
        paths = list(filter(lambda path: len(path) == 3, paths))  # remove direct paths
        t = sp.sympify(0)
        n1 = state
        n3 = target
        for path in paths:
            n2 = path[1]
            d12 = self.statemat.loc[n1, n1] - self.statemat.loc[n2, n2]
            d23 = self.statemat.loc[n2, n2] - self.statemat.loc[n3, n3]
            d12 = Hamil.omega_to_delta(d12)
            d23 = Hamil.omega_to_delta(d23)
            t += self.statemat.loc[n1, n2] * self.statemat.loc[n2, n3] * (1 / d12 - 1 / d23)

        return t / 2

    def order_states(self, s1: str, s2: str):
        if len(s1) != len(s2):
            raise Exception("State strings not same length")

        if self.basisnames.index(s1) > self.basisnames.index(s2):
            return s2, s1
        return s1, s2

    def getsecondedges(self, state, keep_2nd_coupling: bool):
        """Get '(2) edges'.
        2nd order coupling constants can be kept symbolically but these expressions cannot be lambdified for now.
        Order is 4.
        """
        totalexpr = sp.sympify(0)
        secondneighbors: set[str] = set()
        for n in nx.neighbors(self.graph, state):
            for nn in nx.neighbors(self.graph, n):
                if nn != state:
                    secondneighbors.add(nn)  # of course state is its neighbors neighbour

        for nn in secondneighbors:
            if keep_2nd_coupling:
                s1, s2 = self.order_states(state, nn)
                # We can choose
                gconst = Symbol(f"g^{{(2)}}_{{{s1},{s2}}}")
            else:
                gconst = self.secondcoupling(state, nn)  # calculate
            delta = self.statemat.loc[state, state] - self.statemat.loc[nn, nn]
            delta = Hamil.omega_to_delta(delta)
            delta = Hamil.omega_to_delta(delta)  # yes, twice
            totalexpr += gconst**2 / delta
        return totalexpr

    def getlegs(self, state):
        totalexpr = sp.sympify(0)
        num = 0
        for n in nx.neighbors(self.graph, state):
            for nn in nx.neighbors(self.graph, n):
                if nn == state:  # no cycle
                    continue
                num += 1
                # create leg between these
                g1 = self.statemat.loc[state, n]
                g2 = self.statemat.loc[n, nn]
                delta1 = self.statemat.loc[state, state] - self.statemat.loc[n, n]
                delta2 = self.statemat.loc[n, n] - self.statemat.loc[nn, nn]

                delta1 = Hamil.omega_to_delta(delta1)
                delta2 = Hamil.omega_to_delta(delta2)
                ex = -(g1**2) / delta1 / 4 * (g2 / delta2) ** 2 + 3 * g2**2 / delta2 / 4 * (g1 / delta1) ** 2
                totalexpr += ex
        # print("# legs: ", num)
        return totalexpr

    def getbirds(self, state):
        totalexpr = sp.sympify(0)
        num = 0
        for n1, n2 in itertools.combinations(nx.neighbors(self.graph, state), 2):
            num += 1
            g1 = self.statemat.loc[state, n1]
            g2 = self.statemat.loc[state, n2]
            delta1 = self.statemat.loc[state, state] - self.statemat.loc[n1, n1]
            delta2 = self.statemat.loc[state, state] - self.statemat.loc[n2, n2]
            delta1 = Hamil.omega_to_delta(delta1)
            delta2 = Hamil.omega_to_delta(delta2)

            ex = -(g1**2) / delta1 * (g2 / delta2) ** 2 - g2**2 / delta2 * (g1 / delta1) ** 2
            totalexpr += ex

        # print("# birds: ", num)
        return totalexpr

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
            delta1 = Hamil.omega_to_delta(delta1)
            delta2 = Hamil.omega_to_delta(delta2)

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

            delta1 = Hamil.omega_to_delta(delta1)
            delta2 = Hamil.omega_to_delta(delta2)
            delta3 = Hamil.omega_to_delta(delta3)
            delta4 = Hamil.omega_to_delta(delta4)
            ex = (
                g1 * g2 * g3 * g4 / (delta2 * delta3 * delta4) / 4
                + g1 * g2 * g3 * g4 / (delta1 * delta2 * delta3) / 4
                - 3 * g1 * g2 * g3 * g4 / (delta1 * delta3 * delta4) / 4
                + 3 * g1 * g2 * g3 * g4 / (delta1 * delta2 * delta4) / 4
            )
            total += ex
        return total


if __name__ == "__main__":
    Subspace.order_states("11", "20")
