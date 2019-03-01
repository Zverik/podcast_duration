#!/usr/bin/env python3
import sys
import dutil

if len(sys.argv) < 2:
    print('Usage: {} <itunes_url> <yymmdd,yymmdd,...>'.format(sys.argv[0]))
    sys.exit(1)

data = dutil.download_data()
title = [p['title'] for p in data if 'itunes' in p and sys.argv[1] in p['itunes']][0]

lengths = dutil.read_lengths()
if title not in lengths:
    lengths[title] = {}
if 'byhand' not in lengths[title]:
    lengths[title]['byhand'] = {}
lengths[title]['byhand']['date'] = [(int(s[:2]), int(s[2:4]), int(s[4:]))
                                    for s in sys.argv[2].split(',') if s]
dutil.write_lengths(lengths)
