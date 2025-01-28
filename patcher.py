# based on https://github.com/ToxicFrog/Ligaturizer/blob/master/ligaturize.py

import fontforge
import psMat
from pathlib import Path

INPUT_FONT_PATH = Path("/usr/share/fonts/truetype/comfortaa/Comfortaa-Regular.ttf")
FONT_NAME = 'A ligature test font'
OUTPUT_DIR = Path(__file__).parent / "output"

LIGATURES = [
    {
        'chars': ['o', 'e'],
        'ligature_name': 'oe',
    },
]

FEATURE_SCRIPT_LANG_TUPLE = (
    ('calt', (
        ('DFLT', ('dflt',)),
        ('arab', ('dflt',)),
        ('armn', ('dflt',)),
        ('cyrl', ('SRB ', 'dflt')),
        ('geor', ('dflt',)),
        ('grek', ('dflt',)),
        ('lao ', ('dflt',)),
        ('latn', ('CAT ', 'ESP ', 'GAL ', 'ISM ', 'KSM ', 'LSM ', 'MOL ', 'NSM ', 'ROM ', 'SKS ', 'SSM ', 'dflt')),
        ('math', ('dflt',)),
        ('thai', ('dflt',))
    )),
)


class LigatureCreator(object):
    def __init__(self, font_path, font_name, output_dir):
        self.font_path = font_path
        self.font_name = font_name
        self.output_dir = output_dir

        self.font = fontforge.open(str(self.font_path))
        self._lig_counter = 0

    def add_ligature(self, input_chars, ligature_name):
        self._lig_counter += 1

        lookup_name_tmpl = f'lookup.{ self._lig_counter }.%d'
        lookup_sub_name_tmpl = f'lookup.sub.{ self._lig_counter }.%d'
        cr_name_tmpl = f'CR.{ self._lig_counter }.%d'

        self.font.selection.none()
        self.font.selection.select(ligature_name)
        self.font.copy()

        self.font.createChar(-1, ligature_name)
        self.font.selection.none()
        self.font.selection.select(ligature_name)
        self.font.paste()
        self.font[ligature_name].transform(psMat.scale(0.5))

        self.font.selection.none()
        self.font.selection.select('space')
        self.font.copy()

        for i, char in enumerate(input_chars): # ["period", "e"]
            self.font.addLookup(lookup_name_tmpl % i, 'gsub_single', (), ())
            self.font.addLookupSubtable(lookup_name_tmpl % i, lookup_sub_name_tmpl % i)

            if i < len(input_chars) - 1:
                self.font.createChar(-1, cr_name_tmpl % i)
                self.font.selection.none()
                self.font.selection.select(cr_name_tmpl % i)
                self.font.paste()
                self.font[char].addPosSub(lookup_sub_name_tmpl % i, cr_name_tmpl % i)
            else:
                self.font[char].addPosSub(lookup_sub_name_tmpl % i, ligature_name)

        calt_lookup_name = f'calt.{ self._lig_counter }'
        self.font.addLookup(calt_lookup_name, 'gsub_contextchain', (), FEATURE_SCRIPT_LANG_TUPLE)

        print('CALT %s (%s)' % (calt_lookup_name, ligature_name))
        for i, char in enumerate(input_chars):
            prev = ' '.join(cr_name_tmpl % j for j in range(i))
            next = ' '.join(input_chars[i+1:])
            lookup = lookup_name_tmpl % i
            subtable_name = f'calt.{ self._lig_counter }.{ i }'
            rule = f'{ prev } | { char } @<{ lookup }> | { next }'
            print(subtable_name, ":", rule)
            self.font.addContextualSubtable(calt_lookup_name, subtable_name, 'glyph', rule)

    def replace_sfnt(self, key, value):
        self.font.sfnt_names = tuple(
            (row[0], key, value)
            if row[1] == key
            else row
            for row in self.font.sfnt_names
        )

    def update_font_metadata(self):
        old_name = self.font.familyname
        clean_name = self.font_name.replace(' ', '')
        suffix = (self.font.fontname.split('-', 1) + [''])[1]

        self.font.familyname = self.font_name
        self.font.fullname = "%s %s" % (self.font_name, suffix) if suffix else self.font_name
        self.font.fontname = "%s-%s" % (clean_name, suffix) if suffix else clean_name

        path_name = Path(self.font.path).name
        print(f"Ligaturizing font { path_name } ({ old_name }) as '{ self.font_name }'")

        # self.font.copyright = (self.font.copyright or '') + COPYRIGHT
        self.replace_sfnt('UniqueID', '%s; Ligaturized' % self.font.fullname)
        self.replace_sfnt('Preferred Family', self.font_name)
        self.replace_sfnt('Compatible Full', self.font_name)
        self.replace_sfnt('Family', self.font_name)
        self.replace_sfnt('WWS Family', self.font_name)

    def ligaturize_font(self):
        self.update_font_metadata()

        ligature_length = lambda lig: len(lig['chars'])
        for lig_spec in sorted(LIGATURES, key = ligature_length):
            try:
                self.add_ligature(lig_spec['chars'], lig_spec['ligature_name'])
            except Exception as e:
                print('Exception while adding ligature: {}'.format(lig_spec))
                raise

        # Work around a bug in Fontforge where the underline height is subtracted from
        # the underline width when you call generate().
        self.font.upos += self.font.uwidth

        output_font_type = '.otf' if self.font_path.suffix.lower() == '.otf' else '.ttf'
        output_font_file = self.output_dir / (self.font.fontname + output_font_type)
        print(f"saving to '{ output_font_file }' ({ self.font.fullname })")
        self.font.generate(str(output_font_file))


if __name__ == '__main__':
    ligature_creator = LigatureCreator(INPUT_FONT_PATH, FONT_NAME, OUTPUT_DIR)
    ligature_creator.ligaturize_font()
