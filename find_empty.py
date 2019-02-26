#!/usr/bin/env python3
import json

with open('rupodcast_lengths.json', 'r') as f:
    data = json.load(f)

for title, d in data.items():
    cnt = max([0] + [len(v) for v in d.values()])
    if cnt <= 1:
        for k in d:
            d[k] = [round(x) for x in d[k]]
        print(title, json.dumps(d))
