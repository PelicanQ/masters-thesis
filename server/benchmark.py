import numpy as np
import cupy as cp
import timeit

device = cp.cuda.Device()
print("Device ID:", device.id)
props = cp.cuda.runtime.getDeviceProperties(device.id)

print(f"\n📊 Device Info:")
print(f"Name: {props['name'].decode()}")
print(f"Total Memory: {props['totalGlobalMem'] / 1e9:.2f} GB")
print(f"Multiprocessors: {props['multiProcessorCount']}")
print(f"Compute Capability: {props['major']}.{props['minor']}")
print(f"Clock Rate: {props['clockRate'] / 1e3:.0f} MHz")


#
def task(size):
    a = np.random.rand(size, size)
    cp.linalg.eigh(cp.asarray(a))


t = timeit.timeit(lambda: task(10000), setup=lambda: task(10000), number=6)
print("time:", t)
# 10'000 x 10'000
# desktop: 54.6 s
# laptop 101.5 s
# PodRun:
# RTX 6000 Ada: 28.0 s (~0.1kr)
# H100 SXM: 9.1s (~0.05kr)
# H200: 9.8s (~0.11kr)
