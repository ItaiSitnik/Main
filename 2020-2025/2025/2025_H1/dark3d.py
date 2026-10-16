import matplotlib.pyplot as plt
import numpy as np

plt.style.use("Solarize_Light2")

def setup_ax(ax, title):
    ax.set_title(title, fontsize=10)
    ax.set_axis_off()

def plot_spiral(ax):
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 300)
    z = np.linspace(-2, 2, 300)
    r = z**2 + 1
    x = r * np.sin(theta)
    y = r * np.cos(theta)
    ax.plot3D(x, y, z, linewidth=1.5)
    setup_ax(ax, "3D Spiral")

def plot_helix(ax):
    t = np.linspace(0, 8 * np.pi, 300)
    x = np.sin(t)
    y = np.cos(t)
    z = t / (2 * np.pi)
    ax.plot3D(x, y, z, linewidth=1.5)
    setup_ax(ax, "Helix")

def plot_lissajous(ax):
    t = np.linspace(0, 2 * np.pi, 300)
    x = np.sin(3 * t + np.pi / 2)
    y = np.sin(4 * t)
    z = np.sin(5 * t)
    ax.plot3D(x, y, z, linewidth=1.5)
    setup_ax(ax, "Lissajous")

def plot_wave(ax):
    x = np.linspace(-10, 10, 300)
    y = np.sin(x)
    z = np.cos(2 * x)
    ax.plot3D(x, y, z, linewidth=1.5)
    setup_ax(ax, "3D Wave")

def plot_spiral_scatter(ax):
    n = 300
    theta = np.linspace(0, 4 * np.pi, n)
    z = np.linspace(-2, 2, n)
    r = z**2 + 1
    x = r * np.sin(theta) + 0.1 * np.random.randn(n)
    y = r * np.cos(theta) + 0.1 * np.random.randn(n)
    ax.scatter(x, y, z, c=theta, cmap="plasma", s=15)
    setup_ax(ax, "Spiral Scatter")

def plot_random_scatter(ax):
    n = 300
    x = np.random.randn(n)
    y = np.random.randn(n)
    z = np.random.randn(n)
    ax.scatter(x, y, z, c=np.sqrt(x**2 + y**2 + z**2), cmap="plasma", s=10)
    setup_ax(ax, "Random Scatter")

def plot_torus(ax):
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, 2 * np.pi, 40)
    u, v = np.meshgrid(u, v)
    R, r = 2, 0.6
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    ax.plot_wireframe(x, y, z, color="tab:blue", linewidth=0.5)
    setup_ax(ax, "Torus Wireframe")

def plot_parametric_surface(ax):
    u = np.linspace(-2, 2, 40)
    v = np.linspace(-2, 2, 40)
    u, v = np.meshgrid(u, v)
    x = u
    y = v
    z = np.sin(u**2 + v**2)
    ax.plot_wireframe(x, y, z, color="tab:orange", linewidth=0.5)
    setup_ax(ax, "Param Surface Wireframe")

def plot_helix_scatter(ax):
    t = np.linspace(0, 8 * np.pi, 300)
    x = np.sin(t) + 0.1 * np.random.randn(300)
    y = np.cos(t) + 0.1 * np.random.randn(300)
    z = t / (2 * np.pi) + 0.1 * np.random.randn(300)
    ax.scatter(x, y, z, c=t, cmap="viridis", s=15)
    setup_ax(ax, "Helix Scatter")

def plot_lissajous_scatter(ax):
    t = np.linspace(0, 2 * np.pi, 300)
    x = np.sin(3 * t + np.pi / 2) + 0.05 * np.random.randn(300)
    y = np.sin(4 * t) + 0.05 * np.random.randn(300)
    z = np.sin(5 * t) + 0.05 * np.random.randn(300)
    ax.scatter(x, y, z, c=t, cmap="cividis", s=15)
    setup_ax(ax, "Lissajous Scatter")

plot_funcs = [
    plot_spiral,
    plot_helix,
    plot_lissajous,
    plot_wave,
    plot_spiral_scatter,
    plot_random_scatter,
    plot_torus,
    plot_parametric_surface,
    plot_helix_scatter,
    plot_lissajous_scatter,
]

fig = plt.figure(figsize=(18, 10))

for i, func in enumerate(plot_funcs, 1):
    ax = fig.add_subplot(2, 5, i, projection='3d')
    func(ax)

plt.tight_layout()
plt.show()
