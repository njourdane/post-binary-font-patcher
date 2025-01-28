import fontforge
import psMat

print("Importing font...")
font_source = fontforge.open("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
font_source.selection.select(("ranges", None), "A", "Z")
font_source.copy()

print("Generating new font...")
font_new = fontforge.font()
font_new.selection.select(("ranges", None), "A", "Z")
font_new.paste()
# font_new.addExtrema()

font_new.selection.select(("ranges", None), "A", "D")
font_new.transform(psMat.scale(0.5))

font_new.fontname = "NewFont"

font_new.generate("./NewFont.ttf")
