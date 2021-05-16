import numpy as np


# array = np.array([2, 8, 7]).tofile("test.bin")
print(np.fromfile("test.bin",  dtype=np.int8))
