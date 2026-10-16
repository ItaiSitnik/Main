import random
import threading
import tkinter as tk

import numpy as np
from PIL import Image, ImageTk

W, H, ZOOM, MAX_GRAINS = 101, 101, 8, 4
canvas_width, canvas_height = W * ZOOM, H * ZOOM
grid = np.zeros((H, W), int)
colors = ["#b3cde0", "#6497b1", "#005b96", "#03396c", "#000000"]  # 0, 1, 2, 3, >=4


def topple(elem_x, elem_y):
    p = grid[elem_x, elem_y]
    b = p // MAX_GRAINS
    o = p % MAX_GRAINS
    grid[elem_x, elem_y] = o

    # increase height of neighbor piles
    grid[elem_x - 1, elem_y] += b
    grid[elem_x + 1, elem_y] += b
    grid[elem_x, elem_y - 1] += b
    grid[elem_x, elem_y + 1] += b

    # border
    grid[0] = grid[-1] = 0
    grid[:, 0] = grid[:, -1] = 0


def run():
    from time import time

    start_time = time()
    iterations = 0

    while np.max(grid) >= MAX_GRAINS:
        elem_x, elem_y = np.where(grid >= MAX_GRAINS)
        topple(elem_x, elem_y)
        iterations += 1
        draw_grid()

    print(f"{iterations} iterations {time() - start_time} seconds\nRun finished")


def draw_grid():
    squares = []
    for row in range(H):
        for col in range(W):
            x1, y1 = col * ZOOM, row * ZOOM
            x2, y2 = x1 + ZOOM, y1 + ZOOM
            squares.append((x1, y1, x2, y2, colors[min(grid[col, row], 4)]))

    for square in squares:
        x1, y1, x2, y2, color = square
        img.paste(color, (x1, y1, x2, y2))

    photo = ImageTk.PhotoImage(img)
    canvas.itemconfig(image_item, image=photo)
    canvas.photo = photo


root = tk.Tk()
root.resizable(False, False)

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, highlightthickness=0)
canvas.pack()

# grid[W // 2, H // 2] = 2**16
for _ in range(10):
    height = 2 ** random.randint(8, 12)
    grid[random.randint(10, W - 10), random.randint(10, H - 10)] = height

img = Image.new("RGB", (canvas_width, canvas_height))
photo = ImageTk.PhotoImage(img)
image_item = canvas.create_image(0, 0, image=photo, anchor=tk.NW)

draw_grid()

print("Running...")
threading.Thread(target=run).start()

root.mainloop()
