import numpy as np
import quaternion

# Define the quaternion basis elements i, j, k
i = np.quaternion(0, 1, 0, 0)  # i = (0 + 1i + 0j + 0k)
j = np.quaternion(0, 0, 1, 0)  # j = (0 + 0i + 1j + 0k)
k = np.quaternion(0, 0, 0, 1)  # k = (0 + 0i + 0j + 1k)

# List of quaternion basis elements
elements = {"i": i, "j": j, "k": k}

# Function to calculate commutator [x, y] = xy - yx
def commutator(x, y):
    return x * y - y * x

# Helper function to format quaternion as ijk string
def format_quaternion(q):
    w, x, y, z = q.w, q.x, q.y, q.z
    terms = []
    if x != 0:
        terms.append(f"{x}i")
    if y != 0:
        terms.append(f"{y}j")
    if z != 0:
        terms.append(f"{z}k")
    if not terms:
        return "0"
    return " + ".join(terms)

# Iterate over all pairs and calculate commutators
for x_name, x in elements.items():
    for y_name, y in elements.items():
        comm = commutator(x, y)
        formatted_comm = format_quaternion(comm)
        print(f"[{x_name}, {y_name}] = {formatted_comm}")
