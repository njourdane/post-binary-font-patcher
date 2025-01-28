"""
Utility script that:
1. Build a svg file containing a text;
2. Copy font file to user font dir;
3. Convert the svg to png with Inkscape.
Note: cairosvg does not support ligatures but Inkscape does, hence the system call.
"""

from pathlib import Path
import subprocess


FONT_DIR = Path.home() / '.fonts'
OUTPUT_DIR = Path('./output')

SVG_PATH = OUTPUT_DIR / 'preview.svg'
PNG_PATH = OUTPUT_DIR / 'preview.png'
FONT_PATH = OUTPUT_DIR / 'Aligaturetestfont-Regular.ttf'
FONT_NAME = "A ligature test font"
TEXT = "Elle est doué.e !"
WIDTH, HEIGHT = 600, 400


CSS = f'''
text {{
    font-family: "{ FONT_NAME }";
    text-anchor: middle;
    alignment-baseline: middle;
    fill: darkslategrey;
    font-size: 60;
}}
'''

SVG_PREFIX = f'''<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{ WIDTH }" height="{ HEIGHT }">
<style>\n{ CSS }</style>\n
'''

SVG_SUFFIX = '''
</svg>
'''

CMD = f"inkscape { SVG_PATH } --export-filename={ PNG_PATH }"

svg = f'<text x="{ WIDTH/2 }px" y="{ HEIGHT/2 }px">{ TEXT }</text>'

SVG_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(SVG_PATH, 'w', encoding='utf-8') as svg_file:
    svg_file.write(f'{ SVG_PREFIX }{ svg }{ SVG_SUFFIX }')

(FONT_DIR / FONT_PATH.name).write_bytes(FONT_PATH.read_bytes())
subprocess.call(CMD, shell=True)
