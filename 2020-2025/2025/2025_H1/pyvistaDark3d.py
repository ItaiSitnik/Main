import numpy as np
import pyvista as pv

# Data
theta = np.linspace(0, 4 * np.pi, 100)
z = np.linspace(-1, 1, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)
points = np.column_stack((x, y, z))

# Use the proper Theme object
plotter = pv.Plotter(window_size=(800, 600), theme=pv.themes.ParaViewTheme())

# Plot
plotter.add_lines(points, width=3)
plotter.show()
