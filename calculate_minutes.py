#!/usr/bin/env python3
import requests
import json


def r5(n):
    if n < 14:
        return n
    return round(n/5.0)*5


def minut(n):
    if n % 10 == 1 and n % 100 != 11:
        return 'минута'
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return 'минуты'
    return 'минут'


with open('rupodcast_lengths.json', 'r') as f:
    lengths = json.load(f)

resp = requests.get('https://russiancast.club/data.json')
data = resp.json()

for p in data:
    if not lengths.get(p['title']):
        print('No data on {} in lengths'.format(p['title']))
        continue
    ll = [[x for x in p if x >= 1] for p in lengths[p['title']].values()]
    mins = sorted(sorted(ll, key=lambda d: len(d))[-1])
    if len(mins) == 1:
        median = round(mins[0])
    elif len(mins) % 2 == 0:
        median = round((float(mins[len(mins)//2-1]) + mins[len(mins)//2]) / 2.0)
    else:
        median = round(mins[len(mins)//2])
    if len(mins) <= 2:
        dmed = 0
    elif len(mins) <= 5:
        dmed = 1
    elif len(mins) <= 10:
        dmed = 2
    else:
        dmed = len(mins) // 10 + 1
    med_low = round(mins[dmed])
    med_high = round(mins[-1-dmed])
    need_two = (max(med_high-median, median-med_low) > 10 and
                med_high * 1.0 / med_low > 2)
    if need_two:
        res = '{}—{} {}'.format(r5(med_low), r5(med_high), minut(r5(med_high)))
    else:
        res = '{} {}'.format(r5(median), minut(r5(median)))
    print('{} ({}): [{} {} {}] -> {}'.format(
        p['title'], len(mins),
        med_low, median, med_high,
        res
    ))
    p['duration'] = res

with open('rupodcast_minutes.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
