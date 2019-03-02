#!/usr/bin/env python3
import sys
import dutil


def find_by_substr(data, tag, s):
    found = [p['title'] for p in data if tag in p and s in p[tag]]
    return None if not found else found[0]


if len(sys.argv) < 2:
    print('Usage: {} <itunes_url> {<lengths>|yymmdd,yymmdd}'.format(sys.argv[0]))
    sys.exit(1)

data = dutil.download_data()
title = (find_by_substr(data, 'itunes', sys.argv[1]) or
         find_by_substr(data, 'soundcloud', sys.argv[1]))
if not title:
    print('There is no such podcast')
    sys.exit(2)

lengths = dutil.read_lengths()
if title not in lengths:
    lengths[title] = {}
gen = dutil.parse_text('byhand', sys.argv[2])
if 'byhand' in lengths[title]:
    lengths[title]['byhand'].update(gen)
else:
    lengths[title]['byhand'] = gen
dutil.write_lengths(lengths)
