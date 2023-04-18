#!/usr/bin/env python3

"""
This file generates a single html page with list of users.
When no output file is defined, output is written to stdout.

Usage:
  usess_gen.py <users_ini_filename> [-o <output_filename>]
"""

import configparser
from docopt import docopt
from typing import List, Dict
import sys
import datetime
import subprocess
import codecs
import os

TEMPLATE_INDEX_FN = 'templates/users.html'


def encoding_bom(filename: str) -> str:
    bytes_ = min(32, os.path.getsize(filename))
    with open(filename, 'rb') as f:
        raw = f.read(bytes_)
    return 'utf-8-sig' if raw.startswith(codecs.BOM_UTF8) else 'utf-8'


def git_head_id(path: str = '.') -> str:
    return subprocess.check_output(
        ['git', 'rev-parse', '--short', 'HEAD'], cwd=path,
    ).strip().decode('utf-8')


def areas(config) -> List[str]:
    result = set()
    for user in config.sections():
        if 'ORs' in config[user]:
            areas = config[user]['ORs'].replace(')', '').split('(')
            for area in areas:
                splitted = area.split(',')
                if len(splitted) == 2:
                    result.add(splitted[0])
    return sorted(result)


def user(user: Dict[str, str], output, areas) -> str:
    result = '<tr>\n'
    result += f'<td>{user.name}</td>\n'
    result += f'<td>{user.get("fname", "")} {user.get("lname", "")}</td>\n'
    if user.get('reg', '0') == '1':
        result += '<td class="wr center">ano</td>\n'
    else:
        result += '<td class="center">ne</td>\n'
    result += f'<td class="center">{"ano" if user.get("ban", "0") == "1" else "ne"}</td>\n'

    rights = {}
    if 'ORs' in user:
        _areas = user['ORs'].replace(')', '').split('(')
        for area in _areas:
            splitted = area.split(',')
            if len(splitted) == 2:
                rights[splitted[0]] = int(splitted[1])

    for area_id in areas:
        if area_id in rights:
            if rights[area_id] == 1:
                result += '<td class="center">R'
            elif rights[area_id] == 2:
                result += '<td class="center wr">W'
            else:
                result += '<td class="center">'+str(rights[area_id])
        else:
            result += '<td>'
        result += '</td>\n'

    result += '</tr>\n'
    return result


if __name__ == '__main__':
    args = docopt(__doc__)

    output = (open(args['<output_filename>'], 'w', encoding='utf-8')
              if args['<output_filename>'] is not None else sys.stdout)

    ini_filename = args['<users_ini_filename>']
    config = configparser.ConfigParser()
    config.read(ini_filename, encoding=encoding_bom(ini_filename))

    content = ''
    area_ids = areas(config)
    content += '<table>\n<tr>\n'
    content += '<th>Uživatelské jméno</th>\n'
    content += '<th>Jméno</th>\n'
    content += '<th>Ruční řízení</th>\n'
    content += '<th>Ban</th>\n'
    for area_id in area_ids:
        content += f'<th>{area_id}</th>'

    for user_id in config.sections():
        content += user(config[user_id], output, area_ids)

    content += '</tr>\n</table>\n'

    with open(TEMPLATE_INDEX_FN, 'r', encoding='utf-8') as index_t:
        template = index_t.read()

    template = template.replace('{{users_table}}', content)
    template = template.replace(
        '{{last_updated}}',
        datetime.datetime.now().strftime("%-d. %-m. %Y %H:%M")
    )
    template = template.replace('{{git_head_db}}',
                                git_head_id(os.path.dirname(ini_filename)))
    template = template.replace('{{git_head_web}}', git_head_id())
    template = template.replace('{{total}}', str(len(config.sections())))
    output.write(template)

    # ofn will be closed automatically here
