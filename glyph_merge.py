import fontforge
from pathlib import Path
import psMat

INPUT_FONT_PATH = Path("/usr/share/fonts/opentype/artemisia/GFSArtemisia.otf")
OUTPUT_FONT_PATH = Path.home() / ".fonts" / "GFSArtemisia.otf"


font = fontforge.open(str(INPUT_FONT_PATH))

layer_a = font["a"].layers[font["a"].activeLayer]
layer_a.transform(psMat.translate(0, 400))

layer_b = font["b"].layers[font["b"].activeLayer]
layer_b.transform(psMat.translate(0, -400))

font["c"].layers[font["c"].activeLayer] = layer_a + layer_b

font.generate(str(OUTPUT_FONT_PATH))
