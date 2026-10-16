import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# Rodrigues' rotation formula
def rodrigues_rotation_matrix(axis, theta):
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    K = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    I = np.eye(3)
    return I + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)


# Flag geometry
def create_flag_geometry():
    pole = np.array([[0, 0, 0], [0, 1, 0]])
    flag = np.array([[0, 0.8, 0], [0.5, 0.8, 0], [0.5, 1, 0], [0, 1, 0]])
    return pole, flag


# Rotate a set of points
def rotate_geometry(geometry, R):
    return geometry @ R.T


# Random axis on unit sphere
def random_unit_vector():
    vec = np.random.randn(3)
    return vec / np.linalg.norm(vec)


# Draw unit sphere
def draw_unit_sphere(ax):
    u, v = np.mgrid[0 : 2 * np.pi : 30j, 0 : np.pi : 15j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, color="lightblue", alpha=0.2, edgecolor="gray", linewidth=0.3)


# Ensure cubic plot box
def set_cubic_limits(ax, lim=1):
    ax.set_xlim([-lim, lim])
    ax.set_ylim([-lim, lim])
    ax.set_zlim([-lim, lim])
    ax.set_box_aspect([1, 1, 1])


# Plot flag and sphere
def plot_flag(ax, pole, flag, color="green"):
    ax.clear()
    draw_unit_sphere(ax)
    ax.plot(*pole.T, color="black", lw=3)
    poly = Poly3DCollection([flag], facecolors=color, edgecolors="k", linewidths=1, alpha=0.8)
    ax.add_collection3d(poly)
    set_cubic_limits(ax)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Flag Rotating Randomly on Sphere")


# Set up
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")
base_pole, base_flag = create_flag_geometry()
angle_step = np.radians(4)
axis = random_unit_vector()
R_total = np.eye(3)


# Animation function
def update(frame):
    global R_total, axis
    if frame % 40 == 0:
        axis = random_unit_vector()
    R_step = rodrigues_rotation_matrix(axis, angle_step)
    R_total = R_step @ R_total
    pole_rot = rotate_geometry(base_pole, R_total)
    flag_rot = rotate_geometry(base_flag, R_total)
    plot_flag(ax, pole_rot, flag_rot, color="orange")


# Run animation
ani = FuncAnimation(fig, update, frames=300, interval=50, repeat=True)
plt.show()
