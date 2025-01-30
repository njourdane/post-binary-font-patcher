from pathlib import Path

OUTPUT_FONT_DIR = Path.home() / ".fonts"
LIGATURES_PATH = Path(__file__).parent.parent / "ligatures.json"
GLYPH_SCALE = 0.89
VERTICAL_SPACING = 0.27
VERTICAL_OFFSET = 0.03

PREVIEW_OUTPUT_DIR = Path(__file__).parent.parent / 'output'
PREVIEW_SVG_PATH = PREVIEW_OUTPUT_DIR / 'preview.svg'
PREVIEW_PNG_PATH = PREVIEW_OUTPUT_DIR / 'preview.png'

PREVIEW_IMG_WIDTH = 600
PREVIEW_IMG_HEIGHT = 400
PREVIEW_FONT_SIZE = 28

PREVIEW_TEXT = '''
Camille est un.e auteur.ice-compositeur.ice doué.e,
ses ami.e.s la.e trouvent rigolo.te mais parfois
vif.ve et franc.he.

Iel est amoureux.se comme un.e fo.u.lle d'un.e
enseignant.e-chercheur.se et ielles sont
tou.te.s deux rebel.le.s mais inclusif.ve.s.

Son.a fils.le est musicien.ne-intervenant.e,
ce.lle.ux des voisin.e.s sont coifeur.se.s, nous
sommes tou.te.s nombreux.se.s à penser que
ce sont des be.lle.aux humain.e.s.
'''
