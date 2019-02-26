#!/usr/bin/env python3
import json
import requests
import sys

if len(sys.argv) < 2:
    print('Usage: {} <itunes_url> <lengths>'.format(sys.argv[0]))
    sys.exit(1)

resp = requests.get('https://russiancast.club/data.json')
data = resp.json()
title = [p['title'] for p in data if 'itunes' in p and sys.argv[1] in p['itunes']][0]

with open('rupodcast_lengths.json', 'r') as f:
    lengths = json.load(f)

if title not in lengths:
    lengths[title] = {}
lengths[title]['byhand'] = [float(p) for p in sys.argv[2].split(',') if p]
with open('rupodcast_lengths.json', 'w') as f:
    json.dump(lengths, f, ensure_ascii=False)
