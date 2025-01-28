import fontforge

font_source = fontforge.open("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
font_source.selection.select(("ranges", None), "A", "Z")
font_source.copy()

font_new = fontforge.font()
font_new.selection.select(("ranges", None), "A", "Z")
font_new.paste()
font_new.fontname = "NewFont"
font_new.generate("./NewFont.ttf")
