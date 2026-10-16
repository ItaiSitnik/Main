import random
import tkinter as tk

# Initialize the window
root = tk.Tk()
root.title("100 Fast and Smooth Moving Dots")

# Set up the canvas
canvas_width = 800
canvas_height = 800
canvas = tk.Canvas(
    root,
    width=canvas_width,
    height=canvas_height,
    bg="white",
    highlightbackground="black",
    highlightthickness=2,
)
canvas.pack()

# Number of dots
num_dots = 1000
dot_radius = 5  # Smaller radius to fit all dots

# Create lists to store dots, their positions, and velocities
dots = []
positions = []
velocities = []

# Initialize 100 dots with random positions and velocities
for _ in range(num_dots):
    # Random starting position
    x = random.uniform(dot_radius, canvas_width - dot_radius)
    y = random.uniform(dot_radius, canvas_height - dot_radius)

    # Random velocities
    dx = random.uniform(-16, 16)
    dy = random.uniform(-16, 16)

    # Create the dot and store its reference
    dot = canvas.create_oval(
        x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill="red"
    )
    dots.append(dot)

    # Store the position and velocity
    positions.append([x, y])
    velocities.append([dx, dy])


# Function to move all dots
def move_dots():
    for i in range(num_dots):
        x, y = positions[i]
        dx, dy = velocities[i]

        # Update the position
        x += dx
        y += dy

        # Bounce off the edges
        if x - dot_radius <= 0 or x + dot_radius >= canvas_width:
            dx = -dx
        if y - dot_radius <= 0 or y + dot_radius >= canvas_height:
            dy = -dy

        # Update positions and velocities
        positions[i] = [x, y]
        velocities[i] = [dx, dy]

        # Update the dot's position on the canvas
        canvas.coords(
            dots[i], x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius
        )

    # Call the function again after a small delay (16 ms for 60 FPS)
    root.after(16, move_dots)


# Start moving the dots
move_dots()

# Start the Tkinter event loop
root.mainloop()
