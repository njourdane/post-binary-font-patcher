"""
Utility script that:
1. Build a svg file containing a text using the font;
2. Convert the svg to png with Inkscape.
Note: cairosvg does not support ligatures but Inkscape does,
hence the system call.
"""

import subprocess

from . import config


class Previewer:
    def __init__(self, font_name: str, text: str) -> None:
        self.font_name = font_name
        self.text = text

        self.svg_path = config.PREVIEW_SVG_PATH
        self.png_path = config.PREVIEW_PNG_PATH
        self.font_size = config.PREVIEW_FONT_SIZE
        self.img_width = config.PREVIEW_IMG_WIDTH
        self.img_height = config.PREVIEW_IMG_HEIGHT

        self.svg_prefix = self.get_svg_prefix()
        self.svg_suffix = '</svg>'
        self.cmd_rasterize = f"inkscape { self.svg_path } --export-filename={ self.png_path }"

    def get_css(self):
        return f'''
text {{
    font-family: "{ self.font_name }";
    text-anchor: middle;
    alignment-baseline: middle;
    fill: darkslategrey;
    font-size: { self.font_size };
}}

rect {{
    fill: grey;
}}
'''

    def get_svg_prefix(self):
        return f'''<?xml version="1.0" encoding="utf-8"?>
<svg
        xmlns="http://www.w3.org/2000/svg"
        width="{ self.img_width }"
        height="{ self.img_height }">
    <style>\n{ self.get_css() }</style>
'''

    def draw_background(self):
        return f'''
    <rect
        x="0"
        y="0"
        width="{ self.img_width }"
        height="{ self.img_height }"
    />
'''

    def draw_text(self) -> str:
        svg = ''
        subtexts = self.text.split("|")
        for idx, subtext in enumerate(subtexts):
            height = idx * self.font_size * 1.1 + self.img_height / (len(subtexts) + 0.5)
            svg += f'<text x="{ self.img_width / 2 }px" y="{ height }px">{ subtext }</text>\n'
        return svg

    def build_svg_file(self):
        self.svg_path.parent.mkdir(parents=True, exist_ok=True)
        svg = f'{ self.svg_prefix }{ self.draw_background() }{ self.draw_text() }{ self.svg_suffix }'

        with open(self.svg_path, 'w', encoding='utf-8') as svg_file:
            svg_file.write(svg)

        print(f"Preview svg image generated in { self.svg_path }")

    def rasterize_svg(self):
        subprocess.call(self.cmd_rasterize, shell=True)
        print(f"Preview png image generated in { self.png_path }")
