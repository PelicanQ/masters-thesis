from sympy import Matrix, kronecker_product, Symbol
import sympy as sp
from typing import Literal


def getHintLine(a, c, numbits, statesperbit):
    # This gives the Hint for a line of qubits
    Hint = Matrix.zeros(statesperbit**numbits)
    I = Matrix.eye(statesperbit)
    gs = []
    for i in range(numbits - 1):
        seq = [a + c if k == i or k == i + 1 else I for k in range(numbits)]
        g = Symbol(f"g_{{{i},{i+1}}}")
        gs.append(g)
        Hint = Hint + g * kronecker_product(*seq)
    return Hint, gs


def getHintTriang(a, c, numbits, statesperbit):
    I = Matrix.eye(statesperbit)
    Hint = Matrix.zeros(statesperbit**numbits)
    zum = a + c
    if numbits == 3:
        Hint += Symbol("g_{1,2}") * kronecker_product(zum, zum, I)
        Hint += Symbol("g_{2,3}") * kronecker_product(I, zum, zum)
        Hint += Symbol("g_{1,3}") * kronecker_product(zum, I, zum)
    else:
        raise Exception("not impl")
    return Hint, [Symbol("g_{1,2}"), Symbol("g_{2,3}"), Symbol("g_{1,3}")]


def getHintGrid(a, c, numbits, statesperbit):
    I = Matrix.eye(statesperbit)
    Hint = Matrix.zeros(statesperbit**numbits)
    zum = a + c
    symbols = []
    if numbits == 4:
        Hint += Symbol("g_{1,2}") * kronecker_product(zum, zum, I, I)
        Hint += Symbol("g_{2,3}") * kronecker_product(I, zum, zum, I)
        Hint += Symbol("g_{3,4}") * kronecker_product(I, I, zum, zum)
        Hint += Symbol("g_{1,4}") * kronecker_product(zum, I, I, zum)
        symbols = [
            Symbol("g_{1,2}"),
            Symbol("g_{2,3}"),
            Symbol("g_{3,4}"),
            Symbol("g_{1,4}"),
        ]
    elif numbits == 6:

        Hint += Symbol("g_{1,2}") * kronecker_product(zum, zum, I, I, I, I)
        Hint += Symbol("g_{2,3}") * kronecker_product(I, zum, zum, I, I, I)
        Hint += Symbol("g_{3,4}") * kronecker_product(I, I, zum, zum, I, I)
        Hint += Symbol("g_{1,4}") * kronecker_product(zum, I, I, zum, I, I)

        Hint += Symbol("g_{2,5}") * kronecker_product(I, zum, I, I, zum, I)
        Hint += Symbol("g_{5,6}") * kronecker_product(I, I, I, I, zum, zum)
        Hint += Symbol("g_{3,6}") * kronecker_product(I, I, zum, I, I, zum)
        symbols = [
            Symbol("g_{1,2}"),
            Symbol("g_{2,3}"),
            Symbol("g_{3,4}"),
            Symbol("g_{1,4}"),
            Symbol("g_{2,5}"),
            Symbol("g_{5,6}"),
            Symbol("g_{3,6}"),
        ]
    else:
        raise Exception("Not impl  ")

    return Hint, symbols


def anhicreat(statesperbit):
    a = sp.MutableDenseMatrix(statesperbit, statesperbit, lambda i, j: sp.sqrt(j) if j == i + 1 else 0)
    c = sp.MutableDenseMatrix(statesperbit, statesperbit, lambda i, j: sp.sqrt(i) if j == i - 1 else 0)
    return a, c


def Hbare(i: int, statesperbit=None, a=None, c=None):
    if a == None or c == None:
        a, c = anhicreat(statesperbit)

    omega = Symbol(rf"\omega_{{{i}}}")
    alpha = Symbol(rf"\alpha_{{{i}}}")
    H = (
        (omega * c * a)
        + alpha / 2 * (c * c * a * a)
        - alpha / 2 * (c * c + a * a)
        - alpha / 3 * (c * a * a * a + c * c * c * a)
        + alpha / 12 * (a * a * a * a + c * c * c * c)
    )
    return H


def Hgen(numbits, statesperbit, layout: Literal["grid", "line", "triang"]):
    """
    Returns:
        sympy symbolic Hamiltonian
        symbols in order omegas, alphas, gs
    """
    I = Matrix.eye(statesperbit)
    a = sp.MutableDenseMatrix(statesperbit, statesperbit, lambda i, j: sp.sqrt(j) if j == i + 1 else 0)
    c = sp.MutableDenseMatrix(statesperbit, statesperbit, lambda i, j: sp.sqrt(i) if j == i - 1 else 0)
    Hbaretot: sp.Matrix = Matrix.zeros(statesperbit**numbits)
    for i in range(numbits):
        seq = [Hbare(i, a=a, c=c) if i == k else I for k in range(numbits)]
        Hbaretot += kronecker_product(*seq)

    symbols = [Symbol(rf"\omega_{{{i}}}") for i in range(numbits)]  # order is important
    symbols.extend([Symbol(rf"\alpha_{{{i}}}") for i in range(numbits)])

    Htot: sp.Matrix = Hbaretot
    if numbits >= 2:
        if layout == "line":
            Hint, moresymbols = getHintLine(a, c, numbits, statesperbit)
        elif layout == "grid":
            Hint, moresymbols = getHintGrid(a, c, numbits, statesperbit)
        elif layout == "triang":
            Hint, moresymbols = getHintTriang(a, c, numbits, statesperbit)
        else:
            raise Exception("Unrecognized layout")
        symbols.extend(moresymbols)
        Htot += Hint

    return Htot, symbols
