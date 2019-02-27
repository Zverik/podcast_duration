import requests
import re
import json


def extract_hms(m):
    return [float(g[0] or 0) * 60 + float(g[1]) + float(g[2]) / 60 for g in m]


EXTRACTORS = {
    'overcast': (
     re.compile(r'&bull;\s+(\d+) min'),
     lambda m: [float(x) for x in m]),
    'soundcloud': (
     re.compile(r'meta itemprop="duration" content="PT(\d\d)H(\d\d)M(\d\d)S"'),
     extract_hms),
    'vk': (
     re.compile(r'<div class="[^"]*audio_row__duration[^"]*">(?:(\d):)?(\d+):(\d+)</div>'),
     extract_hms),
    'rss': (
     re.compile(r'<itunes:duration>(?:(\d+):)?(\d+):(\d+)\s*</itunes:duration>', re.M | re.S),
     extract_hms),
    'spotify': (
     re.compile(r'<span class="total-duration">(?:(\d+):)?(\d+):(\d+)</span>'),
     extract_hms),
}


def download_data():
    resp = requests.get('https://russiancast.club/data.json')
    return resp.json()


def read_lengths():
    with open('rupodcast_lengths.json', 'r') as f:
        return json.load(f)


def write_lengths(lengths):
    with open('rupodcast_lengths.json', 'w') as f:
        json.dump(lengths, f, ensure_ascii=False)


def get_durations(podcast):
    mins = {}
    for name, ex in EXTRACTORS.items():
        if podcast.get(name):
            resp = requests.get(podcast[name])
            m = ex[0].findall(resp.text)
            if m:
                mins[name] = ex[1](m)
    return mins


def find_longest_mins(lengths):
    ll = [[x for x in p if x >= 1] for p in lengths.values()]
    return sorted(ll, key=lambda d: len(d))[-1]


def find_medians(mins):
    mins.sort()
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
        dmed = len(mins) // 5
    med_low = round(mins[dmed])
    med_high = round(mins[-1-dmed])
    return median, med_low, med_high


def format_medians(median, med_low, med_high):
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

    need_two = med_high-med_low > 10 and med_high * 1.0 / med_low > 1.5
    if need_two:
        res = '{}—{} {}'.format(r5(med_low), r5(med_high), minut(r5(med_high)))
    else:
        res = '{} {}'.format(r5(median), minut(r5(median)))
    return res
