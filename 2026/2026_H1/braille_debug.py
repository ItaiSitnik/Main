import sys
from PIL import Image


def show_flattened_preview(image_path, target_width=28):
    """
    Resizes the image to the target width, converts to 1-bit black and white,
    and then scales it up for viewing on a monitor using Nearest Neighbor
    so the pixels remain sharp and blocky.
    """
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    # Calculate height maintaining aspect ratio
    w_percent = target_width / float(img.size[0])
    h_size = int((float(img.size[1]) * float(w_percent)))

    # 1. Resize to the actual small size (e.g., 28 pixels wide)
    # Using LANCZOS for high quality downsampling
    img_small = img.resize((target_width, h_size), Image.Resampling.LANCZOS)

    # 2. Convert to 1-bit black and white (Dithering)
    # This is exactly what the Braille script sees.
    img_bw = img_small.convert("1")

    # 3. Scale up for display (Visualization only)
    # We define a display width (e.g., 600px) to make it visible on screen
    display_scale = 20
    display_width = target_width * display_scale
    display_height = h_size * display_scale

    # Use NEAREST to keep the "pixelated" look
    img_preview = img_bw.resize((display_width, display_height), Image.Resampling.NEAREST)

    print(f"Original size: {img.size}")
    print(f"Processed size (internal): {target_width}x{h_size}")
    print("Opening preview window...")

    img_preview.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_view.py <path_to_image>")
    else:
        path = sys.argv[1]
        show_flattened_preview(path)
