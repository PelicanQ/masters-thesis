import numpy as np
import time
import cupy
from exact.gale_shapely.gale_shapely import jitted_loop
from exact.gale_shapely.loop_cython import jitted_loop as cloop

N = 5000
a = np.random.rand(N, N)
vals, vecs = cupy.linalg.eigh(cupy.asarray(a))
vecs: np.ndarray = cupy.asnumpy(vecs)
number_of_states = vecs.shape[0]
preference = np.abs(vecs)
ranked_preference = np.argsort(preference, axis=0)
print(preference.dtype, ranked_preference.dtype)
# warmup, just in case
jitted_loop(ranked_preference, number_of_states, preference)
cloop(ranked_preference, number_of_states, preference)


t1 = time.perf_counter()
r1 = jitted_loop(ranked_preference, number_of_states, preference)
t2 = time.perf_counter()
r2 = cloop(ranked_preference, number_of_states, preference)
t3 = time.perf_counter()
print(t2 - t1)
print(t3 - t2)
d = all([r1[i] == r2[i] for i in range(len(r1))])
print(d)
