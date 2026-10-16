import tkinter as tk
import threading
import random
import numpy as np
from PIL import Image, ImageTk

W, H, zoom = 101, 101, 8


class Sandpile:
    def __init__(self, rows, cols):
        self.max_grains = 4
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((cols, rows), int)

    def topple(self, elem_x, elem_y):
        p = self.grid[elem_x, elem_y]
        b = p // self.max_grains
        o = p % self.max_grains
        self.grid[elem_x, elem_y] = o

        # increase height of neighbor piles
        self.grid[elem_x - 1, elem_y] += b
        self.grid[elem_x + 1, elem_y] += b
        self.grid[elem_x, elem_y - 1] += b
        self.grid[elem_x, elem_y + 1] += b

        # border
        self.grid[0] = self.grid[-1] = 0
        self.grid[:, 0] = self.grid[:, -1] = 0

    def run(self):
        from time import time

        start_time = time()
        iterations = 0

        while np.max(self.grid) >= self.max_grains:
            elem_x, elem_y = np.where(self.grid >= self.max_grains)
            self.topple(elem_x, elem_y)
            iterations += 1
            image_grid()

        print(f"{iterations} iterations {time() - start_time} seconds")
        print("Run finished")

    def get_pile(self):
        return self.grid

    def set_sand(self, x, y, number):
        self.grid[x, y] = number


def image_grid():
    squares = []
    for row in range(H):
        for col in range(W):
            x1 = col * zoom
            y1 = row * zoom
            x2 = x1 + zoom
            y2 = y1 + zoom
            squares.append((x1, y1, x2, y2, colors[min(grid[col, row], 4)]))

    for square in squares:
        x1, y1, x2, y2, color = square
        img.paste(color, (x1, y1, x2, y2))

    photo = ImageTk.PhotoImage(img)
    canvas.itemconfig(image_item, image=photo)
    canvas.photo = photo


colors = ["#b3cde0", "#6497b1", "#005b96", "#03396c", "#000000"]  # 0, 1, 2, 3, >=4


root = tk.Tk()
root.resizable(False, False)

canvas_width, canvas_height = W * zoom, H * zoom

canvas = tk.Canvas(
    root, width=canvas_width, height=canvas_height, borderwidth=0, highlightthickness=0
)
canvas.pack()

pile = Sandpile(H, W)

# pile.set_sand(W // 2, H // 2, 2**10)
for _ in range(10):
    pile.set_sand(
        random.randint(10, W - 10),
        random.randint(10, H - 10),
        2 ** random.randint(8, 12),
    )

grid = pile.get_pile()

img = Image.new("RGB", (canvas_width, canvas_height))
photo = ImageTk.PhotoImage(img)
image_item = canvas.create_image(0, 0, image=photo, anchor=tk.NW)
canvas.photo = photo

image_grid()

print("Running...")
thread = threading.Thread(target=pile.run)
thread.start()

root.mainloop()
