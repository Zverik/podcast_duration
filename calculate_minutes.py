#!/usr/bin/env python3
import json
import dutil


lengths = dutil.read_lengths()
data = dutil.download_data()
not_found = []

for p in data:
    if not lengths.get(p['title']):
        not_found.append(p['title'])
        continue
    mins = dutil.find_longest_mins(lengths[p['title']])
    median, med_low, med_high = dutil.find_medians(mins)
    res = dutil.format_medians(median, med_low, med_high)
    print('{} ({}): [{} {} {}] -> {}'.format(
        p['title'], len(mins),
        med_low, median, med_high,
        res
    ))
    p['duration'] = res

with open('rupodcast_minutes.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

if not_found:
    print('Missing lengths:\n{}'.format('\n'.join(not_found)))
