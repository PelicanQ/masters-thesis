from pathlib import Path
import dill
from anharm.Hamiltonian import Hamil

# import numpy as np

base = Path(__file__).parent / "__func_cache__"


class Cacher:
    """Used to cache functions which are heavy to compute"""

    @classmethod
    def savezz(cls, func, zz: str, statesperbit: int, layout: str = ""):
        base.mkdir(exist_ok=True)
        with open((base / f"zz_{zz}_{statesperbit}_{layout}").resolve(), "wb") as f:
            f.write(dill.dumps(func))

    @classmethod
    def getzz(cls, zz: str, statesperbit: int, layout: str = ""):
        with open((base / f"zz_{zz}_{statesperbit}_{layout}").resolve(), "rb") as f:
            return dill.loads(f.read())


if __name__ == "__main__":
    H = Hamil(3, 3, "line")
    f, vars = H.lambdify_expr(H.zzexpr("101"))
    # Cacher.savezz(f, 3, 5)
    f = Cacher.getzz(3, 5)
    # import inspect
    # print(inspect.getsource(f))
    # print(f.__globals__["sqrt"]))
