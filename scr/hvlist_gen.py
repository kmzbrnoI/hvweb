#!/usr/bin/env python3

"""
This file generates a single html page with list of locomotives.
When no output file is defined, output is written to stdout.

Usage:
  hvlist_gen.py <hvlist_directory_path> [-o <output_filename>]
"""

import configparser
from docopt import docopt
from typing import Dict, TextIO
import glob
import sys

HV = Dict[str, str]
HVs = Dict[int, HV]

TEMPLATE_HV_FN = 'templates/hv.html'
TEMPLATE_INDEX_FN = 'templates/index.html'


def generate_hvs(index_t: TextIO, hv_t: TextIO, output: TextIO,
                 hvs: HVs) -> None:
    index_text = index_t.read()
    hv_text = hv_t.read()
    hvs_text = ''

    for addr, hv in sorted(hvs.items()):
        hv_text_spec = hv_text
        for key, val in hv.items():
            hv_text_spec = hv_text_spec.replace('{{' + key + '}}', val)
        hvs_text += hv_text_spec + '\n'

    output.write(index_text.replace('{{hvs}}', hvs_text))


if __name__ == '__main__':
    args = docopt(__doc__)

    output = (open(args['<output_filename>'], 'w', encoding='utf-8')
              if args['<output_filename>'] is not None else sys.stdout)

    hvs: HVs = {}
    for filename in glob.glob(args['<hvlist_directory_path>'] + '/*.2lok'):
        config = configparser.ConfigParser()
        config.read(filename, encoding='utf-8-sig')
        sections = config.sections()
        assert 'global' in sections
        assert config['global']['version'] == '2.0'
        sections.remove('global')

        for addr in sections:
            assert addr.isdecimal()
            hvs[int(addr)] = dict(config[addr])
            hvs[int(addr)]['adresa'] = addr

    with open(TEMPLATE_HV_FN, 'r', encoding='utf-8') as hv_t, \
            open(TEMPLATE_INDEX_FN, 'r', encoding='utf-8') as index_t:
        generate_hvs(index_t, hv_t, output, hvs)

    # ofn will be closed automatically here
