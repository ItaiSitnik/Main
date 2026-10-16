import os

from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables.S_V_G_ import Document


def inject_svg_to_font(base_font_path, output_font_path, svg_dir):
    print("Loading base font file...")
    try:
        font = TTFont(base_font_path)
    except Exception as e:
        print(f"Failed to load font: {e}")
        return

    if "SVG " not in font:
        print("Creating new SVG table in font...")
        font["SVG "] = newTable("SVG ")
        font["SVG "].docList = []

    svg_table = font["SVG "]
    glyph_order = font.getGlyphOrder()

    injected_count = 0

    for glyph_name in glyph_order:
        if glyph_name == ".notdef":
            continue

        svg_path = os.path.join(svg_dir, f"{glyph_name}.svg")

        if os.path.exists(svg_path):
            print(f"Injecting {glyph_name}.svg into glyph '{glyph_name}'...")
            with open(svg_path, "r", encoding="utf-8") as f:
                svg_data = f.read()

            glyph_id = font.getGlyphID(glyph_name)

            svg_doc = Document(svg_data, glyph_id, glyph_id)
            svg_table.docList.append(svg_doc)
            injected_count += 1
        else:
            print(f"Warning: {glyph_name}.svg not found in {svg_dir}, skipping.")

    if injected_count > 0:
        print("Compiling and saving the final color font...")
        font.save(output_font_path)
        print(f"Success! Font saved to {output_font_path} with {injected_count} SVGs.")
    else:
        print("No SVGs were injected. Output file was not generated.")


if __name__ == "__main__":
    inject_svg_to_font("template.ttf", "custom_emoji_font_final.ttf", "./assets/svg")
