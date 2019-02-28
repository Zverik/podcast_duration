#!/usr/bin/env python3
import dutil

data = dutil.download_data()
result = dutil.read_lengths()
for p in data:
    if result.get(p['title']):
        continue
    print(p['title'])
    mins = dutil.get_durations(p)
    if mins:
        result[p['title']] = mins
dutil.write_lengths(result)
