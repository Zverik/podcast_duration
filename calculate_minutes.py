#!/usr/bin/env python3
import json
import datetime
import dutil


def calc_duration(lengths):
    mins = dutil.find_longest_mins(lengths)
    if not mins:
        return None
    median, med_low, med_high = dutil.find_medians(mins)
    res = dutil.format_medians(median, med_low, med_high)
    return '({}): [{} {} {}] -> {}'.format(
        len(mins), med_low, median, med_high, res)


def calc_frequency(lengths):
    dates = dutil.find_longest_dates(lengths)
    if not dates:
        return None
    latest = dutil.get_latest_date(dates)
    age = (datetime.datetime.now() - datetime.datetime.strptime(
        latest, dutil.DATE_FORMAT)).days
    interval = dutil.get_median_interval(dates)
    if interval:
        status = 'inactive' if interval and age > max(32, interval[0]*2) else 'active'
        res = dutil.format_interval(*interval)
    else:
        status = '?'
        res = ''
    return '({}): {}, {}'.format(len(dates), status, res)


lengths = dutil.read_lengths()
data = dutil.download_data()
not_found = []

for p in data:
    if not lengths.get(p['title']):
        # not_found.append(p['title'])
        continue
    print(p['title'], calc_frequency(lengths[p['title']]))
    p.update(dutil.gen_additional_fields(lengths[p['title']]))

with open('rupodcast_minutes.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

if not_found:
    print('Missing lengths:\n{}'.format('\n'.join(not_found)))
