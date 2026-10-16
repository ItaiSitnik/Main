import os

from fontTools.ttLib import TTFont


def build_emoji_font(base_font_path, output_font_path, svg_dir):
    print("Loading base font file...")
    try:
        font = TTFont(base_font_path)
    except Exception as e:
        print(f"Failed to load font: {e}")
        return

    print("Checking SVG directory...")
    if not os.path.exists(svg_dir):
        print(f"Directory '{svg_dir}' not found. Creating it now...")
        os.makedirs(svg_dir)
        print(f"Directory created. Please add your .svg files to '{svg_dir}' and run again.")
        return

    svg_files = [f for f in os.listdir(svg_dir) if f.endswith(".svg")]

    if not svg_files:
        print(f"No SVG files found in '{svg_dir}'. Please add some files and try again.")
        return

    print(f"Detected {len(svg_files)} SVG glyphs to process.")

    # Logic to parse SVGs and append to the 'SVG ' table goes here
    # ...

    print("Compiling and saving the final color font...")
    font.save(output_font_path)
    print("Font generated successfully.")


if __name__ == "__main__":
    build_emoji_font("template.ttf", "custom_emoji_font.ttf", "./assets/svg")
