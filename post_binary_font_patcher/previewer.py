"""
Utility script that:
1. Build a svg file containing a text using the font;
2. Convert the svg to png with Inkscape.
Note: cairosvg does not support ligatures but Inkscape does,
hence the system call.
"""

from sys import argv, exit
from pathlib import Path
import subprocess


class Previewer:
    def __init__(self, font_name: str, text: str) -> None:
        self.font_name = font_name
        self.text = text

        preview_output_dir = Path(__file__).parent.parent / 'output'

        self.svg_path = preview_output_dir / 'preview.svg'
        self.png_path = preview_output_dir / 'preview.png'
        self.font_size = 40
        self.img_width = 300
        self.img_height = 200

        self.svg_prefix = self.get_svg_prefix()
        self.svg_suffix = '</svg>'
        self.cmd_rasterize = f"inkscape { self.svg_path } --export-filename={ self.png_path }"

    def get_css(self):
        return f'''text {{
    font-family: "{ self.font_name }";
    text-anchor: middle;
    alignment-baseline: middle;
    fill: darkslategrey;
    font-size: { self.font_size };
}}'''

    def get_svg_prefix(self):
        return f'''<?xml version="1.0" encoding="utf-8"?>
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="{ self.img_width }"
            height="{ self.img_height }">
        <style>\n{ self.get_css() }</style>\n'''

    def get_svg(self) -> str:
        svg = ''
        subtexts = self.text.split("|")
        for idx, subtext in enumerate(subtexts):
            height = idx * self.font_size * 1.1 + self.img_height / (len(subtexts) + 0.5)
            svg += f'<text x="{ self.img_width / 2 }px" y="{ height }px">{ subtext }</text>\n'
        return svg

    def build_svg_file(self):
        svg = self.get_svg()
        self.svg_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.svg_path, 'w', encoding='utf-8') as svg_file:
            svg_file.write(f'{ self.svg_prefix }{ svg }{ self.svg_suffix }')

        print(f"Preview svg image generated in { self.svg_path }")

    def rasterize_svg(self):
        subprocess.call(self.cmd_rasterize, shell=True)
        print(f"Preview png image generated in { self.svg_path }")


if __name__ == "__main__":
    if len(argv) != 3:
        print(f'usage: { argv[0] } <font name> <preview text>')
        print(f'example: { argv[0] } "GFS Artemisia" "Hello|world"')
        exit(1)

    previewer = Previewer(argv[1], argv[2])
    previewer.build_svg_file()
    previewer.rasterize_svg()
