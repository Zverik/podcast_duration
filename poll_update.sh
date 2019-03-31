#!/bin/sh
cd "$(dirname "$0")"
STATUS=status.txt
[ -e $STATUS ] && exit 0
[ ! -e data.json ] && echo "Needs data.json" && exit 2
python3 update_lengths.py static/result.json -i data.json -a augment.lst -u -s $STATUS
rm -f $STATUS
