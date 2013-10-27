'''
LightYear CSS
Dale Bustad <dale@divmain.com>

Usage:
  lightyear [options] [-v | --vendorize TARGET] FILE... [--out DIR | --stdout]
  lightyear (-h | --help)
  lightyear --version

Alternate:
  python -m lightyear FILE... [--out DIR | --stdout]

Options:
  FILE          LightYear file (.lyc) to convert to CSS.
  --out DIR     Path to put CSS files.
  --stdout      Write results to STDOUT.

  -p            Prettify CSS output
  -d            Include original line numbers in outputted CSS for debugging.
  -r            Reduce and consolidate rules with identical selectors into
                single rules.

  -v                Apply vendor prefixes to CSS output via prefixr.com API.
                    Default is offline method.
  --vendorize       Alternate vendor prefix method.
                    Options: online, offline, prefixr

  --target TARGET   Specify browser targets for vendor prefixes.
                    Example: ie=9;firefox=22;chrome=24;safari=5
                    Default: ie=10;firefox=20;chrome=26;safari=5

  -h --help     Show this screen.
  --version     Show version.
'''

import os
import sys
from glob import glob

from docopt import docopt

from . import LY


def main(argv):
    args = docopt(__doc__, argv, version='0.1.0')

    files = []
    for file_group in args['FILE']:
        files_in_group = glob(file_group)
        if not files_in_group:
            raise OSError('File not found: {}'.format(file_group))
        files.extend(files_in_group)

    vendorize = ('prefixr' if args['-v']
                 else args['--vendorize'] if args['--vendorize']
                 else False)

    for f in files:
        abspath = os.path.dirname(os.path.abspath(f))
        in_name = os.path.basename(f)
        out_name = '.'.join(in_name.split('.')[:-1]) + '.css'
        css = get_css(
            source=load(f),
            debug=args['-d'],
            prettify=args['-p'],
            reduc=args['-r'],
            path=abspath,
            vendorize=vendorize)

        if args['--out']:
            outdir = os.path.abspath(args['--out'])
            save(css, os.path.join(outdir, out_name))
        else:
            print(css)
            if not len(files) == 1:
                print(chr(0), end='')

    return True


def get_css(source, debug, prettify, reduc, path, vendorize):
    ly = LY(debug=debug, path=path, vendorize=vendorize)
    ly.eval(source)
    if reduc:
        ly.reduce()
    if prettify:
        return ly.pretty_css()
    else:
        return ly.css()


def load(filepath):
    with open(filepath, 'r') as f:
        source = f.read()
    return source


def save(css, out_fpath):
    with open(out_fpath, 'w') as f:
        f.write(css)


sys.exit(main(sys.argv[1:]))
