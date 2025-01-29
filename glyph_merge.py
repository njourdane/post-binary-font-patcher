import fontforge
from pathlib import Path
import psMat
import json

INPUT_FONT_PATH = Path("/usr/share/fonts/opentype/artemisia/GFSArtemisia.otf")
OUTPUT_FONT_PATH = Path.home() / ".fonts" / "GFSArtemisia.otf"
LIGATURES_PATH = Path(__file__).parent / "ligatures.json"

GLYPH_SCALE = 0.8
VERTICAL_TRANSLATE_RATIO = 0.35
VERTICAL_OFFSET_RATIO = 0.15

font = fontforge.open(str(INPUT_FONT_PATH))
vmove_ratio = font.em * VERTICAL_TRANSLATE_RATIO
voffset_ratio = font.em * VERTICAL_OFFSET_RATIO
feature_script_lang = (("liga", (("latn", ("dflt")),)),)


def build_layer(chars: list[str], y_offset):
    x_offset = 0
    layer = fontforge.layer()
    for char in chars:
        char_layer = font[char].layers[font[char].activeLayer]
        char_layer.transform(psMat.translate(x_offset, y_offset))
        layer += char_layer
        x_offset += font[char].width
    return layer, x_offset


def build_multi_glyph(name: str, bottom_chars: list[str], top_chars: list[str]):
    layer_top, top_width = build_layer(top_chars, voffset_ratio + vmove_ratio)
    layer_btm, btm_width = build_layer(bottom_chars, voffset_ratio - vmove_ratio)

    font.createChar(-1, name)
    font[name].layers[font[name].activeLayer] = layer_top + layer_btm
    font[name].width = max(top_width, btm_width)
    font[name].transform(psMat.scale(GLYPH_SCALE))


def get_chars(text):
    return ["period" if char == "." else char for char in text]


def add_ligature(pattern: str, bottom_text: str, top_text: str):
    name = pattern.replace('.', '_')
    build_multi_glyph(name, get_chars(bottom_text), get_chars(top_text))
    font[name].addPosSub("liga", get_chars(pattern))


def build_font():
    font.addLookup('liga', 'gsub_ligature', (), feature_script_lang)
    font.addLookupSubtable('liga', 'liga')

    with open(LIGATURES_PATH) as ligatures_file:
        ligatures = json.loads(ligatures_file.read())

    for pattern, bottom_text, top_text in ligatures:
        add_ligature(pattern, bottom_text, top_text)

    font.generate(str(OUTPUT_FONT_PATH))


if __name__ == "__main__":
    build_font()
