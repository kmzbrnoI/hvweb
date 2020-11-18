#!/usr/bin/env python3

"""
This file generates a single html page with list of locomotives.
When no output file is defined, output is written to stdout.

Usage:
  hvlist_gen.py <hvlist_directory_path> [-o <output_filename>]
"""

import configparser
from docopt import docopt
from typing import Dict, List, TextIO
import glob
import sys
import datetime
import subprocess

HV = Dict[str, str]
HVs = Dict[int, HV]

TEMPLATE_HV_FN = 'templates/hv.html'
TEMPLATE_INDEX_FN = 'templates/index.html'

HV_CLASS_CAR = 4


def generate_owners(hvs: HVs) -> str:
    owners: Dict[str, List[HV]] = {}
    for hv in hvs.values():
        if hv['majitel'] not in owners:
            owners[hv['majitel']] = []
        owners[hv['majitel']].append(hv)

    result = ''
    own_sorted = sorted(owners.items(),
                        key=lambda owner_hvs: -len(owner_hvs[1]))
    for owner, hvs in own_sorted:
        result += f'<li>{owner}: {len(hvs)}</li>\n'

    return result


def git_head_id(path: str = '.') -> str:
    return subprocess.check_output(
        ['git', 'rev-parse', '--short', 'HEAD'], cwd=path,
    ).strip().decode('utf-8')


def generate_hvs(index_t: TextIO, hv_t: TextIO, output: TextIO,
                 hvs: HVs, hvlist_path: str) -> None:
    index_text = index_t.read()
    hv_text = hv_t.read()
    hvs_text = ''

    for addr, hv in sorted(hvs.items()):
        hv_text_spec = hv_text
        for key, val in hv.items():
            hv_text_spec = hv_text_spec.replace('{{' + key + '}}', val)
        if hv['trida'] == HV_CLASS_CAR:
            class_ = 'car'
        else:
            class_ = ''
        hv_text_spec = hv_text_spec.replace('{{trclass}}', class_)
        hvs_text += hv_text_spec + '\n'

    index_text = index_text.replace('{{total}}', str(len(hvs)))
    index_text = index_text.replace(
        '{{last_updated}}',
        datetime.datetime.now().strftime("%-d. %-m. %Y %H:%M")
    )

    index_text = index_text.replace('{{git_head_db}}',
                                    git_head_id(hvlist_path))
    index_text = index_text.replace('{{git_head_web}}', git_head_id())

    index_text = index_text.replace('{{owners}}', generate_owners(hvs))

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
        assert 'global' in sections, f'{filename}'
        assert config['global']['version'] == '2.0', f'{filename}'
        sections.remove('global')

        for addr in sections:
            assert addr.isdecimal()
            hvs[int(addr)] = dict(config[addr])
            hvs[int(addr)]['adresa'] = addr

    with open(TEMPLATE_HV_FN, 'r', encoding='utf-8') as hv_t, \
            open(TEMPLATE_INDEX_FN, 'r', encoding='utf-8') as index_t:
        generate_hvs(
            index_t, hv_t, output, hvs, args['<hvlist_directory_path>']
        )

    # ofn will be closed automatically here
