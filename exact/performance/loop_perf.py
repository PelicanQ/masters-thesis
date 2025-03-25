import numpy as np
import timeit
from numba import jit

N = 3
T = 2000000

# np.linalg.eigh() on a 3x3 symmetric
# manual looping, no jit, 4.7
# timeit looping, no jit, 4.6
# manual looping, jit, 0.95
# timeit looping, jit, 1.1, 0,96 also...
# Here the loop was overhead small in comparison to computation. jit made eigh faster

# now with very simple math but more looping
# manual looping, no jit, 3.8 3.8
# timeit looping, no jit, 3.7 3.8
# manual looping, jit, 0.016 0.017
# timeit looping, jit, 0.11 0.11
# jit made eigh faster AND looping

# makes sense that without jit it doesnt matter if I loop of if timeit loops
# with jit, only function I can decorate will have faster loops
# thus the more looping I do myself, the more overhead jit can eliminate
# good to remember when measuring perf that large 'number' to timeit will mask jit loop speedup


@jit
def do():
    return np.random.randint(1, 10) ** 2 + 6**2


# A = np.random.rand(N, N)
# A = A + A.T
# def do2():
# return np.linalg.eigh(A)


@jit
def run():
    # symmetric means real eigenvalues.
    # Numba does not like how numpy.linalg.eig will decide return type to real or complex at runtime
    # for _ in range(T):
    do()


run()  # make sure caching is done
t = timeit.timeit(run, number=T)
print(t)
