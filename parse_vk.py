#!/usr/bin/env python3
import json
import requests
import re
import sys

if len(sys.argv) < 2:
    print('Usage: {} <vk_url> <html>'.format(sys.argv[0]))
    sys.exit(1)

resp = requests.get('https://russiancast.club/data.json')
data = resp.json()
title = [p['title'] for p in data if p.get('vk') == sys.argv[1]][0]

with open('rupodcast_lengths.json', 'r') as f:
    lengths = json.load(f)

with open(sys.argv[2], 'rb') as f:
    text = f.read()
RE_VK = re.compile(r'<div class="[^"]*audio_row__duration[^"]*">(?:(\d):)?(\d+):(\d+)</div>'.encode())
m = RE_VK.findall(text)
if m:
    if title not in lengths:
        lengths[title] = {}
    lengths[title]['vk'] = [float(g[0] or 0) * 60 + float(g[1]) + float(g[2]) / 60 for g in m]
    with open('rupodcast_lengths.json', 'w') as f:
        json.dump(lengths, f, ensure_ascii=False)
