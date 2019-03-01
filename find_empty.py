#!/usr/bin/env python3
import json
import dutil

data = dutil.read_lengths()
for title, d in data.items():
    for k in ('date', 'duration'):
        cnt = max([0] + [len(v.get(k, [])) for v in d.values()])
        if cnt <= 1:
            if k == 'duration':
                for src in d:
                    if k in d[src]:
                        d[src][k] = [round(x) for x in d[src][k]]
            print(title, k, json.dumps({src: d[src].get(k) for src in d}))
