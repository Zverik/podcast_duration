# Aquiring Durations

These scripts were made specifically for [RussianCast](https://russiancast.club/),
although you can use them for whatever.

* `run.sh` — what I ran to get the resulting json.
* `get_podcast_lengths.py` — downloads a list of podcasts from the website and then
    checks every source for track durations. Produces `rupodcast_lengths.json` which
    other tools then enrich.
* `find_empty.py` — shows empty or nearly empty entries in the json.
* `by_hand.py` — adds a minute durations list to a given podcast referenced by
    an iTunes URL substring.
* `parse_vk.py` — parses an HTML from vk.com for durations
* `calculate_minutes.py` — calculates final duration strings for each podcast
    and writes the result into `rupodcast_minutes.json`.

## Author and License

Written by Ilya Zverev, published under WTFPL.
