#!/usr/bin/env python3
import dutil
import json
import argparse
import os
import logging
from datetime import datetime


def augment(url, values, data, result):
    if 'vk.com' in url:
        types = ['vk']
        atype = 'vk'
        with open(values, 'rb') as f:
            values = f.read()
    else:
        types = ['itunes', 'soundcloud']
        atype = 'byhand'
    podcast = None
    for p in data:
        for t in types:
            if t in p and url in p[t]:
                title = p['title']
                podcast = p
        if podcast:
            break
    logging.info('Augmenting %s with %s', title, atype)
    found = False
    if title:
        gen = dutil.parse_text(atype, values)
        if gen:
            found = True
            if title not in result:
                result[title] = {}
            if atype in result[title]:
                result[title][atype].update(gen)
            else:
                result[title][atype] = gen
            podcast.update(dutil.gen_additional_fields(result[title]))
    if not found:
        logging.warning('Did not alter anything for %s', title)


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
    age = (datetime.now() - datetime.strptime(latest, dutil.DATE_FORMAT)).days
    interval = dutil.get_median_interval(dates)
    active = age <= (32 if not interval else max(32, interval[1] + interval[2]))
    status = 'active' if active else 'inactive'
    if interval:
        res = dutil.format_interval(*interval)
        return '({}): [{} {} {}] -> {}, {}'.format(
            len(dates), interval[1], interval[0], interval[2], res, status)
    return '({}): {}'.format(len(dates), status)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Downloads all podcast data')
    parser.add_argument('data', type=argparse.FileType('w'),
                        help='File to write')
    parser.add_argument('-i', '--input', type=argparse.FileType('r'),
                        help='Use file instead of downloading the json')
    parser.add_argument('-s', '--status', help='File name to write status to')
    parser.add_argument('-a', '--augment', type=argparse.FileType('r'),
                        help='File with augmentation data')
    parser.add_argument('-l', '--lengths', help='Use intermediate lengths data')
    parser.add_argument('-u', '--update', action='store_true',
                        help='Update entries already in the lengths file')
    parser.add_argument('-c', '--calc', action='store_true',
                        help='Do not update the data, just print durations and frequencies')
    options = parser.parse_args()

    logging.basicConfig(level=logging.INFO, datefmt='%H:%M:%S',
                        format='%(asctime)s %(levelname)-7s  %(message)s')

    if options.input:
        data = json.load(options.input)
    else:
        logging.info('Downloading data')
        data = dutil.download_data()

    lengths = {}
    if options.lengths:
        if os.path.exists(options.lengths):
            with open(options.lengths, 'r') as f:
                lengths = json.load(f)
                logging.info('Read %s lengths', len(lengths))

    if options.calc:
        not_found = []
        for p in data:
            title = p['title']
            if not lengths.get(title):
                not_found.append(title)
                continue
            print(title, calc_duration(lengths[title]))
            print(title, calc_frequency(lengths[title]))

        for t in not_found:
            print('Missing: {}'.format(t))
        raise SystemExit

    for i, p in enumerate(data):
        title = p['title']
        if title not in lengths or options.update:
            logging.info('Downloading %s', title)
            if options.status:
                with open(options.status, 'w') as f:
                    f.write('Processing {} ({}/{})'.format(title, i+1, len(data)))
            mins = dutil.get_durations(p)
            if mins:
                lengths[title] = mins
        if title in lengths:
            p.update(dutil.gen_additional_fields(lengths[title]))

    if options.lengths:
        with open(options.lengths, 'w') as f:
            json.dump(lengths, f, ensure_ascii=False)

    if options.augment:
        for line in options.augment:
            if len(line) == 0 or line[0] == '#':
                continue
            aug = line.split()
            if len(aug) == 2:
                augment(aug[0], aug[1], data, lengths)

    if options.lengths:
        with open(options.lengths, 'w') as f:
            json.dump(lengths, f, ensure_ascii=False)

    for title, d in lengths.items():
        for k in ('date', 'duration'):
            cnt = max([0] + [len(v.get(k, [])) for v in d.values()])
            if cnt <= 1:
                if k == 'duration':
                    for src in d:
                        if k in d[src]:
                            d[src][k] = [round(x) for x in d[src][k]]
                logging.warning('Missing %s for %s: %s', k, title,
                                json.dumps({src: d[src].get(k) for src in d}))

    logging.info('Writing data')
    json.dump(data, options.data, ensure_ascii=False, indent=1)

    if options.status and os.path.exists(options.status):
        os.unlink(options.status)
    logging.info('Done')
