from tkinter import *
import numpy as np

N, zoom = 201, 4


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
        topple = self.topple
        where = np.where

        while np.max(self.grid) >= self.max_grains:
            elem_x, elem_y = where(self.grid >= self.max_grains)
            topple(elem_x, elem_y)
            iterations += 1

        print(f"{iterations} iterations {time() - start_time} seconds")

    def get_pile(self):
        return self.grid

    def set_sand(self, x, y, number):
        self.grid[x, y] = number

    def __add__(self, other):
        result = Sandpile(rows=self.rows, cols=self.cols)
        try:
            result.grid = self.grid + other.grid
            return result.run()
        except ValueError:
            print("ValueError: sandpile grid sizes must match")


colors = ["#b3cde0", "#6497b1", "#005b96", "#03396c", "#011f4b"]

root = Tk()
root.resizable(False, False)

c = Canvas(
    root, width=zoom * N, height=zoom * N, borderwidth=0, highlightbackground="red"
)
c.pack()

pile = Sandpile(rows=N, cols=N)

pile.set_sand(N // 2, N // 2, 2**16)

print("Running...")
pile.run()
print("Run finished")
grid = pile.get_pile()

print(grid)

for i in range(N):
    for j in range(N):
        x, y = zoom * i, zoom * j
        c.create_rectangle(
            x, y, x + zoom, y + zoom, outline="", fill=colors[grid[i][j]]
        )

print("Render finised")
root.mainloop()
