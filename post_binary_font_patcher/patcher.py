import json
from pathlib import Path

import fontforge
import psMat

from . import config


class FontPatcher:
    def __init__(self, font_path: Path):
        self.font_path = font_path
        self.font = fontforge.open(str(font_path))

        self.ligatures_path = config.LIGATURES_PATH
        self.glyph_scale = config.GLYPH_SCALE

        self.v_spacing = self.font.em * config.VERTICAL_SPACING
        self.v_offset = self.font.em * config.VERTICAL_OFFSET
        self.feature_script_lang = (("liga", (("latn", ("dflt")),)),)
        self.output_font_path = config.OUTPUT_FONT_DIR / self.font_path.name

    def build_layer(self, chars: list[str], x_offset: int, y_offset: int, scale: float):
        x_rel_offset = 0
        layer = fontforge.layer()
        for char in chars:
            char_layer = self.font[char].layers[self.font[char].activeLayer]
            char_layer.transform(psMat.translate(x_offset + x_rel_offset, y_offset))
            layer += char_layer
            x_rel_offset += self.font[char].width

        layer.transform(psMat.scale(scale))
        return layer, int(x_rel_offset * scale)

    def build_liga_glyph(self, name: str, base_chars: list[str], bottom_chars: list[str], top_chars: list[str]):
        layer_base, base_width = self.build_layer(base_chars, 0, 0, 1)
        layer_top, top_width = self.build_layer(top_chars, base_width, self.v_offset + self.v_spacing, self.glyph_scale)
        layer_btm, btm_width = self.build_layer(bottom_chars, base_width, self.v_offset - self.v_spacing, self.glyph_scale)

        self.font.createChar(-1, name)
        self.font[name].layers[self.font[name].activeLayer] = layer_base + layer_top + layer_btm
        self.font[name].width = base_width + max(top_width, btm_width)

    def get_chars(self, text):
        return ["period" if char == "." else char for char in text]

    def add_ligature(self, pattern: str, base: str, bottom_text: str, top_text: str):
        name = pattern.replace('.', '_')
        self.build_liga_glyph(name, self.get_chars(base), self.get_chars(bottom_text), self.get_chars(top_text))
        self.font[name].addPosSub("liga", self.get_chars(pattern))

    def build_font(self):
        self.font.addLookup('liga', 'gsub_ligature', (), self.feature_script_lang)
        self.font.addLookupSubtable('liga', 'liga')

        with open(self.ligatures_path) as ligatures_file:
            ligatures = json.loads(ligatures_file.read())

        for pattern, base, bottom_text, top_text in ligatures:
            self.add_ligature(pattern, base, bottom_text, top_text)

        self.font.generate(str(self.output_font_path))
        print(f"Font generated in { self.output_font_path }")
