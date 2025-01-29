"""
Utility script that:
1. Build a svg file containing a text using the font;
2. Convert the svg to png with Inkscape.
Note: cairosvg does not support ligatures but Inkscape does,
hence the system call.
"""

from pathlib import Path
import subprocess
from sys import argv, exit


if len(argv) != 3:
    print(f'usage: { argv[0] } <font name> <preview text>')
    print(f'example: { argv[0] } "GFS Artemisia" "Hello|world"')
    exit(1)

font_name = argv[1]
text = argv[2]


FONT_DIR = Path.home() / '.fonts'
OUTPUT_DIR = Path('./output')

SVG_PATH = OUTPUT_DIR / 'preview.svg'
PNG_PATH = OUTPUT_DIR / 'preview.png'

WIDTH, HEIGHT = 300, 200
FONT_SIZE = 40

CSS = f'''
text {{
    font-family: "{ font_name }";
    text-anchor: middle;
    alignment-baseline: middle;
    fill: darkslategrey;
    font-size: { FONT_SIZE };
}}
'''

SVG_PREFIX = f'''<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{ WIDTH }" height="{ HEIGHT }">
<style>\n{ CSS }</style>\n
'''

SVG_SUFFIX = '''
</svg>
'''

CMD_RASTERIZE = f"inkscape { SVG_PATH } --export-filename={ PNG_PATH }"

svg = ''
subtexts = text.split("|")
for idx, subtext in enumerate(subtexts):
    height = idx * FONT_SIZE * 1.1 + HEIGHT / (len(subtexts) + 0.5)
    svg += f'<text x="{ WIDTH/2 }px" y="{ height }px">{ subtext }</text>\n'

SVG_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(SVG_PATH, 'w', encoding='utf-8') as svg_file:
    svg_file.write(f'{ SVG_PREFIX }{ svg }{ SVG_SUFFIX }')

subprocess.call(CMD_RASTERIZE, shell=True)
