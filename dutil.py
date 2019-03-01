import requests
import re
import json
import datetime
import os


def extract_hms(g):
    return float(g[0] or 0) * 60 + float(g[1]) + float(g[2]) / 60


def extract_rss(dur):
    g = dur.split(':')
    while len(g) < 3:
        g = [0] + g
    return float(g[0] or 0) * 60 + float(g[1]) + float(g[2]) / 60


def parse_soundcloud_date(m):
    return None


MONTHS = {m: i+1 for i, m in enumerate(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])}


def parse_overcast_date(m):
    month = MONTHS.get(m[0])
    if not month:
        return None
    year = int(m[2] or datetime.date.today().year)
    return year, month, int(m[1])


def parse_rss_date(m):
    month = MONTHS.get(m[1])
    if not month:
        return None
    return int(m[2]), month, int(m[0])


EXTRACTORS = {
    'overcast': {
        'duration': (re.compile(r'&bull;\s+(\d+) min'), lambda x: float(x)),
        'date': (re.compile(r'<div class="caption2[^"]+">\s+([A-Z][a-z]{2})\s+(\d+)(?:, (\d{4}))?\s+(?:&bull;[^<]+)?</div>', re.S),
                 parse_overcast_date),
    },
    'soundcloud': {
        'duration': (re.compile(r'meta itemprop="duration" content="PT(\d\d)H(\d\d)M(\d\d)S"'),
                     extract_hms),
        'date': (re.compile(r'<time pubdate>(\d{4})/(\d\d)/(\d\d) '),
                 lambda m: (int(m[0]), int(m[1]), int(m[2]))),
    },
    'vk': {
        'duration': (
            re.compile(r'<div class="[^"]*audio_row__duration[^"]*">(?:(\d):)?(\d+):(\d+)</div>'.encode()),
            extract_hms),
    },
    'rss': {
        'duration': (re.compile(r'<itunes:duration>\s*([\d:]+)\s*</itunes:duration>', re.M | re.S),
                     extract_rss),
        'date': (re.compile(r'<pubDate>[^<\d]*(\d+) ([A-Z][a-z]{2}) (\d{4}) '), parse_rss_date),
    },
    'spotify': {
        'duration': (re.compile(r'<span class="total-duration">(?:(\d+):)?(\d+):(\d+)</span>'),
                     extract_hms),
        'date': (re.compile(r'<span class="artists-albums">(\d\d)/(\d\d)/(\d{4})</span>'),
                 lambda m: (int(m[2]), int(m[0]), int(m[1]))),
    },
}


def download_data():
    resp = requests.get('https://russiancast.club/data.json')
    return resp.json()


def read_lengths():
    if not os.path.exists('rupodcast_lengths.json'):
        return {}
    with open('rupodcast_lengths.json', 'r') as f:
        return json.load(f)


def write_lengths(lengths):
    with open('rupodcast_lengths.json', 'w') as f:
        json.dump(lengths, f, ensure_ascii=False)


def parse_text(ex_name, text):
    result = {}
    for k, parser in EXTRACTORS[ex_name].items():
        m = parser[0].findall(text)
        if m and parser:
            result[k] = [parser[1](g) for g in m]
    return result


def get_durations(podcast):
    mins = {}
    for name in EXTRACTORS:
        if name == 'vk':
            continue
        if podcast.get(name):
            resp = requests.get(podcast[name])
            res = parse_text(name, resp.text)
            if res:
                mins[name] = res
    return mins


def find_longest_mins(lengths):
    durs = {k: v.get('duration', []) for k, v in lengths.items()}
    ll = [[x for x in p if x >= 1] for p in durs.values()]
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
