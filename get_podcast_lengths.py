#!/usr/bin/env python3
import json
import dutil

data = dutil.download_data()
result = {}
for p in data:
    print(p['title'])
    mins = dutil.get_durations(p)
    result[p['title']] = mins

with open('rupodcast_lengths.json', 'w') as f:
    json.dump(result, f, ensure_ascii=False)
