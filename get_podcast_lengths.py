#!/usr/bin/env python3
import requests
import json
import re
import time

resp = requests.get('https://russiancast.club/data.json')
data = resp.json()

RE_OVERCAST = re.compile(r'&bull;\s+(\d+) min')
RE_SOUNDCLOUD = re.compile(r'meta itemprop="duration" content="PT(\d\d)H(\d\d)M(\d\d)S"')
RE_VK = re.compile(r'<div class="[^"]*audio_row__duration[^"]*">(?:(\d):)?(\d+):(\d+)</div>')
RE_RSS = re.compile(r'<itunes:duration>(?:(\d+):)?(\d+):(\d+)\s*</itunes:duration>', re.M | re.S)
RE_SPOTIFY = re.compile(r'<span class="total-duration">(?:(\d+):)?(\d+):(\d+)</span>')
result = {}
for p in data:
    print(p['title'])
    mins = {}
    if p.get('overcast'):
        overcast = requests.get(p['overcast'])
        m = RE_OVERCAST.findall(overcast.text)
        if m:
            mins['overcast'] = [float(x) for x in m]
    for t in (('soundcloud', RE_SOUNDCLOUD), ('vk', RE_VK),
              ('rss', RE_RSS), ('spotify', RE_SPOTIFY)):
        if p.get(t[0]):
            resp = requests.get(p[t[0]])
            m = t[1].findall(resp.text)
            if m:
                mins[t[0]] = [float(g[0] or 0) * 60 + float(g[1]) + float(g[2]) / 60 for g in m]
    result[p['title']] = mins
    time.sleep(0.5)

with open('rupodcast_lengths.json', 'w') as f:
    json.dump(result, f, ensure_ascii=False)
