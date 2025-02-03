from pathlib import Path
from tempfile import NamedTemporaryFile

from defcon import Font, Glyph
from ufo2ft import compileTTF, compileOTF
from fontTools.ttLib import TTFont
from fontTools.merge import Merger


input_font_path = Path("/usr/share/fonts/opentype/lobstertwo/LobsterTwo-Regular.otf")
output_font_path = Path.home() / ".fonts" / ("patched_" + input_font_path.name)

font = TTFont(input_font_path)

glyphs = font.getGlyphSet()

new_glyph = Glyph()
pen = new_glyph.getPen()

glyphs["e"].draw(pen)
glyphs["m"].draw(pen)

ufo = Font()
ufo.insertGlyph(new_glyph, "e_m")

xtf = compileTTF(ufo) if "glyf" in font else compileOTF(ufo)

merger = Merger()

with NamedTemporaryFile(delete=False) as tmp_file:
    xtf.save(tmp_file.name)

new_font = merger.merge([input_font_path, tmp_file.name])

new_font.save(output_font_path)
