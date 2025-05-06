import numpy as np
from exact.util import Eint_to_g


def gconstants(Ej1, Ej2, Ej3, Ej4, Eint12, Eint23, Eint13, Eint34):
    g12 = Eint_to_g(Ej1, Ej2, Eint12)
    g23 = Eint_to_g(Ej2, Ej3, Eint23)
    g13 = Eint_to_g(Ej1, Ej3, Eint13)
    g34 = Eint_to_g(Ej3, Ej4, Eint34)
    return g12, g23, g13, g34


if __name__ == "__main__":
    pass
