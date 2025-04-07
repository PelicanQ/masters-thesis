import numpy as np
import cupy as cp
# a = np.random.rand(40000, 40000)
# cp.linalg.eigh(cp.asarray(a))
# np.linalg.eigh(a)

# Get current device
device = cp.cuda.Device()
print("Device ID:", device.id)

# Get detailed device properties
props = cp.cuda.runtime.getDeviceProperties(device.id)

print(f"\n📊 Device Info:")
print(f"Name: {props['name'].decode()}")
print(f"Total Memory: {props['totalGlobalMem'] / 1e9:.2f} GB")
print(f"Multiprocessors: {props['multiProcessorCount']}")
print(f"Compute Capability: {props['major']}.{props['minor']}")
print(f"Clock Rate: {props['clockRate'] / 1e3:.0f} MHz")