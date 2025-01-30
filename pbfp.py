#!/usr/bin/env python

from sys import argv, exit
from pathlib import Path

from post_binary_font_patcher.patcher import FontPatcher
from post_binary_font_patcher.previewer import Previewer

USAGE = 'Available commands: patch, preview, help'


def print_patch_usage():
    print(f'usage: { argv[0] } <font path>')
    print(f'example: { argv[0] } /usr/share/fonts/opentype/artemisia/GFSArtemisia.otf')


def print_preview_usage():
    print(f'usage: { argv[0] } <font name>')
    print(f'example: { argv[0] } "GFS Artemisia"')


def main():
    if len(argv) == 1:
        print(USAGE)
        exit(1)

    command = argv[1]

    if command == "patch":
        if len(argv) != 3:
            print_patch_usage()
            exit(1)

        font_patcher = FontPatcher(Path(argv[2]))
        font_patcher.build_font()

    elif command == "preview":
        if len(argv) != 3:
            print_preview_usage()
            exit(1)

        previewer = Previewer(argv[2])
        previewer.build_svg_file()
        previewer.rasterize_svg()

    elif command == "help":
        print("PATCH")
        print_patch_usage()
        print("PREVIEW")
        print_preview_usage()

    else:
        print(USAGE)
        exit(1)

if __name__ == "__main__":
    main()
