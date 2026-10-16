from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib.tables._g_l_y_f import Glyph


def generate_base_ttf(output_filepath):
    print("Initializing FontBuilder...")
    builder = FontBuilder(unitsPerEm=1024, isTTF=True)

    glyph_order = [".notdef", "A", "B", "C"]
    builder.setupGlyphOrder(glyph_order)

    char_map = {65: "A", 66: "B", 67: "C"}
    builder.setupCharacterMap(char_map)

    empty_glyphs = {glyph_name: Glyph() for glyph_name in glyph_order}
    builder.setupGlyf(empty_glyphs)

    metrics = {glyph_name: (1024, 0) for glyph_name in glyph_order}
    builder.setupHorizontalMetrics(metrics)

    builder.setupHorizontalHeader(ascent=800, descent=-224)

    name_table_data = {
        "familyName": "EmojiTemplate",
        "styleName": "Regular",
        "uniqueFontIdentifier": "EmojiTemplate:Regular",
        "fullName": "EmojiTemplate Regular",
        "version": "Version 1.0",
        "psName": "EmojiTemplate-Regular",
    }
    builder.setupNameTable(name_table_data)

    builder.setupOS2(sTypoAscender=800, sTypoDescender=-224)
    builder.setupPost()

    builder.save(output_filepath)
    print(f"Success: Base template saved to {output_filepath}")


if __name__ == "__main__":
    generate_base_ttf("template.ttf")
