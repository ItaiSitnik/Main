from tkinter import *
import numpy as np
import random

N = 101


class Sandpile:
    def __init__(self, arr=None, rows=3, cols=3, max_sand=4):
        """
        arr - 2d array of values
        rows - height of sandpile
        cols - width of sandpile
        max_sand - max count of sandpile grains (must be div by 4)
        """
        self.max_grains = max_sand
        if arr == None:
            self.rows = rows
            self.cols = cols
            self.grid = np.zeros((cols, rows), int)
        else:
            self.rows = len(arr)
            self.cols = len(arr[0])
            self.grid = np.array(arr)

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

        print("--- %d iterations %s seconds ---" % (iterations, time() - start_time))

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

    # def show(self, save=False, filename="sandpile.png"):
    #     """
    #     plot sandpile and/or save it in the file

    #     save - true = save picture, false = dont save picture
    #     filename - name of the file, where would be picture of sandpile
    #     """

    #     heatmap = plt.pcolor(self.grid)
    #     plt.axis("off")
    #     plt.imshow(self.grid)
    #     plt.colorbar(heatmap, ticks=range(self.max_grains))
    #     if save:
    #         plt.savefig(filename, bbox_inches="tight")
    #     plt.show()

    # def save(self, filename="sandpile.png"):
    #     from PIL import Image

    #     colors = [(255, 255, 0), (0, 185, 63), (0, 104, 255), (122, 0, 229)]
    #     img = Image.fromarray(color_grid(self.grid, colors), "RGB")
    #     img.save(filename)


# def color_grid(grid, colors):
#     new_grid = np.zeros((len(grid), len(grid[0]), 3), dtype=np.uint8)
#     for i in range(len(new_grid)):
#         for j in range(len(new_grid[0])):
#             new_grid[i, j] = colors[grid[i, j]]
#     return new_grid


# if __name__ == "__main__":
#     pile = Sandpile(rows=601, cols=601)
#     pile.set_sand(300, 300, 2**16)
#     pile.run()
#     pile.show(save=True, filename="2^16 grains(1).png")
#     pile.save(filename="2^16 grains(2).png")

colors = ["#b3cde0", "#6497b1", "#005b96", "#03396c", "#011f4b"]

root = Tk()
root.resizable(False, False)

# root.minsize(400, 400)
# root.maxsize(400, 400)

# c = Canvas(root)
c = Canvas(root, width=2 * N, height=2 * N, borderwidth=0, highlightbackground="red")
c.pack()
# # c.create_rectangle(100, 100, 200, 200)
# # c.create_rectangle(50, 50, 180, 120, outline="black", fill="blue", dash=(4, 6))
# for x in range(N + 2):
#     for y in range(N + 2):
#         # de = "%02x" % random.randint(0, 255)
#         # re = "%02x" % random.randint(0, 255)
#         # we = "%02x" % random.randint(0, 255)
#         # ge = "#"
#         # color = ge + de + re + we
#         c.create_line(x, y, x + 1, y, fill=colors[random.randint(0, 4)])
# # c.create_rectangle(0, 0, 400, 400, fill="#FF00FF")

pile = Sandpile(rows=N, cols=N)
# pile.set_sand(N // 2, N // 2, 2**18)

# pile.set_sand(N // 3, N // 2, 2**12)
# pile.set_sand(2 * N // 3, N // 2, 2**16)

for _ in range(20):
    pile.set_sand(
        random.randint(10, N), random.randint(10, N), 2 ** random.randint(10, 16)
    )

print("Running...")
pile.run()
# pile.show(save=True, filename="2^16 grains(1).png")
# pile.save(filename="2^16 grains(2).png")
print("Run finished")
grid = pile.get_pile()
print(grid)
for x in range(N):
    for y in range(N):
        c.create_line(x, y, x + 1, y, fill=colors[grid[x][y]])
        # c.create_rectangle(
        #     2 * x, 2 * y, 2 * x + 2, 2 * y + 2, outline="", fill=colors[grid[x][y]]
        # )
print("Render finised")
root.mainloop()
