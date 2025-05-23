from sympy import Matrix, kronecker_product, Symbol
import sympy as sp
from typing import Literal

layouts = Literal["grid", "line", "triang", "4"]


def getHintLine(a, c, numbits, statesperbit):
    # This gives the Hint for a line of qubits
    Hint = Matrix.zeros(statesperbit**numbits)
    I = Matrix.eye(statesperbit)
    gs = []
    for i in range(numbits - 1):
        seq = [a + c if k == i or k == i + 1 else I for k in range(numbits)]
        g = Symbol(f"g_{{{i},{i+1}}}")  # shift so first bit get subscript 1
        gs.append(g)
        Hint = Hint + g * kronecker_product(*seq)
    return Hint, gs


def getHint4(a, c, numbits, statesperbit):
    if numbits != 4:
        raise Exception("Numbits must be 4")

    I = Matrix.eye(statesperbit)
    Hint = Matrix.zeros(statesperbit**numbits)
    g01 = Symbol("g_{0,1}")
    g12 = Symbol("g_{1,2}")
    g02 = Symbol("g_{0,2}")
    g23 = Symbol("g_{2,3}")
    symbols = [g01, g12, g02, g23]
    zum = a + c

    Hint += g01 * kronecker_product(zum, zum, I, I)
    Hint += g12 * kronecker_product(I, zum, zum, I)
    Hint += g02 * kronecker_product(zum, I, zum, I)
    Hint += g23 * kronecker_product(I, I, zum, zum)
    return Hint, symbols


def getHintTriang(a, c, numbits, statesperbit):
    I = Matrix.eye(statesperbit)
    Hint = Matrix.zeros(statesperbit**numbits)
    g01 = Symbol("g_{0,1}")
    g12 = Symbol("g_{1,2}")
    g02 = Symbol("g_{0,2}")
    symbols = [g01, g12, g02]
    zum = a + c
    if numbits == 3:
        Hint += g01 * kronecker_product(zum, zum, I)
        Hint += g12 * kronecker_product(I, zum, zum)
        Hint += g02 * kronecker_product(zum, I, zum)
    elif numbits == 5:
        g23 = Symbol("g_{2,3}")
        g34 = Symbol("g_{3,4}")
        g24 = Symbol("g_{2,4}")
        Hint += g01 * kronecker_product(zum, zum, I, I, I)
        Hint += g12 * kronecker_product(I, zum, zum, I, I)
        Hint += g02 * kronecker_product(zum, I, zum, I, I)

        Hint += g23 * kronecker_product(I, I, zum, zum, I)
        Hint += g34 * kronecker_product(I, I, I, zum, zum)
        Hint += g24 * kronecker_product(I, I, zum, I, zum)
        symbols.extend([g23, g34, g24])
    elif numbits == 7:
        g23 = Symbol("g_{2,3}")
        g34 = Symbol("g_{3,4}")
        g24 = Symbol("g_{2,4}")
        g45 = Symbol("g_{4,5}")
        g56 = Symbol("g_{5,6}")
        g46 = Symbol("g_{4,6}")
        Hint += g01 * kronecker_product(zum, zum, I, I, I, I, I)
        Hint += g12 * kronecker_product(I, zum, zum, I, I, I, I)
        Hint += g02 * kronecker_product(zum, I, zum, I, I, I, I)

        Hint += g23 * kronecker_product(I, I, zum, zum, I, I, I)
        Hint += g34 * kronecker_product(I, I, I, zum, zum, I, I)
        Hint += g24 * kronecker_product(I, I, zum, I, zum, I, I)

        Hint += g45 * kronecker_product(I, I, I, I, zum, zum, I)
        Hint += g56 * kronecker_product(I, I, I, I, I, zum, zum)
        Hint += g46 * kronecker_product(I, I, I, I, zum, I, zum)

        symbols.extend([g23, g34, g24, g45, g56, g46])
    else:
        raise Exception("not impl")
    return Hint, symbols


def getHintGrid(a, c, numbits, statesperbit):
    I = Matrix.eye(statesperbit)
    Hint = Matrix.zeros(statesperbit**numbits)
    zum = a + c
    symbols = []
    if numbits == 4:
        # TODO: Change indices to 0
        g01 = Symbol("g_{0,1}")
        g12 = Symbol("g_{1,2}")
        g23 = Symbol("g_{2,3}")
        g03 = Symbol("g_{0,3}")
        Hint += g01 * kronecker_product(zum, zum, I, I)
        Hint += g12 * kronecker_product(I, zum, zum, I)
        Hint += g23 * kronecker_product(I, I, zum, zum)
        Hint += g03 * kronecker_product(zum, I, I, zum)
        symbols = [g01, g12, g23, g03]
    elif numbits == 7:
        g01 = Symbol("g_{0,1}")
        g12 = Symbol("g_{1,2}")
        g02 = Symbol("g_{0,2}")

        g23 = Symbol("g_{2,3}")
        g34 = Symbol("g_{3,4}")
        g24 = Symbol("g_{2,4}")

        g25 = Symbol("g_{2,5}")
        g56 = Symbol("g_{5,6}")
        g26 = Symbol("g_{2,6}")

        Hint += g01 * kronecker_product(zum, zum, I, I, I, I, I)
        Hint += g12 * kronecker_product(I, zum, zum, I, I, I, I)
        Hint += g02 * kronecker_product(zum, I, zum, I, I, I, I)

        Hint += g23 * kronecker_product(I, I, zum, zum, I, I, I)
        Hint += g34 * kronecker_product(I, I, I, zum, zum, I, I)
        Hint += g24 * kronecker_product(I, I, zum, I, zum, I, I)

        Hint += g25 * kronecker_product(I, I, zum, I, I, zum, I)
        Hint += g56 * kronecker_product(I, I, I, I, I, zum, zum)
        Hint += g26 * kronecker_product(I, I, zum, I, I, I, zum)
        symbols = [g01, g12, g02, g23, g34, g24, g25, g56, g26]
    elif numbits == 8:
        g01 = Symbol("g_{0,1}")
        g12 = Symbol("g_{1,2}")
        g23 = Symbol("g_{2,3}")
        g34 = Symbol("g_{3,4}")
        g45 = Symbol("g_{4,5}")
        g56 = Symbol("g_{5,6}")
        g67 = Symbol("g_{6,7}")
        g07 = Symbol("g_{0,7}")
        Hint += g01 * kronecker_product(zum, zum, I, I, I, I, I, I)
        Hint += g12 * kronecker_product(I, zum, zum, I, I, I, I, I)
        Hint += g23 * kronecker_product(I, I, zum, zum, I, I, I, I)
        Hint += g34 * kronecker_product(I, I, I, zum, zum, I, I, I)
        Hint += g45 * kronecker_product(I, I, I, I, zum, zum, I, I)
        Hint += g56 * kronecker_product(I, I, I, I, I, zum, zum, I)
        Hint += g67 * kronecker_product(I, I, I, I, I, I, zum, zum)
        Hint += g07 * kronecker_product(zum, I, I, I, I, I, I, zum)
        symbols = [g01, g12, g23, g34, g45, g56, g67, g07]
    else:
        raise Exception("Not impleented")

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


def Hgen(numbits, statesperbit, layout: layouts):
    """
    line layout is the only options which works with any number of bits
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
    # notice that the Hamiltonian order counts the first bit as the leftmost in the kronecker products
    symbols = [Symbol(rf"\omega_{{{i}}}") for i in range(numbits)]  # order is important
    symbols.extend([Symbol(rf"\alpha_{{{i}}}") for i in range(numbits)])
    # print("Hbare done")
    Htot: sp.Matrix = Hbaretot
    if numbits >= 2:
        if layout == "line":
            Hint, moresymbols = getHintLine(a, c, numbits, statesperbit)
        elif layout == "grid":
            Hint, moresymbols = getHintGrid(a, c, numbits, statesperbit)
        elif layout == "triang":
            Hint, moresymbols = getHintTriang(a, c, numbits, statesperbit)
        elif layout == "4":
            Hint, moresymbols = getHint4(a, c, numbits, statesperbit)
        else:
            raise Exception("Unrecognized layout")
        symbols.extend(moresymbols)
        # print("Hint done")
        Htot += Hint
        # print("add done")

    return Htot, symbols
