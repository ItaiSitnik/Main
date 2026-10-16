import matplotlib.pyplot as plt
import numpy

x = rand(10_000, 1)
y = -log(x)

h = plt.hist(y, bins=100)
plt.show()

h = plt.hist(x, bins=100)
plt.show()
