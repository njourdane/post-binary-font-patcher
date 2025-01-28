#!/usr/bin/env python

import fontforge
from pathlib import Path


class LigatureCreator(object):

    def __init__(self, font_base, font_pick):
        self.font_base = font_base
        self.font_pick = font_pick

        self._lig_counter = 0

    def add_ligature(self, input_chars, ligature_name):
        self._lig_counter += 1

        self.font_base.createChar(-1, ligature_name)
        font_pick.selection.none()
        font_pick.selection.select(ligature_name)
        font_pick.copy()
        self.font_base.selection.none()
        self.font_base.selection.select(ligature_name)
        self.font_base.paste()

        self.font_base.selection.none()
        self.font_base.selection.select('space')
        self.font_base.copy()

        lookup_name = lambda i: 'lookup.{}.{}'.format(self._lig_counter, i)
        lookup_sub_name = lambda i: 'lookup.sub.{}.{}'.format(self._lig_counter, i)
        cr_name = lambda i: 'CR.{}.{}'.format(self._lig_counter, i)

        for i, char in enumerate(input_chars):
            self.font_base.addLookup(lookup_name(i), 'gsub_single', (), ())
            self.font_base.addLookupSubtable(lookup_name(i), lookup_sub_name(i))

            if i < len(input_chars) - 1:
                self.font_base.createChar(-1, cr_name(i))
                self.font_base.selection.none()
                self.font_base.selection.select(cr_name(i))
                self.font_base.paste()

                self.font_base[char].addPosSub(lookup_sub_name(i), cr_name(i))
            else:
                self.font_base[char].addPosSub(lookup_sub_name(i), ligature_name)


        calt_lookup_name = 'calt.{}'.format(self._lig_counter)
        self.font_base.addLookup(calt_lookup_name, 'gsub_contextchain', (), (('calt', (('DFLT', ('dflt',)), ('arab', ('dflt',)), ('armn', ('dflt',)), ('cyrl', ('SRB ', 'dflt')), ('geor', ('dflt',)), ('grek', ('dflt',)), ('lao ', ('dflt',)), ('latn', ('CAT ', 'ESP ', 'GAL ', 'ISM ', 'KSM ', 'LSM ', 'MOL ', 'NSM ', 'ROM ', 'SKS ', 'SSM ', 'dflt')), ('math', ('dflt',)), ('thai', ('dflt',)))),))
        for i, char in enumerate(input_chars):
            ctx_subtable_name = 'calt.{}.{}'.format(self._lig_counter, i)
            ctx_spec = '{prev} | {cur} @<{lookup}> | {next}'.format(
                prev = ' '.join(cr_name(j) for j in range(i)),
                cur = char,
                lookup = lookup_name(i),
                next = ' '.join(input_chars[i+1:]),
            )
            self.font_base.addContextualSubtable(calt_lookup_name, ctx_subtable_name, 'glyph', ctx_spec)


def change_font_names(font, fontname, fullname, familyname, copyright_add, unique_id):
    font.fontname = fontname
    font.fullname = fullname
    font.familyname = familyname
    font.copyright += copyright_add
    font.sfnt_names = tuple(
        (row[0], 'UniqueID', unique_id) if row[1] == 'UniqueID' else row
        for row in font.sfnt_names
    )


FONT_NAME = "MyFont"
FONT_FULL_NAME = "My Font"

FONT_BASE_PATH = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
FONT_PICK_PATH = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
FONT_DEST_PATH = Path("./my_font.ttf")

font_base = fontforge.open(str(FONT_BASE_PATH))
font_pick = fontforge.open(str(FONT_PICK_PATH))

font_base.em = font_pick.em

creator = LigatureCreator(font_base, font_pick)

ligatures = [{
    'chars': ['o', 'e'],
    'ligature_name': 'oe',
}]

for lig_spec in sorted(ligatures, key = lambda lig: len(lig['chars'])):
    try:
        creator.add_ligature(lig_spec['chars'], lig_spec['ligature_name'])
    except Exception as e:
        print('Exception while adding ligature: {}'.format(lig_spec))
        raise

change_font_names(font_base, FONT_NAME,
                        FONT_FULL_NAME,
                        FONT_FULL_NAME,
                        "\ntest",
                        FONT_FULL_NAME)

font_base.generate(str(FONT_DEST_PATH))
