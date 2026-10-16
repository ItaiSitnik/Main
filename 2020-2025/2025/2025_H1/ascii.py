from PIL import Image, ImageDraw, ImageFont

# Dense ASCII character set (from dark to light)
ASCII_CHARS = r"$@B%8&WM#*oahkbdpqwmZ0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "


def resize_image(image, new_width, font_aspect_ratio=0.55):
    """Resize image preserving aspect ratio and accounting for font height/width ratio."""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * font_aspect_ratio)
    return image.resize((new_width, new_height))


def to_grayscale(image):
    return image.convert("L")


def pixel_to_ascii(image):
    pixels = image.getdata()
    ascii_str = "".join(ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixels)
    return ascii_str


def ascii_to_image(ascii_str, width, font_path="C:/Windows/Fonts/consola.ttf", font_size=12, output_path="ascii_image.png"):
    lines = [ascii_str[i : i + width] for i in range(0, len(ascii_str), width)]

    font = ImageFont.truetype(font_path, font_size)
    bbox = font.getbbox("A")
    char_width = bbox[2] - bbox[0]
    char_height = bbox[3] - bbox[1]

    img_width = char_width * width
    img_height = char_height * len(lines)

    img = Image.new("RGB", (img_width, img_height), color="white")
    draw = ImageDraw.Draw(img)

    for i, line in enumerate(lines):
        draw.text((0, i * char_height), line, fill="black", font=font)

    img.save(output_path)
    print(f"✅ ASCII image saved to: {output_path}")


def image_to_ascii_image(path, new_width=100, font_path="C:/Windows/Fonts/consola.ttf", font_size=12, output_path="ascii_image.png"):
    try:
        image = Image.open(path)
    except Exception as e:
        print(f"❌ Unable to open image: {e}")
        return

    resized = resize_image(image, new_width)
    grayscale = to_grayscale(resized)
    ascii_str = pixel_to_ascii(grayscale)
    ascii_to_image(ascii_str, new_width, font_path, font_size, output_path)


# Example usage
if __name__ == "__main__":
    image_path = r"2025_H1\image.png"
    image_to_ascii_image(
        image_path, new_width=120, font_path="C:/Windows/Fonts/consola.ttf", font_size=10, output_path="2025_H1/ascii_image.png"
    )
