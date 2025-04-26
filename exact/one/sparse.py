# Here we see if switchiing to sparse matrices increases speed and the max matrix size we can handle

import numpy as np
from scipy import linalg
from scipy import sparse
from scipy.sparse import linalg as spalg
from onetransmon.hamil import Hgen
from matplotlib import pyplot as plt
import timeit
import cupy as cp

# Cupy sparse eigsh is not reliable. It gives NaN or very large.
# Instead comparse scipy sparse/dense
# We do one transmon Hamil.


def all_run(k):
    H = Hgen(0, 100, k)

    # this is to give a warmup call
    def run_sparse(H):
        H = sparse.csr_array(H)
        vals = spalg.eigsh(H, k=2 * k, which="SA", return_eigenvectors=False)

    def sp_dense(H):
        vals = linalg.eigvalsh(H)

    def sp_tri(H: np.ndarray):
        vals = linalg.eigvalsh_tridiagonal(H.diagonal(), H.diagonal(1))

    def run_cp(H):
        vals = cp.linalg.eigvalsh(cp.asarray(H))

    # t_sp_dense = timeit.timeit(lambda: sp_dense(H), number=1)

    t_sp_tri = timeit.timeit(lambda: sp_tri(H), number=1)

    t_cp = timeit.timeit(lambda: run_cp(H), number=1)

    return (t_sp_tri, t_cp)


k = 1000
all_run(k)  # warm up
(t_sp_tri, t_cp) = all_run(k)

plt.bar(
    [
        "scipy tri",
        "cupy eigvalsh",
    ],
    [t_sp_tri, t_cp],
)

plt.title(f"Eigevals calculation time, k={k}")
plt.ylabel("time (s)")
plt.show()
