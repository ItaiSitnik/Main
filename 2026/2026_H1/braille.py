import sys
from PIL import Image

# Based on the string provided in the prompt, the width is 28 characters.
WHATSAPP_WIDTH = 28 * 5


def image_to_braille(image_path, width_chars=WHATSAPP_WIDTH, invert=False):
    """
    Converts an image to a Braille ASCII art string.

    Args:
        image_path (str): Path to the input image.
        width_chars (int): The width of the output in Braille characters.
        invert (bool): If True, inverts the colors (black becomes dots).
    """
    try:
        img = Image.open(image_path)
    except Exception as e:
        return f"Error opening image: {e}"

    # Braille characters are 2 dots wide by 4 dots high.
    # To maintain resolution, we map 1 char to a 2x4 pixel block.
    w_pixels = width_chars * 2

    # Calculate height maintaining aspect ratio
    orig_w, orig_h = img.size
    h_pixels = int((orig_h / orig_w) * w_pixels)

    # Ensure height is a multiple of 4 for clean chunking into Braille rows
    remainder = h_pixels % 4
    if remainder:
        h_pixels += 4 - remainder

    # Resize image
    img = img.resize((w_pixels, h_pixels), Image.Resampling.LANCZOS)

    # Convert to 1-bit black and white (uses dithering by default)
    img = img.convert("1")

    # Braille Unicode bit mapping (ISO 11548-1)
    # The dot pattern is:
    # 1 4
    # 2 5
    # 3 6
    # 7 8
    # Maps to hex values:
    dot_map = {(0, 0): 0x1, (1, 0): 0x8, (0, 1): 0x2, (1, 1): 0x10, (0, 2): 0x4, (1, 2): 0x20, (0, 3): 0x40, (1, 3): 0x80}

    pixels = img.load()
    result_lines = []

    # Iterate through the image in 2x4 blocks
    for y in range(0, h_pixels, 4):
        line = ""
        for x in range(0, w_pixels, 2):
            char_offset = 0

            # Check pixels within the 2x4 block
            for dy in range(4):
                for dx in range(2):
                    if x + dx < w_pixels and y + dy < h_pixels:
                        px = pixels[x + dx, y + dy]

                        # Logic: usually 255 is white (light) and 0 is black (dark).
                        # By default, we place a dot for light pixels (brightness).
                        # If 'invert' is True, we place dots for dark pixels (ink).
                        is_dot = px > 128 if not invert else px < 128

                        if is_dot:
                            char_offset += dot_map[(dx, dy)]

            # Base Braille Unicode is 0x2800 + the calculated offset
            line += chr(0x2800 + char_offset)
        result_lines.append(line)

    return "\n".join(result_lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python img_to_braille.py <path_to_image>")
        print("Example: python img_to_braille.py my_photo.jpg")
    else:
        # Get image path from command line arguments
        img_path = sys.argv[1]

        # Generate and print result
        # You can toggle invert=True if the result looks like a negative
        art = image_to_braille(img_path, invert=True)
        print(art)

        print("\n" + "=" * WHATSAPP_WIDTH + "\n")

        art = image_to_braille(img_path, invert=False)
        print(art)
