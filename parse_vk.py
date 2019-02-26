#!/usr/bin/env python3
import json
import sys
import dutil

if len(sys.argv) < 2:
    print('Usage: {} <vk_url> <html>'.format(sys.argv[0]))
    sys.exit(1)

data = dutil.download_data()
title = [p['title'] for p in data if p.get('vk') == sys.argv[1]][0]

with open('rupodcast_lengths.json', 'r') as f:
    lengths = json.load(f)

with open(sys.argv[2], 'rb') as f:
    text = f.read()
m = dutil.EXTRACTORS['vk'][0].findall(text)
if m:
    if title not in lengths:
        lengths[title] = {}
    lengths[title]['vk'] = [float(g[0] or 0) * 60 + float(g[1]) + float(g[2]) / 60 for g in m]
    with open('rupodcast_lengths.json', 'w') as f:
        json.dump(lengths, f, ensure_ascii=False)
