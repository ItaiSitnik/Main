import tkinter as tk
import threading
import time
from PIL import Image, ImageTk
import random


def random_colors():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def generate_square_grid(width, height, square_size):
    colors = [random_colors() for _ in range(width * height)]
    squares = []
    for row in range(height):
        for col in range(width):
            x1 = col * square_size
            y1 = row * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            squares.append((x1, y1, x2, y2, colors[row * width + col]))
    return squares


def update_image():
    while True:
        squares = generate_square_grid(
            canvas_width // square_size, canvas_height // square_size, square_size
        )
        img = Image.new("RGB", (canvas_width, canvas_height))
        for square in squares:
            x1, y1, x2, y2, color = square
            img.paste(color, (x1, y1, x2, y2))
        photo = ImageTk.PhotoImage(img)
        canvas.itemconfig(image_item, image=photo)
        canvas.photo = photo
        time.sleep(0.1)


canvas_width = 500
canvas_height = 500
square_size = 20  # Change this value to set the size of the squares

root = tk.Tk()
root.title("Random Color Squares")

canvas = tk.Canvas(
    root, width=canvas_width, height=canvas_height, borderwidth=0, highlightthickness=0
)
canvas.pack()

photo = ImageTk.PhotoImage(Image.new("RGB", (canvas_width, canvas_height)))
image_item = canvas.create_image(
    canvas_width // 2, canvas_height // 2, anchor=tk.CENTER, image=photo
)
canvas.photo = photo

update_thread = threading.Thread(target=update_image)
update_thread.start()

root.mainloop()
