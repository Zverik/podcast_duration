#!/usr/bin/env python3
import requests
import json
import dutil


with open('rupodcast_lengths.json', 'r') as f:
    lengths = json.load(f)

resp = requests.get('https://russiancast.club/data.json')
data = resp.json()

for p in data:
    if not lengths.get(p['title']):
        print('No data on {} in lengths'.format(p['title']))
        continue
    mins = dutil.find_longest_mins(lengths[p['title']])
    median, med_low, med_high = dutil.find_median(mins)
    res = dutil.format_medians(median, med_low, med_high)
    print('{} ({}): [{} {} {}] -> {}'.format(
        p['title'], len(mins),
        med_low, median, med_high,
        res
    ))
    p['duration'] = res

with open('rupodcast_minutes.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
