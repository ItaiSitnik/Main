import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

# Make plot open in your browser
pio.renderers.default = 'browser'

# Data
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)

# Plot
fig = go.Figure(data=go.Scatter3d(
    x=x, y=y, z=z,
    mode='lines+markers',
    line=dict(color='cyan', width=6),
    marker=dict(size=3, color='magenta')
))

# Dark layout
fig.update_layout(
    title="Beautiful 3D Spiral",
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        bgcolor='black'
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    paper_bgcolor='black',
    font_color='white'
)

fig.show()
