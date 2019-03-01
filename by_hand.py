#!/usr/bin/env python3
import sys
import dutil

if len(sys.argv) < 2:
    print('Usage: {} <itunes_url> {<lengths>|yymmdd,yymmdd}'.format(sys.argv[0]))
    sys.exit(1)

data = dutil.download_data()
title = [p['title'] for p in data if 'itunes' in p and sys.argv[1] in p['itunes']][0]

lengths = dutil.read_lengths()
if title not in lengths:
    lengths[title] = {}
lengths[title]['byhand'] = dutil.parse_text('byhand', sys.argv[2])
dutil.write_lengths(lengths)
