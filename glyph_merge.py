import fontforge
from pathlib import Path
import psMat

INPUT_FONT_PATH = Path("/usr/share/fonts/opentype/artemisia/GFSArtemisia.otf")
OUTPUT_FONT_PATH = Path.home() / ".fonts" / "GFSArtemisia.otf"


font = fontforge.open(str(INPUT_FONT_PATH))

layer_a = font["a"].layers[font["a"].activeLayer]
layer_b = font["b"].layers[font["b"].activeLayer]
layer_c = font["c"].layers[font["c"].activeLayer]
layer_d = font["d"].layers[font["d"].activeLayer]

layer_a.transform(psMat.translate(0, 400))
layer_b.transform(psMat.translate(0, -400))
layer_c.transform(psMat.translate(font["a"].width, 400))
layer_d.transform(psMat.translate(font["b"].width, -400))

font["c"].layers[font["c"].activeLayer] = layer_a + layer_b + layer_c + layer_d
font["c"].width = max(font["a"].width + font["c"].width, font["b"].width + font["d"].width)
font["c"].transform(psMat.scale(0.8))

font.generate(str(OUTPUT_FONT_PATH))
