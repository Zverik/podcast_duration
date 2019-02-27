#!/usr/bin/env python3
import dutil

data = dutil.download_data()
result = dutil.read_lengths()
for p in data:
    if p['title'] in result:
        continue
    print(p['title'])
    mins = dutil.get_durations(p)
    result[p['title']] = mins
dutil.write_lengths(result)
