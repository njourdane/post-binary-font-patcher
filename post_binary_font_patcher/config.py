from pathlib import Path

OUTPUT_FONT_DIR = Path.home() / ".fonts"
LIGATURES_PATH = Path(__file__).parent.parent / "ligatures.json"
GLYPH_SCALE = 0.89
VERTICAL_SPACING = 0.27
VERTICAL_OFFSET = 0.03

PREVIEW_OUTPUT_DIR = Path(__file__).parent.parent / 'output'
PREVIEW_SVG_PATH = PREVIEW_OUTPUT_DIR / 'preview.svg'
PREVIEW_PNG_PATH = PREVIEW_OUTPUT_DIR / 'preview.png'

PREVIEW_IMG_WIDTH = 300
PREVIEW_IMG_HEIGHT = 200
PREVIEW_FONT_SIZE = 40
