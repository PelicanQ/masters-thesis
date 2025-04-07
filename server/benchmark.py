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


t = timeit.timeit(lambda: task(10000), setup=lambda: task(10000),number=6)
print("time:",t)
# desktop: 54.6