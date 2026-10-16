import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider


def bezier_recursive(points, t):
    return points[0] if len(points) == 1 else bezier_recursive([(1 - t) * p0 + t * p1 for p0, p1 in zip(points[:-1], points[1:])], t)

def generate_random_points(n=7):
    points = [np.array([0, 0, 0])]
    for _ in range(n - 2):
        points.append(np.random.randint(0, 18, size=3))
    points.append(np.array([18, 18, 18]))
    return points

control_points = generate_random_points()
control_points_arr = np.array(control_points)

def compute_curve(t_max):
    ts = np.linspace(0, t_max, 100)
    return np.array([bezier_recursive(control_points, t) for t in ts])

curve_arr = compute_curve(1.0)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
curve_plot, = ax.plot(*curve_arr.T, 'b-', linewidth=2.5, label='Bézier Curve')
ctrl_line, = ax.plot(*control_points_arr.T, 'k--', alpha=0.4, label='Control Polygon')
ctrl_dots, = ax.plot(*control_points_arr.T, 'ko', alpha=0.6)  # same data, just dots

ax.set_xlabel("X")
ax.set_xlim(0,18)
ax.set_ylabel("Y")
ax.set_ylim(0,18)
ax.set_zlabel("Z")
ax.set_zlim(0,18)
ax.set_title("3D Bézier Curve with 10 Random Control Points")
ax.legend()

# Slider for max t
slider_ax = plt.axes([0.2, 0.03, 0.6, 0.02])
t_slider = Slider(slider_ax, 'Max t', 0.01, 1.0, valinit=1.0)

def update_curve(t_max):
    global curve_arr
    curve_arr = compute_curve(t_max)
    curve_plot.set_data(curve_arr[:, 0], curve_arr[:, 1])
    curve_plot.set_3d_properties(curve_arr[:, 2])
    fig.canvas.draw_idle()

t_slider.on_changed(update_curve)

# Re-roll button
button_ax = plt.axes([0.8, 0.9, 0.15, 0.05])
reroll_button = Button(button_ax, 'Re-roll Points')

def reroll(event):
    global control_points, control_points_arr
    control_points = generate_random_points()
    control_points_arr = np.array(control_points)
    ctrl_line.set_data(control_points_arr[:, 0], control_points_arr[:, 1])
    ctrl_line.set_3d_properties(control_points_arr[:, 2])
    ctrl_dots.set_data(control_points_arr[:, 0], control_points_arr[:, 1])
    ctrl_dots.set_3d_properties(control_points_arr[:, 2])
    update_curve(t_slider.val)

reroll_button.on_clicked(reroll)

plt.show()
