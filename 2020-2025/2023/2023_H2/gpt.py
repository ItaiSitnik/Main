import tkinter as tk
import threading
import time
from PIL import Image, ImageTk
import random


def random_colors(width, height):
    return [
        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for _ in range(width * height)
    ]


def update_image():
    while True:
        colors = random_colors(canvas_width, canvas_height)
        img.putdata(colors)
        photo = ImageTk.PhotoImage(img)
        canvas.itemconfig(image_item, image=photo)
        canvas.photo = photo  # To prevent image from being garbage collected
        time.sleep(0.1)  # Update every 100 milliseconds


canvas_width = 500
canvas_height = 500

root = tk.Tk()
root.title("Random Color Image")

canvas = tk.Canvas(
    root, width=canvas_width, height=canvas_height, borderwidth=0, highlightthickness=0
)  # Set highlightthickness to 0
canvas.pack()

img = Image.new("RGB", (canvas_width, canvas_height))
colors = random_colors(canvas_width, canvas_height)
img.putdata(colors)

photo = ImageTk.PhotoImage(img)
image_item = canvas.create_image(
    canvas_width // 2, canvas_height // 2, anchor=tk.CENTER, image=photo
)
canvas.photo = photo  # To prevent image from being garbage collected

# Start the thread to update the image
update_thread = threading.Thread(target=update_image)
update_thread.start()

root.mainloop()
