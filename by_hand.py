#!/usr/bin/env python3
import sys
import dutil

if len(sys.argv) < 2:
    print('Usage: {} <itunes_url> <lengths>'.format(sys.argv[0]))
    sys.exit(1)

data = dutil.download_data()
title = [p['title'] for p in data if 'itunes' in p and sys.argv[1] in p['itunes']][0]

lengths = dutil.read_lengths()
if title not in lengths:
    lengths[title] = {}
lengths[title]['byhand'] = [float(p) for p in sys.argv[2].split(',') if p]
dutil.write_lengths(lengths)
