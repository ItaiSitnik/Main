import numpy as np

n = int(1e9)
X = np.random.random(n)
Y = np.random.random(n)

ratios = np.round(X / Y).astype(np.uint32)
even_ratio = np.count_nonzero(ratios % 2 == 0) / n

print(f"Proportion of even results: {even_ratio:.6f}")
